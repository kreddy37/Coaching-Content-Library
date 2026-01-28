import { Link } from 'react-router-dom';

export function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen px-4 py-12 bg-gradient-to-br from-glacier-white to-white">
      {/* Hero Section Container - Responsive */}
      <div className="w-full max-w-3xl mx-auto space-y-8 text-center">
        {/* Main Heading */}
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold font-display text-hockey-blue leading-tight">
          Coaching Content Library
        </h1>

        {/* Hero Description */}
        <p className="text-lg md:text-xl font-body text-rink-gray max-w-2xl mx-auto">
          Organize and discover hockey goalie drills from YouTube, Reddit, Instagram, and TikTok
        </p>

        {/* Divider */}
        <div className="h-1 w-16 bg-ice-blue mx-auto rounded-full" />

        {/* Empty State Section */}
        <div className="bg-white rounded-lg shadow-sm p-8 md:p-12 border border-gray-200">
          <div className="space-y-6">
            {/* Empty State Icon */}
            <div className="text-6xl text-ice-blue">📚</div>

            {/* Empty State Message */}
            <h2 className="text-2xl font-semibold text-hockey-blue font-display">
              Your drill library is empty
            </h2>

            <p className="text-base md:text-lg text-rink-gray max-w-xl mx-auto">
              Start by adding drills via the Discord bot or web interface.
            </p>

            {/* CTA Button */}
            <div className="pt-4">
              <Link
                to="/library"
                className="inline-block px-8 py-3 bg-ice-blue hover:bg-blue-400 text-white font-semibold rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-ice-blue focus:ring-offset-2"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
