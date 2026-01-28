import axios, { AxiosError } from 'axios';
import { toast } from 'sonner';

export const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'User-Agent': 'Coaching-Library-Web/1.0',
  },
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    let errorMessage = 'An error occurred';

    if (!error.response) {
      // Network error or timeout
      errorMessage = 'Network error - please check your connection';
      console.error('Network Error:', error.message);
    } else if (error.response.status === 404) {
      // Handle 404 errors
      errorMessage = 'Resource not found';
      console.error('404 Error:', error.message);
    } else if (error.response.status >= 500) {
      // Handle 5xx errors
      errorMessage = 'Server error - please try again later';
      console.error('Server Error:', error.message);
    } else if (error.response.status >= 400) {
      // Handle other 4xx errors
      errorMessage = ((error.response.data as Record<string, unknown>)?.error as string) || 'Request failed';
      console.error(`${error.response.status} Error:`, error.message);
    }

    // Notify user via toast
    toast.error(errorMessage);

    return Promise.reject(new Error(errorMessage));
  }
);
