export default function clsx(...items: Array<string | undefined | false>) {
  return items.filter(Boolean).join(' ');
}
