import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'learner',
    institution: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      return setError('Passwords do not match');
    }
    setError('');
    setIsLoading(true);
    try {
      const { confirmPassword, ...submitData } = formData;
      await register(submitData);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to register');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Card className="max-w-md w-full space-y-6 p-8">
        <div>
          <h2 className="mt-2 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
            Create an account
          </h2>
        </div>
        <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
          {error && <div className="text-red-500 text-sm text-center bg-red-50 dark:bg-red-900/20 p-2 rounded">{error}</div>}
          
          <div>
            <input
              name="name" type="text" required placeholder="Full Name"
              className="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-quantum-500 focus:border-quantum-500 sm:text-sm dark:bg-gray-800 dark:text-white"
              value={formData.name} onChange={handleChange}
            />
          </div>
          <div>
            <input
              name="email" type="email" required placeholder="Email address"
              className="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-quantum-500 focus:border-quantum-500 sm:text-sm dark:bg-gray-800 dark:text-white"
              value={formData.email} onChange={handleChange}
            />
          </div>
          <div>
            <input
              name="password" type="password" required placeholder="Password"
              className="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-quantum-500 focus:border-quantum-500 sm:text-sm dark:bg-gray-800 dark:text-white"
              value={formData.password} onChange={handleChange}
            />
          </div>
          <div>
            <input
              name="confirmPassword" type="password" required placeholder="Confirm Password"
              className="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-quantum-500 focus:border-quantum-500 sm:text-sm dark:bg-gray-800 dark:text-white"
              value={formData.confirmPassword} onChange={handleChange}
            />
          </div>
          <div>
            <select
              name="role"
              className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-700 focus:outline-none focus:ring-quantum-500 focus:border-quantum-500 sm:text-sm rounded-md dark:bg-gray-800 dark:text-white"
              value={formData.role} onChange={handleChange}
            >
              <option value="learner">Learner</option>
              <option value="instructor">Instructor</option>
            </select>
          </div>
          <div>
            <input
              name="institution" type="text" placeholder="Institution (Optional)"
              className="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-quantum-500 focus:border-quantum-500 sm:text-sm dark:bg-gray-800 dark:text-white"
              value={formData.institution} onChange={handleChange}
            />
          </div>

          <div>
            <Button type="submit" className="w-full" loading={isLoading}>
              Register
            </Button>
          </div>
        </form>
        <div className="text-center text-sm text-gray-600 dark:text-gray-400 mt-4">
          Already have an account? <Link to="/login" className="text-quantum-600 hover:text-quantum-500 font-medium">Sign in</Link>
        </div>
      </Card>
    </div>
  );
};

export default RegisterPage;
