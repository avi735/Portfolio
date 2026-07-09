'use client';

import { useState, type ChangeEvent, type FormEvent } from 'react';

const initialFormState = { name: '', email: '', message: '' };

export function ContactForm() {
  const [form, setForm] = useState(initialFormState);
  const [status, setStatus] = useState<'idle' | 'sending' | 'success' | 'error'>('idle');

  function handleChange(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus('sending');

    try {
      await new Promise((resolve) => setTimeout(resolve, 700));
      setStatus('success');
      setForm(initialFormState);
    } catch (error) {
      setStatus('error');
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 rounded-[2rem] border border-slate-200/80 bg-slate-50 p-8 shadow-soft dark:border-slate-800/80 dark:bg-slate-900">
      <div className="grid gap-5 sm:grid-cols-2">
        <label className="space-y-2 text-sm text-slate-700 dark:text-slate-300">
          <span>Name</span>
          <input
            name="name"
            value={form.name}
            onChange={handleChange}
            required
            className="w-full rounded-3xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100 dark:focus:border-slate-600 dark:focus:ring-slate-700"
            placeholder="Your name"
          />
        </label>
        <label className="space-y-2 text-sm text-slate-700 dark:text-slate-300">
          <span>Email</span>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
            className="w-full rounded-3xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100 dark:focus:border-slate-600 dark:focus:ring-slate-700"
            placeholder="you@example.com"
          />
        </label>
      </div>
      <label className="space-y-2 text-sm text-slate-700 dark:text-slate-300">
        <span>Message</span>
        <textarea
          name="message"
          value={form.message}
          onChange={handleChange}
          required
          rows={6}
          className="w-full rounded-3xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100 dark:focus:border-slate-600 dark:focus:ring-slate-700"
          placeholder="Tell me about your project."
        />
      </label>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <button type="submit" disabled={status === 'sending'} className="btn-primary w-full sm:w-auto">
          {status === 'sending' ? 'Sending...' : 'Send message'}
        </button>
        {status === 'success' && <p className="text-sm text-emerald-600">Message sent successfully.</p>}
        {status === 'error' && <p className="text-sm text-rose-600">Something went wrong. Please try again.</p>}
      </div>
    </form>
  );
}
