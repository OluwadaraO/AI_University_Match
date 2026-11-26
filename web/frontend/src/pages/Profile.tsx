
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  BookOpen,
  UserRound,
} from "lucide-react";

import AcademicBackgroundForm from "../components/profile/AcademicBackgroundForm";

import WaecResultsForm from "../components/profile/WaecResultsForm";

import {
  getStudentProfile,
  getStudentCredentials,
  type StudentProfileResponse,
  type CredentialResponse,
} from "../services/api";

export default function Profile() {
  const navigate = useNavigate();

  const [profile, setProfile] =
    useState<StudentProfileResponse | null>(null);

  const [credential, setCredential] =
    useState<CredentialResponse | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const student = await getStudentProfile();
        setProfile(student);

        if (student) {
          const credentials = await getStudentCredentials();

          const waec = credentials.find(
            (item) => item.credential_type.toUpperCase() === "WAEC"
          );

          setCredential(waec ?? null);
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

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Loading your profile...</p>
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

  if (!profile) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-5 px-6 text-center">
        <h1 className="text-2xl font-semibold">
          Complete your student profile
        </h1>

        <p className="max-w-md text-gray-500">
          Add your academic background to start building your university profile.
        </p>

        <Link
          to="/onboarding/academics"
          className="rounded-xl bg-[#176B54] px-6 py-3 font-semibold text-white"
        >
          Add academic background
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAFAF7] px-6 py-12">
      <div className="mx-auto max-w-4xl">
        <button
          type="button"
          onClick={() => navigate("/home")}
          className="mb-9 inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900"
        >
          <ArrowLeft size={17} />
          Back to Home
        </button>

        <div className="mb-10">
          <div className="mb-4 flex items-center gap-3 text-[#176B54]">
            <UserRound size={28} />
            <span className="font-semibold">MY ACCOUNT</span>
          </div>

          <h1 className="text-4xl font-semibold tracking-tight text-[#172B26]">
            My Profile
          </h1>

          <p className="mt-3 text-gray-500">
            Manage your academic information and university preferences.
          </p>
        </div>

        <section className="mb-8 rounded-2xl border border-gray-200 bg-white p-6 sm:p-8">
          <div className="mb-6 flex items-center gap-3">
            <UserRound className="text-emerald-700" size={23} />
            <h2 className="text-xl font-semibold text-gray-900">
              Personal Information
            </h2>
          </div>

          <div className="grid gap-6 sm:grid-cols-2">
            <div>
              <p className="text-sm text-gray-500">Email address</p>
              <p className="mt-1 font-medium text-gray-900">
                {profile.email}
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500">Student ID</p>
              <p className="mt-1 font-medium text-gray-900">
                {profile.student_index}
              </p>
            </div>
          </div>
        </section>

        <AcademicBackgroundForm
            profile={profile}
            onSaved={setProfile}
        />

        <div className="mb-8 flex items-center gap-3">
          <BookOpen className="text-emerald-700" size={23} />
          <h2 className="text-xl font-semibold text-gray-900">
            Academic Results
          </h2>
        </div>

        <WaecResultsForm
          studentIndex={profile.student_index}
          credential={credential}
          onSaved={setCredential}
        />
      </div>
    </div>
  );
}
