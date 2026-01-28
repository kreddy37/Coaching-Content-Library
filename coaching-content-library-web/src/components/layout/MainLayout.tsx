import { Outlet, Link, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { cn } from '@/lib/utils';

export interface MainLayoutProps {}

export function MainLayout() {
  const [isNavOpen, setIsNavOpen] = useState(false);
  const location = useLocation();

  // Close mobile menu on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isNavOpen) {
        setIsNavOpen(false);
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isNavOpen]);

  return (
    <div className="min-h-screen flex flex-col bg-glacier-white">
      {/* Header */}
      <header className="bg-hockey-blue text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold font-display">Coaching Content Library</h1>

            {/* Mobile menu button */}
            <button
              onClick={() => setIsNavOpen(!isNavOpen)}
              className="md:hidden inline-flex items-center justify-center p-2 rounded-md hover:bg-ice-blue/20 focus:outline-none focus:ring-2 focus:ring-ice-blue focus:ring-offset-2 focus:ring-offset-hockey-blue"
              aria-label="Toggle navigation menu"
              aria-expanded={isNavOpen}
            >
              <svg
                className={cn('h-6 w-6 transition-transform', isNavOpen && 'rotate-180')}
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M4 6h16M4 12h16M4 18h16"></path>
              </svg>
            </button>
          </div>

          {/* Navigation - Desktop */}
          <nav className="hidden md:flex mt-4 space-x-8">
            <Link
              to="/"
              className="font-body text-white hover:text-ice-blue transition-colors focus:outline-none focus:ring-2 focus:ring-ice-blue focus:rounded px-2 py-1"
              aria-current={location.pathname === '/' ? 'page' : undefined}
            >
              Home
            </Link>
            <Link
              to="/library"
              className="font-body text-white hover:text-ice-blue transition-colors focus:outline-none focus:ring-2 focus:ring-ice-blue focus:rounded px-2 py-1"
              aria-current={location.pathname === '/library' ? 'page' : undefined}
            >
              Library
            </Link>
          </nav>

          {/* Navigation - Mobile */}
          {isNavOpen && (
            <nav className="md:hidden mt-4 space-y-2 pb-4">
              <Link
                to="/"
                className="block font-body text-white hover:text-ice-blue transition-colors focus:outline-none focus:ring-2 focus:ring-ice-blue focus:rounded px-2 py-2"
                onClick={() => setIsNavOpen(false)}
                aria-current={location.pathname === '/' ? 'page' : undefined}
              >
                Home
              </Link>
              <Link
                to="/library"
                className="block font-body text-white hover:text-ice-blue transition-colors focus:outline-none focus:ring-2 focus:ring-ice-blue focus:rounded px-2 py-2"
                onClick={() => setIsNavOpen(false)}
                aria-current={location.pathname === '/library' ? 'page' : undefined}
              >
                Library
              </Link>
            </nav>
          )}
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-rink-gray text-white mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm">
            © 2026 Coaching Content Library. Built for hockey coaches.
          </p>
        </div>
      </footer>
    </div>
  );
}
