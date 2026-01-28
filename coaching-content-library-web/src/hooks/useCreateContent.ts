/**
 * useCreateContent Hook
 *
 * Placeholder for Epic 8 implementation
 * Will create new drill with POST /api/v1/content
 *
 * Usage:
 * const mutation = useCreateContent();
 * mutation.mutate({ url, title, ... });
 */

export function useCreateContent(): {
  mutate: () => void;
  isPending: boolean;
  error: null;
} {
  // Placeholder implementation for future Epic 8
  return {
    mutate: () => {},
    isPending: false,
    error: null,
  };
}
