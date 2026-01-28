import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { DrillCard } from '../DrillCard';
import type { ContentItem } from '@/lib/types';

describe('DrillCard', () => {
  const mockOnClick = vi.fn();

  const mockYouTubeDrill: ContentItem = {
    id: 1,
    source: 'YouTube',
    content_type: 'Video',
    url: 'https://youtube.com/watch?v=test',
    title: 'Butterfly Recovery Drill',
    author: 'Coach Mike',
    thumbnail_url: 'https://example.com/thumb.jpg',
    drill_description: 'Test description',
    drill_tags: ['butterfly', 'recovery'],
    published_at: '2024-01-01T00:00:00Z',
    created_at: '2024-01-01T00:00:00Z',
    difficulty: 'Intermediate',
  };

  const mockInstagramDrill: ContentItem = {
    ...mockYouTubeDrill,
    id: 2,
    source: 'Instagram',
    thumbnail_url: null,
    title: 'Glove Save Technique',
  };

  const mockTikTokDrill: ContentItem = {
    ...mockYouTubeDrill,
    id: 3,
    source: 'TikTok',
    thumbnail_url: null,
    title: 'Quick Reflexes Training',
  };

  afterEach(() => {
    mockOnClick.mockClear();
  });

  describe('Component Structure and Accessibility', () => {
    it('renders DrillCard component with required props', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      expect(screen.getByText('Butterfly Recovery Drill')).toBeInTheDocument();
    });

    it('applies hover classes for interactivity', () => {
      const { container } = render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const card = container.firstChild as HTMLElement;
      expect(card).toHaveClass('cursor-pointer');
      expect(card).toHaveClass('transition-all');
    });

    it('calls onClick when card is clicked', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const card = screen.getByRole('button', { name: /Butterfly Recovery Drill/i });
      fireEvent.click(card);
      expect(mockOnClick).toHaveBeenCalledTimes(1);
    });

    it('is keyboard accessible and calls onClick on Enter key', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const card = screen.getByRole('button', { name: /Butterfly Recovery Drill/i });
      card.focus();
      fireEvent.keyDown(card, { key: 'Enter', code: 'Enter' });
      expect(mockOnClick).toHaveBeenCalledTimes(1);
    });

    it('is keyboard accessible and calls onClick on Space key', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const card = screen.getByRole('button', { name: /Butterfly Recovery Drill/i });
      card.focus();
      fireEvent.keyDown(card, { key: ' ', code: 'Space' });
      expect(mockOnClick).toHaveBeenCalledTimes(1);
    });
  });

  describe('Thumbnail Display', () => {
    it('renders thumbnail image when thumbnail_url exists', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const img = screen.getByAltText('Butterfly Recovery Drill');
      expect(img).toBeInTheDocument();
      expect(img).toHaveAttribute('src', 'https://example.com/thumb.jpg');
      expect(img).toHaveAttribute('loading', 'lazy');
    });

    it('applies correct image classes for aspect ratio and styling', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const img = screen.getByAltText('Butterfly Recovery Drill');
      expect(img).toHaveClass('object-cover');
      expect(img).toHaveClass('aspect-video');
      expect(img).toHaveClass('w-full');
    });

    it('uses title as alt text when title exists', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      expect(screen.getByAltText('Butterfly Recovery Drill')).toBeInTheDocument();
    });

    it('uses fallback alt text when title is null', () => {
      const drillNoTitle = { ...mockYouTubeDrill, title: null };
      render(<DrillCard drill={drillNoTitle} onClick={mockOnClick} />);
      expect(screen.getByAltText('Drill thumbnail')).toBeInTheDocument();
    });
  });

  describe('Instagram Placeholder', () => {
    it('renders Instagram placeholder when source is Instagram and no thumbnail', () => {
      render(<DrillCard drill={mockInstagramDrill} onClick={mockOnClick} />);
      // Check for gradient background div
      const { container } = render(<DrillCard drill={mockInstagramDrill} onClick={mockOnClick} />);
      const placeholder = container.querySelector('.bg-gradient-to-br');
      expect(placeholder).toBeInTheDocument();
    });

    it('displays Instagram icon in placeholder', () => {
      const { container } = render(<DrillCard drill={mockInstagramDrill} onClick={mockOnClick} />);
      // Lucide icons render as SVG with specific attributes
      const icon = container.querySelector('svg');
      expect(icon).toBeInTheDocument();
    });
  });

  describe('TikTok Placeholder', () => {
    it('renders TikTok placeholder when source is TikTok and no thumbnail', () => {
      const { container } = render(<DrillCard drill={mockTikTokDrill} onClick={mockOnClick} />);
      const placeholder = container.querySelector('.bg-black');
      expect(placeholder).toBeInTheDocument();
    });

    it('displays Music icon in TikTok placeholder', () => {
      const { container } = render(<DrillCard drill={mockTikTokDrill} onClick={mockOnClick} />);
      const icon = container.querySelector('svg');
      expect(icon).toBeInTheDocument();
    });
  });

  describe('Metadata Display', () => {
    it('renders drill title with proper truncation classes', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const title = screen.getByText('Butterfly Recovery Drill');
      expect(title).toHaveClass('line-clamp-2');
      expect(title).toHaveClass('font-semibold');
    });

    it('renders author name when available', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      expect(screen.getByText('Coach Mike')).toBeInTheDocument();
    });

    it('does not render author section when author is null', () => {
      const drillNoAuthor = { ...mockYouTubeDrill, author: null };
      render(<DrillCard drill={drillNoAuthor} onClick={mockOnClick} />);
      expect(screen.queryByText('Coach Mike')).not.toBeInTheDocument();
    });

    it('renders SourceBadge component', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      // SourceBadge will display the source
      expect(screen.getByText(/YouTube/i)).toBeInTheDocument();
    });

    it('renders DifficultyBadge when difficulty exists', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      expect(screen.getByText('Intermediate')).toBeInTheDocument();
    });

    it('does not render DifficultyBadge when difficulty is null', () => {
      const drillNoDifficulty = { ...mockYouTubeDrill, difficulty: null };
      render(<DrillCard drill={drillNoDifficulty} onClick={mockOnClick} />);
      expect(screen.queryByText(/Beginner|Intermediate|Advanced/i)).not.toBeInTheDocument();
    });

    it('renders drill tags when available', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      expect(screen.getByText('butterfly')).toBeInTheDocument();
      expect(screen.getByText('recovery')).toBeInTheDocument();
    });

    it('limits display to first 2 tags (progressive disclosure)', () => {
      const drillManyTags = {
        ...mockYouTubeDrill,
        drill_tags: ['butterfly', 'recovery', 'glove', 'blocker', 'stance'],
      };
      render(<DrillCard drill={drillManyTags} onClick={mockOnClick} />);
      expect(screen.getByText('butterfly')).toBeInTheDocument();
      expect(screen.getByText('recovery')).toBeInTheDocument();
      expect(screen.queryByText('glove')).not.toBeInTheDocument();
    });
  });

  describe('Layout and Styling', () => {
    it('applies correct color to title (hockey-blue)', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const title = screen.getByText('Butterfly Recovery Drill');
      expect(title).toHaveClass('text-hockey-blue');
    });

    it('applies correct text size to author', () => {
      render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const author = screen.getByText('Coach Mike');
      expect(author).toHaveClass('text-sm');
      expect(author).toHaveClass('text-gray-600');
    });

    it('uses flex layout with proper gap for badges', () => {
      const { container } = render(<DrillCard drill={mockYouTubeDrill} onClick={mockOnClick} />);
      const badgeContainer = container.querySelector('.flex.gap-2');
      expect(badgeContainer).toBeInTheDocument();
    });
  });
});
