import { useState } from "react";
import { Link, Navigate } from "react-router-dom";

import {
  ArrowLeft,
  GraduationCap,
  Sparkles,
  LoaderCircle,
  Compass,
  AlertCircle,
} from "lucide-react";

import { getRecommendations } from "../services/api";

import UniversityCard from
  "../components/recommendations/UniversityCard";

import type {
  RecommendationResponse,
} from "../types/recommendation";

export default function Recommendations() {
  const [major, setMajor] = useState("Computer Science");

  const [data, setData] =
    useState<RecommendationResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleGenerate() {
    if (loading) return;

    setLoading(true);
    setError("");
    setData(null);

    try {
      const response = await getRecommendations(
        major,
        true
      );

      setData(response);
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

  if (!sessionStorage.getItem("access_token")) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-[#FAFAF7]">

      {/* Header */}
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
            className="text-sm font-medium text-gray-600 hover:text-emerald-700"
          >
            My Profile
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-10">

        <Link
          to="/home"
          className="mb-8 inline-flex items-center gap-2 text-sm text-gray-500 hover:text-emerald-700"
        >
          <ArrowLeft size={16} />
          Back to dashboard
        </Link>

        {/* Introduction */}
        <div className="mb-8">
          <p className="mb-3 text-sm font-semibold tracking-wide text-emerald-700">
            DISCOVER YOUR OPTIONS
          </p>

          <h1 className="text-4xl font-semibold tracking-tight text-[#172B26]">
            Find your university
          </h1>

          <p className="mt-4 max-w-2xl leading-7 text-gray-500">
            Explore universities based on your academic
            background and intended major. Understand which
            requirements you meet and what you may still need
            before applying.
          </p>
        </div>

        {/* Search controls */}
        <div className="rounded-2xl border border-gray-200 bg-white p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end">

            <div className="flex-1">
              <label
                htmlFor="major"
                className="mb-2 block text-sm font-medium text-gray-700"
              >
                Intended major
              </label>

              <select
                id="major"
                value={major}
                disabled={loading}
                onChange={(event) => {
                  setMajor(event.target.value);
                  setData(null);
                  setError("");
                }}
                className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm text-gray-800 outline-none focus:border-emerald-500"
              >
                <option value="Computer Science">
                  Computer Science
                </option>

                <option value="">
                  All available programs
                </option>
              </select>
            </div>

            <button
              onClick={handleGenerate}
              disabled={loading}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-[#123D35] px-6 py-3 text-sm font-semibold text-white transition hover:bg-[#1B5549] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? (
                <LoaderCircle
                  size={18}
                  className="animate-spin"
                />
              ) : (
                <Sparkles size={18} />
              )}

              {loading
                ? "Finding your matches..."
                : "Find my matches"}
            </button>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div
            role="alert"
            className="mt-6 rounded-xl border border-red-200 bg-red-50 p-5"
          >
            <div className="flex items-center gap-2 text-red-700">
              <AlertCircle size={19} />
              <p className="text-sm font-medium">{error}</p>
            </div>

            <Link
              to="/profile"
              className="mt-3 inline-block text-sm font-medium text-red-700 underline"
            >
              Review your academic profile
            </Link>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div
            role="status"
            className="py-20 text-center"
          >
            <LoaderCircle
              size={36}
              className="mx-auto animate-spin text-emerald-700"
            />

            <h2 className="mt-5 text-lg font-semibold text-gray-800">
              Finding universities for you
            </h2>

            <p className="mt-2 text-sm text-gray-500">
              We're comparing your academic results with
              recorded admission requirements.
            </p>
          </div>
        )}

        {/* Initial state */}
        {!data && !loading && !error && (
          <div className="py-20 text-center">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-[#EAF3EF]">
              <Compass
                size={30}
                className="text-emerald-700"
              />
            </div>

            <h2 className="mt-5 text-xl font-semibold text-gray-800">
              Your next chapter starts here
            </h2>

            <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-gray-500">
              Choose your intended major and generate
              recommendations based on your academic profile.
            </p>
          </div>
        )}

        {/* Recommendations */}
        {data && (
          <section className="mt-10">
            <h2 className="text-2xl font-semibold text-[#172B26]">
              Your university matches
            </h2>

            <p className="mt-2 text-sm text-gray-500">
              {data.total_recommendations} programs found
              {" · "}
              Based on your {data.credential_type} results
            </p>

            {data.recommendations.length === 0 ? (
              <div className="mt-6 rounded-2xl border border-gray-200 bg-white p-10 text-center">
                <p className="font-medium text-gray-800">
                  No matching programs found
                </p>

                <p className="mt-2 text-sm text-gray-500">
                  Try selecting another available program.
                </p>
              </div>
            ) : (
              <div className="mt-6 grid items-start gap-6 lg:grid-cols-2">
                {data.recommendations.map(
                  (recommendation) => (
                    <UniversityCard
                      key={recommendation.program_id}
                      recommendation={recommendation}
                    />
                  )
                )}
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}