import { useEffect, useState } from 'react';
import { getDiagnostics, listJobs } from '../api/rinApi';
import StatusPill from '../components/StatusPill';

export default function OverviewPage() {
  const [diag, setDiag] = useState<any>(null);
  const [jobs, setJobs] = useState<any[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([getDiagnostics(), listJobs()])
      .then(([d, j]) => {
        setDiag(d);
        setJobs(j);
      })
      .catch((e) => setError(e?.response?.data?.detail ?? String(e)));
  }, []);

  return (
    <div className="grid gap-4">
      <section className="card">
        <h2 className="mb-2 text-lg font-semibold">System Diagnostics</h2>
        {error && <p className="text-red-300">{error}</p>}
        {!diag && !error && <p>Loading diagnostics…</p>}
        {diag && (
          <div className="grid grid-cols-2 gap-2 text-sm">
            {Object.entries(diag).map(([k, v]) => (
              <div key={k} className="rounded bg-slate-900/50 p-2">
                <p className="text-slate-400">{k}</p>
                <p className="font-medium">{String(v)}</p>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="card">
        <h2 className="mb-2 text-lg font-semibold">Workflow Jobs</h2>
        <div className="space-y-2">
          {jobs.map((job) => (
            <div key={job.id} className="flex items-center justify-between rounded bg-slate-900/50 p-2 text-sm">
              <span>#{job.id} · {job.kind} · {job.stage}</span>
              <StatusPill status={job.status} />
            </div>
          ))}
          {jobs.length === 0 && <p className="text-slate-400">No jobs yet.</p>}
        </div>
      </section>
    </div>
  );
}
