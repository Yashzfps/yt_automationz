import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './index.css';
import AppLayout from './layouts/AppLayout';
import LibraryPage from './pages/LibraryPage';
import OverviewPage from './pages/OverviewPage';
import PlaceholderPage from './pages/PlaceholderPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<OverviewPage />} />
          <Route path="library" element={<LibraryPage />} />
          <Route path="captions" element={<PlaceholderPage title="Caption Studio" description="Edit generated Roman Hinglish captions and inspect SRT export diagnostics." />} />
          <Route path="metadata" element={<PlaceholderPage title="AI Metadata" description="Review title options, description, hashtags, tags and approve metadata before upload." />} />
          <Route path="queue" element={<PlaceholderPage title="Upload Queue" description="Track resumable uploads, retries, failures and duplicate-prevention reconciliation." />} />
          <Route path="schedule" element={<PlaceholderPage title="Schedule Calendar" description="Preview timezone-aware planned publish slots with interval and daily limits." />} />
          <Route path="published" element={<PlaceholderPage title="Published Videos" description="Audit successful YouTube IDs and post-upload verification history." />} />
          <Route path="history" element={<PlaceholderPage title="History and Logs" description="Inspect structured logs, workflow errors and restart recovery events." />} />
          <Route path="settings" element={<PlaceholderPage title="Settings" description="Configure sources, local models, Ollama and YouTube OAuth diagnostics." />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
