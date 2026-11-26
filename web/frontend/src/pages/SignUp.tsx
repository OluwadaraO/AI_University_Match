import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowRight,
  CheckCircle2,
  Eye,
  EyeOff,
  GraduationCap,
  Sparkles,
} from "lucide-react";

import { registerUser } from "../services/api";

export default function SignUp() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (password.length < 12) {
      setError("Your password must contain at least 12 characters.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Your passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await registerUser({
        email: email.trim(),
        password,
      });

      navigate("/login", {
        replace: true,
        state: {
          registered: true,
        },
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#FAFAF7] lg:grid lg:grid-cols-2">
      {/* Left panel */}
      <section className="relative hidden min-h-screen flex-col justify-between overflow-hidden bg-[#123D35] p-12 text-white lg:flex">
        <div className="absolute -right-32 -top-32 h-96 w-96 rounded-full bg-emerald-400/10 blur-3xl" />
        <div className="absolute -bottom-40 -left-32 h-[450px] w-[450px] rounded-full bg-teal-300/10 blur-3xl" />

        <Link
          to="/signup"
          className="relative z-10 flex items-center gap-3 text-xl font-semibold"
        >
          <div className="rounded-xl bg-white/15 p-2.5">
            <GraduationCap size={25} />
          </div>
          AI University Match
        </Link>

        <div className="relative z-10 max-w-lg">
          <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-4 py-2 text-sm text-emerald-100">
            <Sparkles size={16} />
            Your future starts here
          </div>

          <h1 className="text-5xl font-semibold leading-tight tracking-tight xl:text-6xl">
            Your dream university is closer than you think.
          </h1>

          <p className="mt-7 max-w-md text-lg leading-8 text-emerald-100/80">
            Discover universities that align with your academic
            achievements, interests, and aspirations.
          </p>

          <div className="mt-12 space-y-5">
            {[
              "Explore universities that fit your goals",
              "Understand admission requirements",
              "Get personalized, explainable recommendations",
            ].map((feature) => (
              <div key={feature} className="flex items-center gap-3">
                <CheckCircle2
                  size={21}
                  className="shrink-0 text-emerald-300"
                />
                <span className="text-emerald-50">{feature}</span>
              </div>
            ))}
          </div>
        </div>

        <p className="relative z-10 text-sm text-emerald-100/60">
          Built to make university discovery more accessible.
        </p>
      </section>

      {/* Right panel */}
      <main className="flex min-h-screen items-center justify-center px-6 py-12 sm:px-10 lg:px-16">
        <div className="w-full max-w-md">
          <div className="mb-10 flex items-center gap-2 text-[#123D35] lg:hidden">
            <GraduationCap size={27} />
            <span className="text-lg font-semibold">
              AI University Match
            </span>
          </div>

          <div className="mb-9">
            <p className="mb-3 text-sm font-semibold tracking-wide text-emerald-700">
              GET STARTED
            </p>

            <h2 className="text-4xl font-semibold tracking-tight text-[#172B26]">
              Create your account
            </h2>

            <p className="mt-3 text-base text-gray-500">
              Start exploring universities that match your potential.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label
                htmlFor="email"
                className="mb-2 block text-sm font-medium text-gray-700"
              >
                Email address
              </label>

              <input
                id="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@example.com"
                className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3.5 text-gray-900 outline-none transition focus:border-emerald-700 focus:ring-2 focus:ring-emerald-700/10"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="mb-2 block text-sm font-medium text-gray-700"
              >
                Password
              </label>

              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="new-password"
                  required
                  minLength={12}
                  maxLength={128}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Create a secure password"
                  className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3.5 pr-12 text-gray-900 outline-none transition focus:border-emerald-700 focus:ring-2 focus:ring-emerald-700/10"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={
                    showPassword ? "Hide password" : "Show password"
                  }
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-700"
                >
                  {showPassword ? <EyeOff size={19} /> : <Eye size={19} />}
                </button>
              </div>

              <p className="mt-2 text-xs text-gray-500">
                Must be at least 12 characters.
              </p>
            </div>

            <div>
              <label
                htmlFor="confirm-password"
                className="mb-2 block text-sm font-medium text-gray-700"
              >
                Confirm password
              </label>

              <input
                id="confirm-password"
                type="password"
                autoComplete="new-password"
                required
                value={confirmPassword}
                onChange={(event) =>
                  setConfirmPassword(event.target.value)
                }
                placeholder="Re-enter your password"
                className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3.5 text-gray-900 outline-none transition focus:border-emerald-700 focus:ring-2 focus:ring-emerald-700/10"
              />
            </div>

            {error && (
              <div
                role="alert"
                className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
              >
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="mt-3 flex w-full items-center justify-center gap-2 rounded-xl bg-[#176B54] px-5 py-4 font-semibold text-white transition hover:bg-[#115540] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Creating account..." : "Create account"}
              {!loading && <ArrowRight size={19} />}
            </button>
          </form>

          <p className="mt-8 text-center text-sm text-gray-500">
            Already have an account?{" "}
            <Link
              to="/login"
              className="font-semibold text-emerald-700 hover:underline"
            >
              Log in
            </Link>
          </p>

          <p className="mt-10 text-center text-xs leading-5 text-gray-400">
            Your academic journey, your choices, your future.
          </p>
        </div>
      </main>
    </div>
  );
}