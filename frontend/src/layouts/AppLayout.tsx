import { Link, Outlet, useLocation } from 'react-router-dom';
import { Film, LayoutDashboard, MessageSquareText, UploadCloud, Settings, CalendarDays, BookCheck, History, Library } from 'lucide-react';
import clsx from '../utils/clsx';

const nav = [
  { to: '/', icon: LayoutDashboard, label: 'Overview' },
  { to: '/library', icon: Library, label: 'Video Library' },
  { to: '/captions', icon: MessageSquareText, label: 'Caption Studio' },
  { to: '/metadata', icon: BookCheck, label: 'AI Metadata' },
  { to: '/queue', icon: UploadCloud, label: 'Upload Queue' },
  { to: '/schedule', icon: CalendarDays, label: 'Schedule Calendar' },
  { to: '/published', icon: Film, label: 'Published Videos' },
  { to: '/history', icon: History, label: 'History and Logs' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

export default function AppLayout() {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-surface to-black text-slate-100">
      <div className="mx-auto grid max-w-[1400px] grid-cols-[260px_1fr] gap-4 p-4">
        <aside className="card sticky top-4 h-[calc(100vh-2rem)] overflow-y-auto">
          <h1 className="mb-4 text-xl font-bold tracking-widest text-violet-300">RIN STUDIO</h1>
          <nav className="space-y-2">
            {nav.map(({ to, icon: Icon, label }) => (
              <Link
                key={to}
                to={to}
                className={clsx(
                  'flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition',
                  location.pathname === to ? 'bg-violet-500/20 text-violet-200' : 'hover:bg-slate-800/80',
                )}
              >
                <Icon size={16} />
                {label}
              </Link>
            ))}
          </nav>
          <p className="mt-4 rounded-lg border border-violet-500/30 bg-violet-500/10 p-2 text-xs text-violet-200">
            Demo Mode is explicitly marked in pages and never publishes real videos.
          </p>
        </aside>
        <main className="space-y-4">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
