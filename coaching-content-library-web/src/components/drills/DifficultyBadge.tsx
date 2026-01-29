import { cn } from '@/lib/utils';

export interface DifficultyBadgeProps {
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced' | null;
}

export function DifficultyBadge({ difficulty }: DifficultyBadgeProps) {
  if (difficulty === null) {
    return null;
  }

  const badgeConfig = {
    Beginner: {
      label: 'Beginner',
      className: 'bg-green-500 text-white',
    },
    Intermediate: {
      label: 'Intermediate',
      className: 'bg-amber-500 text-white',
    },
    Advanced: {
      label: 'Advanced',
      className: 'bg-red-500 text-white',
    },
  };

  const config = badgeConfig[difficulty];

  if (!config) {
    return null;
  }

  return (
    <span
      className={cn(
        'rounded-md px-2 py-1 text-xs',
        config.className
      )}
    >
      {config.label}
    </span>
  );
}