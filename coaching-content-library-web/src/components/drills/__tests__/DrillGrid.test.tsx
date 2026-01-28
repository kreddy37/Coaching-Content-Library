import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { DrillGrid } from '../DrillGrid';

const mockChildren = [
  <div key="1" data-testid="mock-child">Child 1</div>,
  <div key="2" data-testid="mock-child">Child 2</div>,
];

describe('DrillGrid', () => {
  it('renders its children correctly', () => {
    render(<DrillGrid>{mockChildren}</DrillGrid>);
    const renderedChildren = screen.getAllByTestId('mock-child');
    expect(renderedChildren).toHaveLength(mockChildren.length);
    expect(screen.getByText('Child 1')).toBeInTheDocument();
    expect(screen.getByText('Child 2')).toBeInTheDocument();
  });

  it('applies all responsive grid classes', () => {
    render(<DrillGrid>{mockChildren}</DrillGrid>);
    const gridElement = screen.getByTestId('drill-grid');
    const classes = gridElement.className;

    expect(classes).toContain('grid');
    expect(classes).toContain('grid-cols-1');
    expect(classes).toContain('md:grid-cols-2');
    expect(classes).toContain('lg:grid-cols-3');
    expect(classes).toContain('xl:grid-cols-4');
  });
});
