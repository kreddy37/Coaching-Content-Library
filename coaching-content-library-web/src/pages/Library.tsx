import { useContentList } from '@/hooks/useContentList';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { DrillCard } from '@/components/drills/DrillCard';
import type { ContentItem } from '@/lib/types';
import { DrillGrid } from '@/components/drills/DrillGrid';

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

// Placeholder onClick handler - Story 3.1 will implement DrillDetail sheet
const handleDrillClick = (drill: ContentItem) => {
  // To be implemented in Story 3.1
  console.log('Clicked drill:', drill.id);
};

/**
 * Library Page Component
 * Main page for browsing all saved drills with filtering and search capabilities
 * Displays loading state, error handling, empty state, and drill grid
 */
export function Library() {
  const { data, isLoading, isError, refetch } = useContentList();

  const renderContent = () => {
    if (isError) {
      return <ErrorState onRetry={() => refetch()} />;
    }

    if (isLoading) {
      return (
        <DrillGrid>
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
        </DrillGrid>
      );
    }

    if (data) {
      if (data.items.length === 0) {
        return <EmptyState />;
      }
      return (
        <DrillGrid>
          {data.items.map((drill) => (
            <DrillCard key={drill.id} drill={drill} onClick={() => handleDrillClick(drill)} />
          ))}
        </DrillGrid>
      );
    }

    return null;
  };

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
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        {renderContent()}
      </div>
    </div>
  );
}
