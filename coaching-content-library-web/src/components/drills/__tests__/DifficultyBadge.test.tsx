import { render, screen } from '@testing-library/react';
import { DifficultyBadge } from '../DifficultyBadge';

describe('DifficultyBadge', () => {
  it('renders beginner badge with correct text and color', () => {
    render(<DifficultyBadge difficulty="Beginner" />);
    const badge = screen.getByText('Beginner');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-green-500');
  });

  it('renders intermediate badge with correct text and color', () => {
    render(<DifficultyBadge difficulty="Intermediate" />);
    const badge = screen.getByText('Intermediate');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-amber-500');
  });

  it('renders advanced badge with correct text and color', () => {
    render(<DifficultyBadge difficulty="Advanced" />);
    const badge = screen.getByText('Advanced');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-red-500');
  });

  it('returns null when difficulty is null', () => {
    const { container } = render(<DifficultyBadge difficulty={null} />);
    expect(container.firstChild).toBeNull();
  });
});
