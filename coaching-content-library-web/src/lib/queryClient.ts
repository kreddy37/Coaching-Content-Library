import { QueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
      throwOnError: false,
    },
    mutations: {
      retry: 1,
      onError: (error: Error) => {
        const errorMessage = error instanceof Error ? error.message : 'Mutation failed';
        toast.error(errorMessage);
      },
    },
  },
});
