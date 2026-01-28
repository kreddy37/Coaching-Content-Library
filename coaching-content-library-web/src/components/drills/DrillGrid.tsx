import React from 'react';

export interface DrillGridProps {
  children: React.ReactNode;
}

export function DrillGrid({ children }: DrillGridProps) {
  return (
    <div
      data-testid="drill-grid"
      className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3 xl:grid-cols-4"
    >
      {children}
    </div>
  );
}
