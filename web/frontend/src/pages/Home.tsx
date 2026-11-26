
import { Link } from "react-router-dom";
import {
  ArrowRight,
  GraduationCap,
  UserRound,
  Compass,
} from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#FAFAF7]">
      <header className="border-b border-gray-200 bg-white px-6 py-5">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <Link
            to="/home"
            className="flex items-center gap-2 font-semibold text-[#123D35]"
          >
            <GraduationCap size={25} />
            AI University Match
          </Link>

          <Link
            to="/profile"
            className="inline-flex items-center gap-2 rounded-xl border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <UserRound size={18} />
            My Profile
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-12">
        <div className="mb-10">
          <p className="mb-3 text-sm font-semibold text-emerald-700">
            YOUR DASHBOARD
          </p>

          <h1 className="text-4xl font-semibold tracking-tight text-[#172B26]">
            Welcome to AI University Match
          </h1>

          <p className="mt-4 max-w-xl text-gray-500">
            Your university journey starts here. Complete your profile
            to help us understand your academic background and goals.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Link
            to="/profile"
            className="rounded-2xl border border-gray-200 bg-white p-7 transition hover:border-emerald-300 hover:shadow-sm"
          >
            <UserRound size={28} className="mb-5 text-emerald-700" />

            <h2 className="text-xl font-semibold text-gray-900">
              My Profile
            </h2>

            <p className="mt-3 text-sm leading-6 text-gray-500">
              View and update your academic background and WAEC results.
            </p>

            <div className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-emerald-700">
              Manage profile
              <ArrowRight size={17} />
            </div>
          </Link>

            <Link
            to="/recommendations"
            className="rounded-2xl border border-gray-200 bg-white p-7 transition hover:border-emerald-300 hover:shadow-sm"
            >
            <Compass
                size={28}
                className="mb-5 text-emerald-700"
            />

            <h2 className="text-xl font-semibold text-gray-900">
                University Matches
            </h2>

            <p className="mt-3 text-sm leading-6 text-gray-500">
                Discover universities based on your academic results
                and intended major, with personalized AI insights.
            </p>

            <div className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-emerald-700">
                Explore universities
                <ArrowRight size={17} />
            </div>
            </Link>
        </div>
      </main>
    </div>
  );
}
