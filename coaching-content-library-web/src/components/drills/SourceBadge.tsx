import type { ContentSource } from '@/lib/types';
import { cn } from '@/lib/utils';
import { Video, MessageSquare, Instagram, Music } from 'lucide-react';

export interface SourceBadgeProps {
  source: ContentSource;
}

export function SourceBadge({ source }: SourceBadgeProps) {
  const badgeConfig = {
    YouTube: {
      icon: <Video data-testid="youtube-icon" className="w-3 h-3" />,
      label: 'YouTube',
      className: 'bg-red-600 text-white',
    },
    Reddit: {
      icon: <MessageSquare data-testid="reddit-icon" className="w-3 h-3" />,
      label: 'Reddit',
      className: 'bg-orange-500 text-white',
    },
    Instagram: {
      icon: <Instagram data-testid="instagram-icon" className="w-3 h-3" />,
      label: 'Instagram',
      className: 'bg-pink-500 text-white',
    },
    TikTok: {
      icon: <Music data-testid="tiktok-icon" className="w-3 h-3" />,
      label: 'TikTok',
      className: 'bg-black text-white',
    },
  };

  const config = badgeConfig[source];

  if (!config) {
    return null;
  }

  return (
    <span
      className={cn(
        'rounded-md px-2 py-1 text-xs flex items-center gap-1',
        config.className
      )}
    >
      {config.icon}
      {config.label}
    </span>
  );
}