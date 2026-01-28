import type { ContentItem } from '@/lib/types';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Instagram, Music } from 'lucide-react';
import { SourceBadge } from './SourceBadge';
import { DifficultyBadge } from './DifficultyBadge';
import { cn } from '@/lib/utils';
import React from 'react';

export interface DrillCardProps {
  drill: ContentItem;
  onClick: () => void;
  showRelevance?: boolean;
  relevanceReason?: string;
  variant?: 'standard' | 'compact';
}

export function DrillCard({ drill, onClick }: DrillCardProps) {
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' || event.key === ' ') {
      onClick();
    }
  };

  const renderThumbnail = () => {
    // YouTube/Reddit - real thumbnail
    if (drill.thumbnail_url) {
      return (
        <img
          src={drill.thumbnail_url}
          alt={drill.title || 'Drill thumbnail'}
          className="w-full aspect-video object-cover rounded-t-lg"
          loading="lazy"
        />
      );
    }

    // Instagram placeholder
    if (drill.source === 'Instagram') {
      return (
        <div className={cn('w-full aspect-video flex items-center justify-center rounded-t-lg', 'bg-gradient-to-br from-pink-400 to-purple-500')}>
          <Instagram className="w-12 h-12 text-white" />
        </div>
      );
    }

    // TikTok placeholder
    if (drill.source === 'TikTok') {
      return (
        <div className={cn('w-full aspect-video flex items-center justify-center rounded-t-lg', 'bg-black')}>
          <Music className="w-12 h-12 text-cyan-400" />
        </div>
      );
    }

    // Fallback for other sources without thumbnail
    return (
      <div className="w-full aspect-video bg-gray-200 flex items-center justify-center rounded-t-lg">
        <span className="text-gray-400 text-sm">No thumbnail</span>
      </div>
    );
  };

  // Limit to first 2 tags (progressive disclosure)
  const displayTags = drill.drill_tags?.slice(0, 2) || [];

  return (
    <Card
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={handleKeyDown}
      className={cn(
        'cursor-pointer transition-all duration-250 hover:scale-[1.02] hover:shadow-lg',
        'border-hockey-blue-200 hover:border-ice-blue-400'
      )}
    >
      {renderThumbnail()}

      <CardContent className="p-4">
        <h3 className="text-hockey-blue font-semibold text-base line-clamp-2 mb-2">
          {drill.title}
        </h3>

        {drill.author && (
          <p className="text-gray-600 text-sm truncate mb-3">
            {drill.author}
          </p>
        )}

        <div className="flex flex-wrap gap-2">
          <SourceBadge source={drill.source} />
          {drill.difficulty && <DifficultyBadge difficulty={drill.difficulty} />}
          {displayTags.map((tag, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
