
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowLeft, GraduationCap } from "lucide-react";

import WaecResultsForm from "../components/profile/WaecResultsForm";

import {
  getStudentProfile,
  getStudentCredentials,
  type CredentialResponse,
} from "../services/api";

export default function OnboardingResults() {
  const navigate = useNavigate();

  const [studentIndex, setStudentIndex] = useState("");
  const [credential, setCredential] =
    useState<CredentialResponse | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const profile = await getStudentProfile();

        if (!profile) {
          navigate("/onboarding/academics", { replace: true });
          return;
        }

        setStudentIndex(profile.student_index);

        const credentials = await getStudentCredentials();
        const existingWAEC = credentials.find(
          (item) => item.credential_type.toUpperCase() === "WAEC"
        );

        setCredential(existingWAEC ?? null);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load your academic results."
        );
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [navigate]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        Loading academic results...
      </div>
    );
  }

  if (error) {
    return (
      <div role="alert" className="p-8 text-center text-red-700">
        {error}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAFAF7] px-6 py-12">
      <div className="mx-auto max-w-3xl">
        <Link
          to="/onboarding/academics"
          className="mb-10 inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900"
        >
          <ArrowLeft size={17} />
          Back to academic background
        </Link>

        <div className="mb-8 flex items-center gap-3 text-[#176B54]">
          <GraduationCap size={28} />
          <span className="font-semibold">AI University Match</span>
        </div>

        <p className="mb-3 text-sm font-semibold text-emerald-700">
          ACADEMIC RESULTS
        </p>

        <h1 className="text-4xl font-semibold tracking-tight text-[#172B26]">
          Your examination results
        </h1>

        <p className="mb-9 mt-4 text-gray-500">
          Enter your WAEC subjects and grades. You can update
          these results whenever you need to.
        </p>

        <WaecResultsForm
          studentIndex={studentIndex}
          credential={credential}
          onSaved={setCredential}
        />

        <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
          <button
            type="button"
            onClick={() => navigate("/home")}
            className="text-sm font-medium text-gray-500 hover:text-gray-900"
          >
            Skip for now
          </button>

          <button
            type="button"
            onClick={() => navigate("/home")}
            disabled={!credential}
            className="rounded-xl bg-[#176B54] px-6 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-40"
          >
            Continue
          </button>
        </div>
      </div>
    </div>
  );
}
