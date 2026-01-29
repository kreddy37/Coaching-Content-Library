import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { EmptyState } from '../EmptyState';
import { FolderOpen } from 'lucide-react';

describe('EmptyState', () => {
  it('renders with required props', () => {
    render(<EmptyState title="No Items" message="The list is empty." />);
    expect(screen.getByText('No Items')).toBeInTheDocument();
    expect(screen.getByText('The list is empty.')).toBeInTheDocument();
  });

  it('renders with all optional props', () => {
    const onAction = vi.fn();
    const customIcon = <FolderOpen data-testid="custom-icon" />;

    render(
      <EmptyState
        title="No Items"
        message="Empty"
        actionLabel="Add Item"
        onAction={onAction}
        icon={customIcon}
      />
    );

    expect(screen.getByText('No Items')).toBeInTheDocument();
    expect(screen.getByText('Empty')).toBeInTheDocument();
    expect(screen.getByText('Add Item')).toBeInTheDocument();
    expect(screen.getByTestId('custom-icon')).toBeInTheDocument();
  });

  it('does not render CTA button when actionLabel is omitted', () => {
    render(<EmptyState title="No Items" message="Empty" />);
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('calls onClick handler when CTA button is clicked', () => {
    const onAction = vi.fn();

    render(
      <EmptyState
        title="No Items"
        message="Empty"
        actionLabel="Add Item"
        onAction={onAction}
      />
    );

    const button = screen.getByText('Add Item');
    fireEvent.click(button);
    expect(onAction).toHaveBeenCalledTimes(1);
  });

  it('renders custom icon when provided', () => {
    const customIcon = <div data-testid="custom-icon">Custom</div>;

    render(
      <EmptyState
        title="No Items"
        message="Empty"
        icon={customIcon}
      />
    );

    expect(screen.getByTestId('custom-icon')).toBeInTheDocument();
  });

  it('renders default FolderOpen icon when no icon prop provided', () => {
    const { container } = render(
      <EmptyState title="No Items" message="Empty" />
    );

    // Lucide icons render as SVG
    const svg = container.querySelector('svg');
    expect(svg).toBeInTheDocument();
  });

  it('applies correct layout classes for centering and spacing', () => {
    const { container } = render(
      <EmptyState title="No Items" message="Empty" />
    );

    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper).toHaveClass('flex');
    expect(wrapper).toHaveClass('flex-col');
    expect(wrapper).toHaveClass('items-center');
    expect(wrapper).toHaveClass('justify-center');
    expect(wrapper).toHaveClass('gap-4');
  });

  it('renders with custom button variant', () => {
    render(
      <EmptyState
        title="No Items"
        message="Empty"
        actionLabel="Add Item"
        buttonVariant="outline"
      />
    );

    const button = screen.getByRole('button');
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent('Add Item');
  });

  it('applies responsive text sizing', () => {
    const { container } = render(
      <EmptyState title="No Items" message="Empty" />
    );

    const title = screen.getByText('No Items');
    expect(title).toHaveClass('text-2xl');
    expect(title).toHaveClass('md:text-3xl');

    const message = screen.getByText('Empty');
    expect(message).toHaveClass('text-sm');
    expect(message).toHaveClass('md:text-base');
  });

  it('has accessibility attributes', () => {
    const { container } = render(
      <EmptyState title="No Items" message="Empty" />
    );

    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper).toHaveAttribute('role', 'status');
    expect(wrapper).toHaveAttribute('aria-live', 'polite');
  });

  it('handles errors in onAction callback gracefully', () => {
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const onAction = vi.fn(() => {
      throw new Error('Test error');
    });

    render(
      <EmptyState
        title="No Items"
        message="Empty"
        actionLabel="Add Item"
        onAction={onAction}
      />
    );

    const button = screen.getByText('Add Item');
    fireEvent.click(button);

    expect(onAction).toHaveBeenCalledTimes(1);
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      'Error in EmptyState action handler:',
      expect.any(Error)
    );

    consoleErrorSpy.mockRestore();
  });
});
