'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import axios from 'axios'
import { FiShoppingBag, FiTruck, FiShield, FiStar } from 'react-icons/fi'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

interface Product {
  id: number
  name: string
  slug: string
  price: string
  discount_price?: string
  final_price: string
  discount_percentage: number
  image?: string
  primary_image?: string
  rating: string
}

export default function Home() {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchFeaturedProducts()
    fetchCategories()
  }, [])

  const fetchFeaturedProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/products/featured/`)
      setFeaturedProducts(response.data.slice(0, 8))
    } catch (error) {
      console.error('Error fetching featured products:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/products/categories/`)
      // Categories are not paginated, so response.data is directly the array
      const categoriesData = response.data.results || response.data || []
      const categoriesArray = Array.isArray(categoriesData) ? categoriesData : []
      setCategories(categoriesArray.slice(0, 6))
    } catch (error) {
      console.error('Error fetching categories:', error)
      setCategories([]) // Set empty array on error
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="bg-gradient-to-r from-primary-600 to-secondary-600 text-white py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="flex justify-center mb-6">
              <div className="relative w-32 h-32 md:w-40 md:h-40 rounded-full overflow-hidden border-4 border-white shadow-2xl bg-white">
                <Image
                  src="/logo.png"
                  alt="NextBloom Logo"
                  fill
                  className="object-contain p-3"
                  priority
                  sizes="(max-width: 768px) 128px, 160px"
                />
              </div>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Fresh Groceries, Delivered Fresh
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              Shop the finest selection of organic produce and groceries
            </p>
            <Link href="/products" className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition-colors inline-block">
              Shop Now
            </Link>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FiTruck className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Free Delivery</h3>
                <p className="text-gray-600">On orders over $50</p>
              </div>
              <div className="text-center">
                <div className="bg-accent-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FiShield className="w-8 h-8 text-accent-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Secure Payment</h3>
                <p className="text-gray-600">100% secure transactions</p>
              </div>
              <div className="text-center">
                <div className="bg-secondary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FiStar className="w-8 h-8 text-secondary-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Quality Products</h3>
                <p className="text-gray-600">Fresh and organic</p>
              </div>
              <div className="text-center">
                <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FiShoppingBag className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Easy Returns</h3>
                <p className="text-gray-600">7-day return policy</p>
              </div>
            </div>
          </div>
        </section>

        {/* Categories Section */}
        <section className="py-16 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-center mb-12">Shop by Category</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
              {Array.isArray(categories) && categories.length > 0 ? (
                categories.map((category) => (
                  <Link
                    key={category.id}
                    href={`/products?category=${category.id}`}
                    className="card p-6 text-center hover:scale-105 transition-transform"
                  >
                    <div className="bg-primary-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                      <FiShoppingBag className="w-10 h-10 text-primary-600" />
                    </div>
                    <h3 className="font-semibold">{category.name}</h3>
                  </Link>
                ))
              ) : (
                <div className="col-span-6 text-center text-gray-500">No categories available</div>
              )}
            </div>
          </div>
        </section>

        {/* Featured Products Section */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-center mb-12">Featured Products</h2>
            {loading ? (
              <div className="text-center py-12">Loading...</div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {featuredProducts.map((product) => (
                  <Link
                    key={product.id}
                    href={`/products/${product.slug}`}
                    className="card p-4 hover:scale-105 transition-transform"
                  >
                    <div className="relative mb-4">
                      <div className="w-full h-48 bg-gray-200 rounded-lg flex items-center justify-center">
                        {product.primary_image || product.image ? (
                          <img
                            src={product.primary_image || product.image}
                            alt={product.name}
                            className="w-full h-full object-cover rounded-lg"
                            onError={(e) => {
                              (e.target as HTMLImageElement).src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgZmlsbD0iI2U1ZTdlYSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM5Y2EzYWYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5Qcm9kdWN0IEltYWdlPC90ZXh0Pjwvc3ZnPg=='
                            }}
                          />
                        ) : (
                          <span className="text-gray-400">No Image</span>
                        )}
                      </div>
                      {product.discount_percentage > 0 && (
                        <span className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded text-sm font-semibold">
                          -{product.discount_percentage}%
                        </span>
                      )}
                    </div>
                    <h3 className="font-semibold mb-2">{product.name}</h3>
                      <div className="flex items-center justify-between">
                        <div>
                          {product.discount_price ? (
                            <div>
                              <span className="text-primary-600 font-bold">₹{product.final_price}</span>
                              <span className="text-gray-400 line-through ml-2">₹{product.price}</span>
                            </div>
                          ) : (
                            <span className="text-primary-600 font-bold">₹{product.price}</span>
                          )}
                        </div>
                      <div className="flex items-center">
                        <FiStar className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                        <span className="ml-1 text-sm">{product.rating}</span>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
            <div className="text-center mt-8">
              <Link href="/products" className="btn-primary">
                View All Products
              </Link>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  )
}

