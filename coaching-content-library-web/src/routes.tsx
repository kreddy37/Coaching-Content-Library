import type { RouteObject } from 'react-router-dom';
import { MainLayout } from '@/components/layout/MainLayout';
import { Home } from '@/pages/Home';
import { Library } from '@/pages/Library';
import { DrillDetail } from '@/pages/DrillDetail';

export const routes: RouteObject[] = [
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: 'library',
        element: <Library />,
      },
      {
        path: 'drill/:id',
        element: <DrillDetail />,
      },
    ],
  },
];
