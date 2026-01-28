import type { ContentItem } from '@/lib/types';
import { DrillCard } from './DrillCard';

export interface DrillGridProps {
  drills: ContentItem[];
}

export function DrillGrid({ drills }: DrillGridProps) {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3 xl:grid-cols-4 max-w-7xl mx-auto px-4 md:px-6">
      {drills.map((drill) => (
        <DrillCard key={drill.id} drill={drill} onClick={() => {}} />
      ))}
    </div>
  );
}
