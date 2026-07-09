import { ContactForm } from '../components/contact-form';
import { ThemeToggle } from '../components/theme-toggle';
import { ProjectCard } from '../components/project-card';
import { SectionHeading } from '../components/section-heading';
import { motion } from 'framer-motion';
import { ArrowRight, Mail, MapPin, Briefcase, Sparkles } from 'lucide-react';

const projects = [
  {
    title: 'SaaS Analytics Dashboard',
    description: 'Bespoke dashboard with interactive charts, custom insights, and secure auth flows.',
    tags: ['React', 'Next.js', 'Tailwind', 'Node']
  },
  {
    title: 'E-Commerce Launch',
    description: 'Conversion-first storefront with checkout, inventory sync, and performance tuning.',
    tags: ['Shopify', 'React', 'API', 'Stripe']
  },
  {
    title: 'Portfolio Redesign',
    description: 'Modern branding system, accessibility-first responsive layouts, and motion microinteractions.',
    tags: ['UI/UX', 'Animation', 'SEO', 'Responsive']
  }
];

export default function Home() {
  return (
    <main className="relative mx-auto max-w-6xl px-5 py-10 sm:px-8 lg:px-12">
      <div className="flex flex-col gap-10">
        <section className="grid gap-8 rounded-[2rem] border border-slate-200/80 bg-slate-50/80 p-8 shadow-soft dark:border-slate-800/80 dark:bg-slate-950/50 lg:grid-cols-[1.4fr_0.6fr] lg:items-start">
          <div className="space-y-6">
            <div className="inline-flex items-center gap-3 rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-soft dark:bg-slate-200 dark:text-slate-900">
              <Sparkles className="h-4 w-4" />
              Fullstack developer building polished digital experiences.
            </div>
            <div className="space-y-4">
              <p className="text-sm uppercase tracking-[0.4em] text-slate-500 dark:text-slate-400">Hello, I&apos;m</p>
              <h1 className="text-5xl font-semibold tracking-tight text-slate-950 dark:text-white sm:text-6xl">Alex Morgan</h1>
              <p className="max-w-2xl text-base leading-8 text-slate-700 dark:text-slate-300">
                I create modern web applications with thoughtful interactions, strong performance, and clean user experiences using React, Next.js, and Tailwind CSS.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <a href="#projects" className="btn-primary">View projects</a>
              <a href="#contact" className="btn-secondary">Contact me</a>
            </div>
          </div>
          <div className="rounded-[2rem] border border-slate-200/80 bg-white p-6 shadow-soft dark:border-slate-800/80 dark:bg-slate-900">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm uppercase tracking-[0.35em] text-slate-500 dark:text-slate-400">Experience</p>
                <p className="mt-4 text-3xl font-semibold text-slate-950 dark:text-white">6+ Years</p>
              </div>
              <ThemeToggle />
            </div>
            <div className="mt-8 space-y-4 text-sm text-slate-600 dark:text-slate-300">
              <p className="flex items-center gap-3"><Briefcase className="h-4 w-4" /> Freelance & agency projects</p>
              <p className="flex items-center gap-3"><Mail className="h-4 w-4" /> Design systems, marketing pages, and apps</p>
              <p className="flex items-center gap-3"><MapPin className="h-4 w-4" /> Remote-first collaboration</p>
            </div>
          </div>
        </section>

        <section id="projects" className="space-y-6">
          <SectionHeading number="01" title="Featured work" description="Projects that showcase strong design, technical depth, and polished implementation." />
          <div className="grid gap-6 lg:grid-cols-3">
            {projects.map((project, index) => (
              <ProjectCard key={project.title} project={project} index={index} />
            ))}
          </div>
        </section>

        <section className="grid gap-8 lg:grid-cols-[0.8fr_1.2fr]">
          <div className="section-card">
            <SectionHeading number="02" title="About me" description="I combine design sensibility with engineering reliability to build responsive web products." />
            <div className="mt-6 space-y-5 text-slate-700 dark:text-slate-300">
              <p>
                My focus is building maintainable web apps with fast load times, accessible interactions, and delightful animation. I enjoy working end-to-end across user interfaces, API integrations, and deployment pipelines.
              </p>
              <p>
                Recent work includes scaling dashboards, delivering conversion-focused landing pages, and optimizing performance for long-term growth. I use component-driven workflows and clean code patterns to ship faster.
              </p>
            </div>
          </div>
          <div className="section-card bg-gradient-to-br from-slate-900 via-slate-800 to-slate-950 text-white">
            <div className="space-y-6">
              <div className="inline-flex rounded-full bg-white/10 px-4 py-2 text-sm text-slate-200">What I do</div>
              <div className="grid gap-4">
                <div className="rounded-3xl bg-slate-950/90 p-5">
                  <h3 className="text-xl font-semibold">UI & Product Design</h3>
                  <p className="mt-3 text-sm text-slate-300">Crafting clear visual systems, interactive flows, and accessible responsive layouts.</p>
                </div>
                <div className="rounded-3xl bg-slate-950/90 p-5">
                  <h3 className="text-xl font-semibold">Fullstack Web Apps</h3>
                  <p className="mt-3 text-sm text-slate-300">Building performant Next.js experiences with reusable components and clean state management.</p>
                </div>
                <div className="rounded-3xl bg-slate-950/90 p-5">
                  <h3 className="text-xl font-semibold">Launch & Deployment</h3>
                  <p className="mt-3 text-sm text-slate-300">Shipping production-ready sites with SEO, fast CI/CD, and scalable hosting configurations.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="contact" className="section-card">
          <SectionHeading number="03" title="Let&apos;s build something" description="Reach out for collaborations, freelance projects, or new digital product ideas." />
          <div className="mt-8 grid gap-10 lg:grid-cols-[0.7fr_1.3fr]">
            <div className="rounded-3xl border border-slate-200/80 bg-slate-50 p-8 dark:border-slate-800/80 dark:bg-slate-900">
              <p className="text-sm uppercase tracking-[0.35em] text-slate-500 dark:text-slate-400">Contact</p>
              <div className="mt-6 space-y-4 text-slate-700 dark:text-slate-300">
                <p>Alex Morgan</p>
                <p>Fullstack Developer</p>
                <p>alex@example.com</p>
              </div>
            </div>
            <ContactForm />
          </div>
        </section>

        <footer className="border-t border-slate-200/80 py-8 text-center text-sm text-slate-500 dark:border-slate-800/80 dark:text-slate-400">
          Built with Next.js, Tailwind CSS, and Framer Motion. Ready for deployment on Vercel.
        </footer>
      </div>
    </main>
  );
}
