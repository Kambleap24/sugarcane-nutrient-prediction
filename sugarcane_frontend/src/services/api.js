import axios from 'axios';

// CRITICAL: Match your backend port
const API_URL = 'http://localhost:5000/api';

console.log('🌐 API Configuration:');
console.log(`   Base URL: ${API_URL}`);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
});

// Add request interceptor for logging
api.interceptors.request.use(
  config => {
    console.log(`📤 API Request: ${config.method.toUpperCase()} ${config.url}`);
    if (config.data) {
      console.log(`   Data: `, config.data);
    }
    return config;
  },
  error => {
    console.error('❌ Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for logging
api.interceptors.response.use(
  response => {
    console.log(`📥 API Response: ${response.status}`, response.data);
    return response;
  },
  error => {
    console.error('❌ Response error:', error);
    if (error.response) {
      console.error('   Status:', error.response.status);
      console.error('   Data:', error.response.data);
    }
    return Promise.reject(error);
  }
);

// API functions
export const predictNutrients = async (formData) => {
  try {
    console.log('🔮 Making prediction...');
    const response = await api.post('/predict', formData);
    console.log('✅ Prediction successful:', response.data);
    return response.data;
  } catch (error) {
    const errorMsg = error.response?.data?.error || error.message || 'Prediction failed';
    console.error('❌ Prediction error:', errorMsg);
    throw new Error(errorMsg);
  }
};

export const getHistory = async () => {
  try {
    console.log('📜 Fetching history...');
    const response = await api.get('/history?limit=50&days=30');
    console.log('✅ History fetched:', response.data);
    return response.data;
  } catch (error) {
    const errorMsg = error.response?.data?.error || error.message || 'Failed to fetch history';
    console.error('❌ History error:', errorMsg);
    throw new Error(errorMsg);
  }
};

export const getStatistics = async () => {
  try {
    console.log('📊 Fetching statistics...');
    const response = await api.get('/statistics?days=30');
    console.log('✅ Statistics fetched:', response.data);
    return response.data;
  } catch (error) {
    const errorMsg = error.response?.data?.error || error.message || 'Failed to fetch statistics';
    console.error('❌ Statistics error:', errorMsg);
    throw new Error(errorMsg);
  }
};

export const healthCheck = async () => {
  try {
    console.log('🏥 Checking backend health...');
    const response = await api.get('/health');
    console.log('✅ Backend healthy:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Backend unhealthy');
    return { status: 'unhealthy' };
  }
};

export default api;
