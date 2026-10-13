import { useEffect, useMemo, useState } from 'react';
import { addSource, createBatch, listAssets, listSources, scan } from '../api/rinApi';
import type { Asset, SourceConfig } from '../types';
import StatusPill from '../components/StatusPill';

export default function LibraryPage() {
  const [sources, setSources] = useState<SourceConfig[]>([]);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [path, setPath] = useState('');
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState<number[]>([]);
  const [message, setMessage] = useState('');

  async function refresh() {
    const [src, vid] = await Promise.all([listSources(), listAssets()]);
    setSources(src);
    setAssets(vid);
  }

  useEffect(() => {
    refresh().catch((e) => setMessage(String(e)));
  }, []);

  const filtered = useMemo(
    () => assets.filter((a) => a.file_name.toLowerCase().includes(query.toLowerCase())),
    [assets, query],
  );

  return (
    <div className="grid gap-4">
      <section className="card space-y-2">
        <h2 className="text-lg font-semibold">Folder Sources</h2>
        <div className="flex gap-2">
          <input
            value={path}
            onChange={(e) => setPath(e.target.value)}
            placeholder="C:\\Videos\\Shorts"
            className="w-full rounded bg-slate-900 p-2"
          />
          <button
            onClick={async () => {
              const source = await addSource(path, true);
              setSources((prev) => [source, ...prev]);
              setPath('');
            }}
            className="rounded bg-violet-600 px-4 py-2"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2 text-xs">
          {sources.map((s) => (
            <button
              key={s.id}
              onClick={async () => {
                await scan([s.id]);
                await refresh();
              }}
              className="rounded border border-slate-600 px-2 py-1"
            >
              Scan {s.path}
            </button>
          ))}
        </div>
      </section>

      <section className="card space-y-2">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Video Library</h2>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search videos"
            className="rounded bg-slate-900 p-2 text-sm"
          />
        </div>
        <p className="text-xs text-slate-400">
          Batch confirmation policy: verify source paths, quantity, captions mode, burn-in/SRT, metadata and upload mode before processing.
        </p>
        <div className="space-y-2">
          {filtered.map((asset) => (
            <label key={asset.id} className="flex items-center justify-between rounded bg-slate-900/50 p-2 text-sm">
              <span className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={selected.includes(asset.id)}
                  onChange={(e) => {
                    setSelected((prev) =>
                      e.target.checked ? [...prev, asset.id] : prev.filter((id) => id !== asset.id),
                    );
                  }}
                />
                {asset.file_name}
              </span>
              <span className="flex items-center gap-2">
                <StatusPill status={asset.valid ? 'valid' : 'invalid'} />
                <StatusPill status={asset.approval_state} />
              </span>
            </label>
          ))}
          {filtered.length === 0 && <p className="text-slate-400">No videos discovered yet.</p>}
        </div>

        <button
          onClick={async () => {
            if (selected.length === 0) return;
            const qty = Number(prompt('Process how many selected videos?', String(selected.length)) ?? selected.length);
            if (!qty || qty < 1) return;
            if (!confirm('Confirm batch: Roman Hinglish captions + SRT + metadata generation enabled.')) return;
            const job = await createBatch(selected, qty);
            setMessage(`Started job #${job.id}`);
          }}
          className="rounded bg-blue-600 px-4 py-2"
        >
          Process Selected
        </button>
        {message && <p className="text-sm text-emerald-300">{message}</p>}
      </section>
    </div>
  );
}
