import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { DrillGrid } from '../DrillGrid';
import { ContentItem } from '@/lib/types';

// Mock the DrillCard component to isolate the DrillGrid tests
vi.mock('@/components/drills/DrillCard', () => ({
  DrillCard: ({ drill }: { drill: ContentItem }) => <div data-testid="drill-card">{drill.title}</div>,
}));

const mockDrills: ContentItem[] = [
  { id: 1, title: 'Drill 1' } as ContentItem,
  { id: 2, title: 'Drill 2' } as ContentItem,
];

describe('DrillGrid', () => {
  it('renders the correct number of drill cards', () => {
    render(<DrillGrid drills={mockDrills} />);
    const drillCards = screen.getAllByTestId('drill-card');
    expect(drillCards).toHaveLength(mockDrills.length);
  });
});
