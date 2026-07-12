import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center px-6 py-12">
      <div className="max-w-6xl w-full grid gap-10 lg:grid-cols-[1.2fr_0.8fr] items-center">
        <section className="space-y-8">
          <div className="inline-flex items-center gap-3 rounded-full border border-slate-700 bg-slate-900/60 px-4 py-2 text-sm text-slate-300">
            Enterprise-grade risk AI · Role-based access · Banking-ready
          </div>

          <div className="space-y-6">
            <h1 className="text-5xl font-semibold tracking-tight text-white">SME Credit Risk Platform for Financial Institutions</h1>
            <p className="max-w-2xl text-lg leading-8 text-slate-300">
              Launch a polished SaaS workflow for SME assessment, role-based access, and AI-driven credit decisions. Designed for banks, risk teams, and compliance units.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              href="/login"
              className="inline-flex items-center justify-center rounded-full bg-blue-600 px-6 py-3 text-base font-semibold text-white shadow-lg shadow-blue-500/20 hover:bg-blue-500 transition"
            >
              Sign in
            </Link>
            <Link
              href="/register"
              className="inline-flex items-center justify-center rounded-full border border-slate-700 bg-slate-900/90 px-6 py-3 text-base font-semibold text-slate-100 hover:bg-slate-800 transition"
            >
              Create account
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm text-slate-400">
            <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-5">
              <p className="font-semibold text-slate-100">Rapid onboarding</p>
              <p className="mt-2 text-slate-400">Secure user registration and instant role assignment.</p>
            </div>
            <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-5">
              <p className="font-semibold text-slate-100">Role-based access</p>
              <p className="mt-2 text-slate-400">Admins, analysts and managers get tailored workflows.</p>
            </div>
            <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-5">
              <p className="font-semibold text-slate-100">AI-backed insights</p>
              <p className="mt-2 text-slate-400">Prediction and recommendations driven by ML and Gemini AI.</p>
            </div>
          </div>
        </section>

        <aside className="rounded-[2rem] border border-slate-800 bg-slate-900/80 p-8 shadow-2xl shadow-slate-950/60">
          <div className="space-y-6">
            <div className="rounded-3xl bg-slate-950/60 p-6 border border-slate-800">
              <p className="text-sm uppercase tracking-[0.24em] text-blue-400">Platform status</p>
              <h2 className="mt-4 text-3xl font-semibold text-white">Ready for next-gen SME risk operations.</h2>
            </div>
            <div className="grid gap-4">
              <StatCard title="Role-aware routing" value="Admin / Analyst / Manager" />
              <StatCard title="Secure API" value="JWT + OAuth2" />
              <StatCard title="Smart assessment" value="Risk scoring + advisory" />
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}

function StatCard({ title, value }: { title: string; value: string }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-5">
      <p className="text-sm text-slate-400">{title}</p>
      <p className="mt-3 text-xl font-semibold text-white">{value}</p>
    </div>
  );
}
