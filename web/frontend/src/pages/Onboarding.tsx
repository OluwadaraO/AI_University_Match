import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  GraduationCap,
  BookOpen,
  Compass,
  Sparkles,
} from "lucide-react";

export default function Onboarding() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#FAFAF7] px-6 py-12">
      <div className="w-full max-w-xl text-center">
        <div className="mx-auto mb-8 flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-100 text-emerald-800">
          <GraduationCap size={34} />
        </div>

        <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700">
          <Sparkles size={16} />
          Let's get to know you
        </div>

        <h1 className="text-4xl font-semibold tracking-tight text-[#172B26] sm:text-5xl">
          Let's find your university match.
        </h1>

        <p className="mx-auto mt-6 max-w-md text-lg leading-8 text-gray-500">
          Tell us a little about your academic background and what you're
          looking for in a university. We'll use your information to help
          you discover programs that fit your goals.
        </p>

        <div className="mt-10 grid gap-4 text-left sm:grid-cols-2">
          <div className="rounded-2xl border border-gray-200 bg-white p-5">
            <BookOpen className="mb-4 text-emerald-700" size={26} />
            <h3 className="font-semibold text-gray-900">
              Your academics
            </h3>
            <p className="mt-2 text-sm leading-6 text-gray-500">
              Add your WAEC results and educational background.
            </p>
          </div>

          <div className="rounded-2xl border border-gray-200 bg-white p-5">
            <Compass className="mb-4 text-emerald-700" size={26} />
            <h3 className="font-semibold text-gray-900">
              Your preferences
            </h3>
            <p className="mt-2 text-sm leading-6 text-gray-500">
              Share your preferred programs, locations, and budget.
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() => navigate("/onboarding/academics")}
          className="mt-10 flex w-full items-center justify-center gap-2 rounded-xl bg-[#176B54] px-6 py-4 font-semibold text-white transition hover:bg-[#115540]"
        >
          Get started
          <ArrowRight size={19} />
        </button>

        <button
          type="button"
          onClick={() => navigate("/home")}
          className="mt-4 w-full rounded-xl px-6 py-3 font-medium text-gray-500 transition hover:text-gray-900"
        >
          Skip for now
        </button>

        <p className="mt-5 text-xs text-gray-400">
          You can always complete or update your profile later.
        </p>
      </div>
    </div>
  );
}