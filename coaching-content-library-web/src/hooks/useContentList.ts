import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type { ContentListResponse } from '@/lib/types';

/**
 * useContentList Hook
 *
 * Fetches list of drills from GET /api/v1/content endpoint
 * Uses TanStack Query for server state management with caching and automatic refetch
 *
 * @returns {Object} Query state with data, loading, and error states
 * @returns {ContentListResponse | undefined} data - List of drills with pagination info
 * @returns {boolean} isLoading - True while fetching data
 * @returns {boolean} isError - True if query encountered an error
 * @returns {Error | null} error - Error object if query failed, null otherwise
 *
 * @example
 * const { data, isLoading, isError, error } = useContentList();
 *
 * if (isLoading) return <LoadingState />;
 * if (isError) return <ErrorState error={error} />;
 * return <DrillGrid drills={data?.items} />;
 */
export function useContentList() {
  return useQuery<ContentListResponse>({
    queryKey: ['content'],
    queryFn: async () => {
      const response = await api.get<{ data: ContentListResponse }>('/content');
      return response.data.data;
    },
  });
}
