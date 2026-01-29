import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { FolderOpen } from 'lucide-react';

export interface EmptyStateProps {
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
  icon?: React.ReactNode;
  buttonVariant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
}

export function EmptyState({
  title,
  message,
  actionLabel,
  onAction,
  icon,
  buttonVariant = 'default',
}: EmptyStateProps): JSX.Element {
  const handleAction = () => {
    try {
      onAction?.();
    } catch (error) {
      console.error('Error in EmptyState action handler:', error);
    }
  };

  return (
    <div role="status" aria-live="polite" className="flex flex-col items-center justify-center gap-4 min-h-[400px] px-4 py-8 md:py-12 text-center">
      {/* Icon */}
      {icon || <FolderOpen className="w-20 h-20 text-ice-blue" />}

      {/* Title */}
      <h2 className="text-2xl font-bold text-hockey-blue md:text-3xl">{title}</h2>

      {/* Message */}
      <p className="text-gray-600 text-sm md:text-base max-w-md">{message}</p>

      {/* Optional CTA Button */}
      {actionLabel && (
        <Button onClick={handleAction} variant={buttonVariant}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
}
