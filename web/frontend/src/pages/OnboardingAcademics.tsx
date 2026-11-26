
import { useEffect, useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowLeft, ArrowRight, GraduationCap } from "lucide-react";

import {
  createStudentProfile,
  getStudentProfile,
  type StudentProfileResponse,
} from "../services/api";

export default function OnboardingAcademics() {
  const navigate = useNavigate();

  const [country, setCountry] = useState("Nigeria");
  const [educationLevel, setEducationLevel] = useState("");
  const [existingProfile, setExistingProfile] =
    useState<StudentProfileResponse | null>(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const profile = await getStudentProfile();

        if (profile) {
          setExistingProfile(profile);
          setCountry(profile.country);
          setEducationLevel(profile.education_level);
        }
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load your profile."
        );
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (!educationLevel) {
      setError("Please select your education level.");
      return;
    }

    setSaving(true);

    try {
      if (!existingProfile) {
        await createStudentProfile({
          country,
          education_level: educationLevel,
        });
      }

      navigate("/onboarding/results");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to save your academic profile."
      );
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Loading your profile...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAFAF7] px-6 py-12">
      <div className="mx-auto max-w-2xl">
        <Link
          to="/onboarding"
          className="mb-10 inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900"
        >
          <ArrowLeft size={17} />
          Back to onboarding
        </Link>

        <div className="mb-8 flex items-center gap-3 text-[#176B54]">
          <GraduationCap size={28} />
          <span className="font-semibold">AI University Match</span>
        </div>

        <div className="mb-8">
          <p className="mb-3 text-sm font-semibold text-emerald-700">
            STEP 1 OF 3
          </p>

          <h1 className="text-4xl font-semibold tracking-tight text-[#172B26]">
            Your academic background
          </h1>

          <p className="mt-4 text-gray-500">
            Let's start with a few details about your education.
            This helps us understand which admission requirements
            apply to your academic background.
          </p>
        </div>

        <div className="mb-10 flex gap-2">
          <div className="h-1.5 flex-1 rounded-full bg-emerald-700" />
          <div className="h-1.5 flex-1 rounded-full bg-gray-200" />
          <div className="h-1.5 flex-1 rounded-full bg-gray-200" />
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-7 rounded-2xl border border-gray-200 bg-white p-6 sm:p-9"
        >
          <div>
            <label
            htmlFor="country"
            className={`mb-2 block text-sm font-medium ${
                existingProfile ? "text-gray-400" : "text-gray-700"
            }`}
            >
            Country of education
            </label>

            <select
              id="country"
              value={country}
              onChange={(event) => setCountry(event.target.value)}
              disabled={!!existingProfile}
              className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3.5 text-gray-900 outline-none focus:border-emerald-700 disabled:cursor-not-allowed disabled:border-gray-200 disabled:bg-gray-100 disabled:text-gray-400 disabled:opacity-75"
            >
              <option value="Nigeria">Nigeria</option>
            </select>

            <p className="mt-2 text-xs text-gray-500">
              We're starting with Nigerian secondary-school qualifications.
            </p>
          </div>

          <div>
            <label
            htmlFor="education-level"
            className={`mb-2 block text-sm font-medium ${
                existingProfile ? "text-gray-400" : "text-gray-700"
            }`}
            >
            Education level
            </label>

            <select
              id="education-level"
              value={educationLevel}
              onChange={(event) => setEducationLevel(event.target.value)}
              disabled={!!existingProfile}
              required
              className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3.5 text-gray-900 outline-none focus:border-emerald-700 disabled:cursor-not-allowed disabled:border-gray-200 disabled:bg-gray-100 disabled:text-gray-400 disabled:opacity-75"
            >
              <option value="">Select your education level</option>
              <option value="SS1">SS1 — Senior Secondary School 1</option>
              <option value="SS2">SS2 — Senior Secondary School 2</option>
              <option value="SS3">SS3 — Senior Secondary School 3</option>
              <option value="Graduated">Completed secondary school</option>
            </select>
          </div>

          {existingProfile && (
            <div className="rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800">
              Your academic profile has already been saved.
              You can continue to your examination results.
              Profile editing will be available later.
            </div>
          )}

          {error && (
            <div
              role="alert"
              className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
            >
              {error}
            </div>
          )}

          <div className="flex flex-col gap-3 border-t border-gray-100 pt-6 sm:flex-row sm:justify-between">
            <button
              type="button"
              onClick={() => navigate("/home")}
              className="rounded-xl px-5 py-3 text-sm font-medium text-gray-500 hover:text-gray-900"
            >
              Skip for now
            </button>

            <button
              type="submit"
              disabled={saving || !!error}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-[#176B54] px-6 py-3.5 font-semibold text-white hover:bg-[#115540] disabled:opacity-60"
            >
              {saving ? "Saving..." : "Continue to results"}
              {!saving && <ArrowRight size={18} />}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
