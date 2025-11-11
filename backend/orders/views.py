from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from cart.models import Cart, CartItem
from .payment import create_razorpay_order, verify_razorpay_payment
from .delivery import create_delivery_order


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get user's cart
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
        except Cart.DoesNotExist:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate totals
        subtotal = sum(item.total_price for item in cart_items)
        shipping_cost = 50  # Fixed shipping cost, can be made dynamic
        total = subtotal + shipping_cost
        payment_method = serializer.validated_data.get('payment_method', 'cod')

        # Create order
        order = Order.objects.create(
            user=request.user,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            payment_method=payment_method,
            payment_status='pending' if payment_method == 'razorpay' else 'pending',
            shipping_address=serializer.validated_data['shipping_address'],
            shipping_city=serializer.validated_data['shipping_city'],
            shipping_state=serializer.validated_data['shipping_state'],
            shipping_zip_code=serializer.validated_data['shipping_zip_code'],
            shipping_phone=serializer.validated_data['shipping_phone'],
            notes=serializer.validated_data.get('notes', ''),
        )

        # Create order items
        order_items_data = []
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.final_price,
            )
            order_items_data.append({
                'name': cart_item.product.name,
                'quantity': cart_item.quantity,
                'price': float(cart_item.product.final_price)
            })

        # Handle Razorpay payment
        razorpay_order = None
        if payment_method == 'razorpay':
            razorpay_order = create_razorpay_order(
                amount=total,
                receipt=order.order_number
            )
            if razorpay_order:
                order.razorpay_order_id = razorpay_order.get('id')
                order.save()
            else:
                order.delete()
                return Response({'error': 'Failed to create payment order'}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create delivery order with Delhivery
        delivery_data = {
            'order_id': order.order_number,
            'delivery_address': serializer.validated_data['shipping_address'],
            'delivery_city': serializer.validated_data['shipping_city'],
            'delivery_state': serializer.validated_data['shipping_state'],
            'delivery_pincode': serializer.validated_data['shipping_zip_code'],
            'customer_name': f"{request.user.first_name or ''} {request.user.last_name or ''}".strip() or request.user.email,
            'customer_phone': serializer.validated_data['shipping_phone'],
            'items': order_items_data,
            'total_amount': float(total),
            'payment_method': payment_method
        }
        
        delivery_result = create_delivery_order(delivery_data)
        if delivery_result.get('success'):
            order.delivery_partner_order_id = delivery_result.get('order_id')
            order.delivery_tracking_id = delivery_result.get('tracking_id')
            order.delivery_status = delivery_result.get('status', 'Pending')
            order.save()
        else:
            # Log error but don't fail the order creation
            print(f"Delhivery order creation failed: {delivery_result.get('message')}")
            order.delivery_status = 'Pending Manual Entry'
            order.save()

        # For COD, mark as processing and clear cart
        # For Razorpay, cart will be cleared after payment verification
        if payment_method == 'cod':
            order.status = 'processing'
            order.payment_status = 'pending'  # Will be updated when payment is collected
            order.save()
            cart.items.all().delete()

        # Return order details
        order_serializer = OrderSerializer(order)
        response_data = order_serializer.data
        
        # Add Razorpay order details if payment method is Razorpay
        if payment_method == 'razorpay' and razorpay_order:
            from decouple import config
            response_data['razorpay_order_id'] = razorpay_order.get('id')
            response_data['razorpay_key'] = config('RAZORPAY_KEY_ID', default='')
        
        return Response(response_data, status=status.HTTP_201_CREATED)

