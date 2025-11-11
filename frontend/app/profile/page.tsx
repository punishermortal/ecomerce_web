'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import api from '@/lib/axios'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/store/store'
import { setUser } from '@/store/slices/authSlice'
import { useForm } from 'react-hook-form'
import { toast } from 'react-toastify'

interface UserProfile {
  id: number
  email: string
  username: string
  first_name: string
  last_name: string
  phone_number?: string
  address?: string
  city?: string
  state?: string
  zip_code?: string
}

export default function ProfilePage() {
  const router = useRouter()
  const dispatch = useDispatch()
  const { isAuthenticated, user } = useSelector((state: RootState) => state.auth)
  const { register, handleSubmit, formState: { errors }, setValue } = useForm()
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    fetchProfile()
  }, [isAuthenticated, router])

  const fetchProfile = async () => {
    try {
      const response = await api.get('/auth/profile/')
      const profileData = response.data
      setValue('first_name', profileData.first_name || '')
      setValue('last_name', profileData.last_name || '')
      setValue('phone_number', profileData.phone_number || '')
      setValue('address', profileData.address || '')
      setValue('city', profileData.city || '')
      setValue('state', profileData.state || '')
      setValue('zip_code', profileData.zip_code || '')
    } catch (error) {
      console.error('Error fetching profile:', error)
    }
  }

  const onSubmit = async (data: any) => {
    setLoading(true)
    try {
      const response = await api.put('/auth/profile/', data)
      dispatch(setUser(response.data))
      toast.success('Profile updated successfully')
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold mb-8">My Profile</h1>
          
          <div className="card p-8">
            <div className="mb-6">
              <h2 className="text-xl font-semibold mb-2">Account Information</h2>
              <p className="text-gray-600">{user?.email}</p>
              <p className="text-gray-600">{user?.username}</p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">First Name</label>
                  <input
                    {...register('first_name', { required: 'First name is required' })}
                    type="text"
                    className="input-field"
                  />
                  {errors.first_name && (
                    <p className="text-red-500 text-sm mt-1">{errors.first_name.message as string}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Last Name</label>
                  <input
                    {...register('last_name', { required: 'Last name is required' })}
                    type="text"
                    className="input-field"
                  />
                  {errors.last_name && (
                    <p className="text-red-500 text-sm mt-1">{errors.last_name.message as string}</p>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Phone Number</label>
                <input
                  {...register('phone_number')}
                  type="tel"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Address</label>
                <textarea
                  {...register('address')}
                  className="input-field"
                  rows={3}
                />
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">City</label>
                  <input
                    {...register('city')}
                    type="text"
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">State</label>
                  <input
                    {...register('state')}
                    type="text"
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Zip Code</label>
                  <input
                    {...register('zip_code')}
                    type="text"
                    className="input-field"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn-primary disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {loading ? 'Updating...' : 'Update Profile'}
              </button>
            </form>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}

