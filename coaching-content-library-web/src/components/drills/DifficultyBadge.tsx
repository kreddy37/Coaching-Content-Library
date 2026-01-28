import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

export interface DifficultyBadgeProps {
  difficulty: string | null;
}

export function DifficultyBadge({ difficulty }: DifficultyBadgeProps) {
  if (!difficulty) return null;

  // Temporary colors - Story 2.4 will enhance with icons
  const getDifficultyColor = () => {
    const lower = difficulty.toLowerCase();
    if (lower === 'beginner') {
      return 'bg-green-500 text-white hover:bg-green-600';
    }
    if (lower === 'intermediate') {
      return 'bg-amber-500 text-white hover:bg-amber-600';
    }
    if (lower === 'advanced') {
      return 'bg-red-500 text-white hover:bg-red-600';
    }
    return 'bg-gray-500 text-white';
  };

  return (
    <Badge className={cn('text-xs', getDifficultyColor())}>
      {difficulty}
    </Badge>
  );
}
