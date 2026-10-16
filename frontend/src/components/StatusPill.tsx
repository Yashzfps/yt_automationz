import clsx from '../utils/clsx';

type Props = { status: string };

export default function StatusPill({ status }: Props) {
  return (
    <span
      className={clsx(
        'rounded-full px-2 py-0.5 text-xs uppercase tracking-wider',
        status.includes('fail') ? 'bg-red-500/20 text-red-300' : '',
        status.includes('complete') ? 'bg-emerald-500/20 text-emerald-300' : '',
        status.includes('running') || status.includes('upload') ? 'bg-blue-500/20 text-blue-300' : '',
        status.includes('pending') ? 'bg-yellow-500/20 text-yellow-300' : '',
      )}
    >
      {status}
    </span>
  );
}
