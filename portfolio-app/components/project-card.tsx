'use client';

import { motion } from 'framer-motion';

interface Project {
  title: string;
  description: string;
  tags: string[];
}

interface ProjectCardProps {
  project: Project;
  index: number;
}

export function ProjectCard({ project, index }: ProjectCardProps) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.55, delay: index * 0.12 }}
      className="group rounded-[2rem] border border-slate-200/80 bg-white p-7 shadow-soft transition hover:-translate-y-1 hover:shadow-xl dark:border-slate-800/80 dark:bg-slate-950"
    >
      <div className="mb-5 flex items-center justify-between gap-3 text-slate-500 dark:text-slate-400">
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.35em] text-slate-700 dark:bg-slate-900 dark:text-slate-300">Project</span>
        <span className="text-xs">Featured</span>
      </div>
      <h3 className="text-2xl font-semibold text-slate-950 dark:text-white">{project.title}</h3>
      <p className="mt-4 text-sm leading-7 text-slate-600 dark:text-slate-300">{project.description}</p>
      <div className="mt-6 flex flex-wrap gap-2">
        {project.tags.map((tag) => (
          <span key={tag} className="rounded-full border border-slate-200 px-3 py-1 text-xs text-slate-600 dark:border-slate-700 dark:text-slate-300">
            {tag}
          </span>
        ))}
      </div>
      <div className="mt-8 flex items-center gap-2 text-sm font-semibold text-slate-900 transition group-hover:text-slate-700 dark:text-slate-100 dark:group-hover:text-slate-300">
        <span>See details</span>
        <span aria-hidden="true">→</span>
      </div>
    </motion.article>
  );
}
