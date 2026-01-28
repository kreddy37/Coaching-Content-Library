import { useContentList } from '@/hooks/useContentList';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { DrillCard } from '@/components/drills/DrillCard';
import type { ContentItem } from '@/lib/types';

/**
 * Loading Skeleton Component
 * Displays 3-4 card placeholders with shimmer animation while data loads
 */
function LoadingState() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: 4 }).map((_, index) => (
        <Card key={index} className="overflow-hidden" data-testid="loading-skeleton">
          <Skeleton className="w-full h-48" />
          <div className="p-4 space-y-3">
            <Skeleton className="h-6 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-2/3" />
          </div>
        </Card>
      ))}
    </div>
  );
}

/**
 * Error State Component Props
 */
export interface ErrorStateProps {
  onRetry: () => void;
}

/**
 * Error State Component
 * Displays error message with retry button when API call fails
 */
function ErrorState({ onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="text-center max-w-md">
        <p className="text-xl font-bold text-hockey-blue mb-6">
          Failed to load drills. Please try again.
        </p>
        <Button
          onClick={onRetry}
          className="bg-ice-blue hover:bg-ice-blue/90 text-white"
        >
          Try Again
        </Button>
      </div>
    </div>
  );
}

/**
 * Empty State Component
 * Displays when no drills exist in database
 */
function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="text-center max-w-md">
        <h3 className="text-2xl font-bold text-hockey-blue mb-3">
          No drills yet
        </h3>
        <p className="text-rink-gray mb-6">
          Your drill library is empty. Start by adding drills via the Discord
          bot or web interface.
        </p>
        <Button className="bg-ice-blue hover:bg-ice-blue/90 text-white">
          Add Your First Drill
        </Button>
      </div>
    </div>
  );
}

// DrillCard component now imported from @/components/drills/DrillCard
// Placeholder onClick handler - Story 3.1 will implement DrillDetail sheet

/**
 * Success State Component Props
 */
export interface SuccessStateProps {
  drills: ContentItem[];
}

/**
 * Success State Component
 * Displays drill cards in responsive grid layout
 */
function SuccessState({ drills }: SuccessStateProps) {
  if (drills.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {drills.map((drill) => (
        <DrillCard
          key={drill.id}
          drill={drill}
          onClick={() => console.log('Open drill detail (Story 3.1):', drill.id)}
        />
      ))}
    </div>
  );
}

/**
 * Library Page Component
 * Main page for browsing all saved drills with filtering and search capabilities
 * Displays loading state, error handling, empty state, and drill grid
 */
export function Library() {
  const { data, isLoading, isError, refetch } = useContentList();

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-bold font-display text-hockey-blue mb-2">
          Drill Library
        </h1>
        <p className="text-rink-gray">
          Browse and access your collection of saved drills
        </p>
      </div>

      {isLoading && <LoadingState />}
      {isError && <ErrorState onRetry={() => refetch()} />}
      {data && <SuccessState drills={data.items} />}
    </div>
  );
}
