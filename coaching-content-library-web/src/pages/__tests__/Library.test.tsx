import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Library } from '../Library';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import React from 'react';
import { vi, Mock } from 'vitest';
import { useContentList } from '@/hooks/useContentList';

// Mock the entire module
vi.mock('@/hooks/useContentList');

// Mock data for successful fetch - must match ContentItem type
const mockContentItems = [
  {
    id: 1,
    title: 'Test Drill 1',
    source: 'YouTube',
    content_type: 'Video',
    url: 'https://youtube.com/watch?v=1',
    author: 'Coach Mike',
    thumbnail_url: 'https://example.com/thumb1.jpg',
    drill_description: 'A drill to improve passing.',
    drill_tags: ['passing', 'beginner'],
    difficulty: 'Beginner',
    age_group: null,
    equipment: null,
    view_count: null,
    published_at: '2024-01-01T00:00:00Z',
    fetched_at: '2024-01-01T00:00:00Z',
    saved_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    title: 'Test Drill 2',
    source: 'Reddit',
    content_type: 'Post',
    url: 'https://reddit.com/r/hockey/2',
    author: 'Coach Sarah',
    thumbnail_url: 'https://example.com/thumb2.jpg',
    drill_description: 'An advanced shooting drill.',
    drill_tags: ['shooting', 'advanced'],
    difficulty: 'Advanced',
    age_group: null,
    equipment: null,
    view_count: null,
    published_at: '2024-01-02T00:00:00Z',
    fetched_at: '2024-01-02T00:00:00Z',
    saved_at: '2024-01-02T00:00:00Z',
  },
];

const handlers = [
  http.get('/api/v1/content', () => {
    return HttpResponse.json({
      items: mockContentItems,
      total: mockContentItems.length,
      page: 1,
      size: 10,
      pages: 1,
    });
  }),
];

const server = setupServer(...handlers);

// Server setup
beforeAll(() => server.listen());
afterEach(() => {
  server.resetHandlers();
  vi.resetAllMocks();
});
afterAll(() => server.close());

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{children}</MemoryRouter>
    </QueryClientProvider>
  );
};

describe('Library Page', () => {
  it('should render the Drill Library heading', async () => {
    (useContentList as Mock).mockReturnValue({
      data: { items: [] },
      isLoading: false,
      isError: false,
    });
    render(<Library />, { wrapper: createWrapper() });

    await waitFor(() => {
        expect(screen.getByText('Drill Library')).toBeInTheDocument();
    });
  });

  it('should display loading state when data is fetching', async () => {
    (useContentList as Mock).mockReturnValue({
      data: undefined,
      isLoading: true,
      isError: false,
      error: null,
      refetch: vi.fn(),
    });

    render(<Library />, { wrapper: createWrapper() });

    expect(screen.getAllByTestId('loading-skeleton')).toHaveLength(4);
  });

  it('should display error state when data fetching fails', async () => {
    const mockRefetch = vi.fn();
    (useContentList as Mock).mockReturnValue({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error('Failed to fetch content'),
      refetch: mockRefetch,
    });

    render(<Library />, { wrapper: createWrapper() });

    await waitFor(() => {
      expect(screen.getByText('Failed to load drills. Please try again.')).toBeInTheDocument();
      const retryButton = screen.getByRole('button', { name: /Try Again/i });
      expect(retryButton).toBeInTheDocument();

      // Verify refetch is called on retry button click
      fireEvent.click(retryButton);
      expect(mockRefetch).toHaveBeenCalledTimes(1);
    });
  });

  it('should display drill cards on successful data fetch', async () => {
    (useContentList as Mock).mockReturnValue({
      data: { items: mockContentItems, total: mockContentItems.length },
      isLoading: false,
      isError: false,
      error: null,
      refetch: vi.fn(),
    });

    render(<Library />, { wrapper: createWrapper() });

    await waitFor(() => {
      // Check drill titles are rendered
      expect(screen.getByText('Test Drill 1')).toBeInTheDocument();
      expect(screen.getByText('Test Drill 2')).toBeInTheDocument();

      // Check authors are rendered
      expect(screen.getByText('Coach Mike')).toBeInTheDocument();
      expect(screen.getByText('Coach Sarah')).toBeInTheDocument();

      // Check source badges
      expect(screen.getByText('YouTube')).toBeInTheDocument();
      expect(screen.getByText('Reddit')).toBeInTheDocument();

      // Check difficulty badges
      expect(screen.getByText('Beginner')).toBeInTheDocument();
      expect(screen.getByText('Advanced')).toBeInTheDocument();

      // Check drill tags are displayed
      expect(screen.getByText('passing')).toBeInTheDocument();
      expect(screen.getByText('shooting')).toBeInTheDocument();
    });
  });

  it('should display empty state when data returns empty array', async () => {
    (useContentList as Mock).mockReturnValue({
      data: { items: [], total: 0 },
      isLoading: false,
      isError: false,
      error: null,
      refetch: vi.fn(),
    });

    render(<Library />, { wrapper: createWrapper() });

    await waitFor(() => {
      expect(screen.getByText('No drills yet')).toBeInTheDocument();
      expect(screen.getByText(/Your drill library is empty/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Add Your First Drill/i })).toBeInTheDocument();
    });
  });
});
