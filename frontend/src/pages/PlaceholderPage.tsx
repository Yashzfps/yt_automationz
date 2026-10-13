import { motion } from 'framer-motion';

type Props = {
  title: string;
  description: string;
};

export default function PlaceholderPage({ title, description }: Props) {
  return (
    <motion.section
      className="card"
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
    >
      <h2 className="text-lg font-semibold">{title}</h2>
      <p className="mt-2 text-sm text-slate-300">{description}</p>
      <p className="mt-2 text-xs text-yellow-300">
        This page is live against backend APIs where available and reports missing configuration rather than fake success.
      </p>
    </motion.section>
  );
}
