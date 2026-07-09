'use client';

interface SectionHeadingProps {
  number: string;
  title: string;
  description: string;
}

export function SectionHeading({ number, title, description }: SectionHeadingProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3 text-sm uppercase tracking-[0.35em] text-slate-500 dark:text-slate-400">
        <span className="font-semibold text-slate-900 dark:text-white">{number}</span>
        <span className="h-px flex-1 bg-slate-200 dark:bg-slate-800" />
      </div>
      <div>
        <h2 className="text-3xl font-semibold tracking-tight text-slate-950 dark:text-white sm:text-4xl">{title}</h2>
        <p className="mt-2 max-w-2xl text-sm leading-7 text-slate-600 dark:text-slate-300">{description}</p>
      </div>
    </div>
  );
}
