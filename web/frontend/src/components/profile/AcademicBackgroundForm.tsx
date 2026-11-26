
import { useState, type FormEvent } from "react";
import { GraduationCap, Pencil, Check, X } from "lucide-react";

import {
  updateStudentProfile,
  type StudentProfileResponse,
} from "../../services/api";

type Props = {
  profile: StudentProfileResponse;
  onSaved: (profile: StudentProfileResponse) => void;
};

const EDUCATION_LEVELS = [
  "SS1",
  "SS2",
  "SS3",
  "Graduated",
];

export default function AcademicBackgroundForm({
  profile,
  onSaved,
}: Props) {
  const [editing, setEditing] = useState(false);
  const [educationLevel, setEducationLevel] = useState(
    profile.education_level
  );

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function startEditing() {
    setEducationLevel(profile.education_level);
    setError("");
    setSuccess("");
    setEditing(true);
  }

  function cancelEditing() {
    setEducationLevel(profile.education_level);
    setEditing(false);
    setError("");
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    setError("");
    setSuccess("");
    setSaving(true);

    try {
      const updatedProfile = await updateStudentProfile({
        education_level: educationLevel,
      });

      onSaved(updatedProfile);
      setEditing(false);
      setSuccess("Your academic background has been updated.");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to update your academic background."
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="mb-8 rounded-2xl border border-gray-200 bg-white p-6 sm:p-8"
    >
      <div className="mb-6 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <GraduationCap
            className="text-emerald-700"
            size={23}
          />

          <h2 className="text-xl font-semibold text-gray-900">
            Academic Background
          </h2>
        </div>

        {!editing && (
          <button
            type="button"
            onClick={startEditing}
            className="inline-flex items-center gap-2 rounded-xl border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <Pencil size={16} />
            Edit
          </button>
        )}
      </div>

      <div className="grid gap-6 sm:grid-cols-2">
        <div>
          <label
            htmlFor="academic-country"
            className="mb-2 block text-sm text-gray-500"
          >
            Country of education
          </label>

          {editing ? (
            <>
              <input
                id="academic-country"
                value={profile.country}
                disabled
                className="w-full cursor-not-allowed rounded-xl border border-gray-200 bg-gray-100 px-4 py-3 text-gray-400"
              />

              <p className="mt-2 text-xs text-gray-400">
                Country cannot currently be changed.
              </p>
            </>
          ) : (
            <p className="font-medium text-gray-900">
              {profile.country}
            </p>
          )}
        </div>

        <div>
          <label
            htmlFor="education-level"
            className="mb-2 block text-sm text-gray-500"
          >
            Education level
          </label>

          {editing ? (
            <select
              id="education-level"
              value={educationLevel}
              onChange={(event) =>
                setEducationLevel(event.target.value)
              }
              disabled={saving}
              required
              className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3"
            >
              {EDUCATION_LEVELS.map((level) => (
                <option key={level} value={level}>
                  {level}
                </option>
              ))}
            </select>
          ) : (
            <p className="font-medium text-gray-900">
              {profile.education_level}
            </p>
          )}
        </div>
      </div>

      {error && (
        <div
          role="alert"
          className="mt-6 rounded-xl bg-red-50 p-4 text-sm text-red-700"
        >
          {error}
        </div>
      )}

      {success && (
        <div
          role="status"
          className="mt-6 rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800"
        >
          {success}
        </div>
      )}

      {editing && (
        <div className="mt-8 flex flex-wrap justify-end gap-3 border-t border-gray-100 pt-6">
          <button
            type="button"
            onClick={cancelEditing}
            disabled={saving}
            className="inline-flex items-center gap-2 rounded-xl border border-gray-200 px-5 py-3 text-gray-700"
          >
            <X size={17} />
            Cancel
          </button>

          <button
            type="submit"
            disabled={
              saving ||
              educationLevel === profile.education_level
            }
            className="inline-flex items-center gap-2 rounded-xl bg-[#176B54] px-6 py-3 font-semibold text-white hover:bg-[#115540] disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Check size={18} />
            {saving ? "Saving..." : "Save changes"}
          </button>
        </div>
      )}
    </form>
  );
}
