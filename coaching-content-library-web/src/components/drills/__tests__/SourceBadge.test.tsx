import { render, screen } from '@testing-library/react';
import { SourceBadge } from '../SourceBadge';

describe('SourceBadge', () => {
  it('renders YouTube badge with correct text and icon', () => {
    render(<SourceBadge source="YouTube" />);
    expect(screen.getByText('YouTube')).toBeInTheDocument();
    expect(screen.getByTestId('youtube-icon')).toBeInTheDocument();
  });

  it('renders Reddit badge with correct text and icon', () => {
    render(<SourceBadge source="Reddit" />);
    expect(screen.getByText('Reddit')).toBeInTheDocument();
    expect(screen.getByTestId('reddit-icon')).toBeInTheDocument();
  });

  it('renders Instagram badge with correct text and icon', () => {
    render(<SourceBadge source="Instagram" />);
    expect(screen.getByText('Instagram')).toBeInTheDocument();
    expect(screen.getByTestId('instagram-icon')).toBeInTheDocument();
  });

  it('renders TikTok badge with correct text and icon', () => {
    render(<SourceBadge source="TikTok" />);
    expect(screen.getByText('TikTok')).toBeInTheDocument();
    expect(screen.getByTestId('tiktok-icon')).toBeInTheDocument();
  });
});
