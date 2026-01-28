import type { ContentItem } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

export interface SourceBadgeProps {
  source: ContentItem['source'];
}

export function SourceBadge({ source }: SourceBadgeProps) {
  // Temporary colors - Story 2.4 will enhance with brand colors and icons
  const getSourceColor = () => {
    switch (source) {
      case 'YouTube':
        return 'bg-red-600 text-white hover:bg-red-700';
      case 'Reddit':
        return 'bg-orange-500 text-white hover:bg-orange-600';
      case 'Instagram':
        return 'bg-pink-500 text-white hover:bg-pink-600';
      case 'TikTok':
        return 'bg-black text-white hover:bg-gray-900';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  return (
    <Badge className={cn('text-xs', getSourceColor())}>
      {source}
    </Badge>
  );
}
