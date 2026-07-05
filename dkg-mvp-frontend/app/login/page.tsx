"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { login, saveToken } from "@/lib/dkgApi";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const response = await login(username, password);
      saveToken(response.access_token);
      router.replace("/");
    } catch {
      setError("Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-ink px-5 text-slate-100">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm rounded border border-slate-800 bg-slate-900 p-6 shadow-2xl shadow-black/30"
      >
        <p className="text-xs uppercase tracking-[0.25em] text-cyan-300">
          Dharma Knowledge Graph
        </p>
        <h1 className="mt-2 text-2xl font-semibold">Login</h1>

        <label className="mt-6 block text-sm text-slate-300">
          Username
          <input
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            className="mt-2 h-11 w-full rounded border border-slate-700 bg-slate-950 px-3 text-slate-100 outline-none focus:border-cyan-400"
            autoComplete="username"
          />
        </label>

        <label className="mt-4 block text-sm text-slate-300">
          Password
          <input
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            type="password"
            className="mt-2 h-11 w-full rounded border border-slate-700 bg-slate-950 px-3 text-slate-100 outline-none focus:border-cyan-400"
            autoComplete="current-password"
          />
        </label>

        {error ? <p className="mt-4 text-sm text-rose-300">{error}</p> : null}

        <button
          type="submit"
          disabled={loading}
          className="mt-6 h-11 w-full rounded bg-cyan-500 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Signing in" : "Enter Knowledge Map"}
        </button>
      </form>
    </main>
  );
}
