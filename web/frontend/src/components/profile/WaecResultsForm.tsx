
import { useEffect, useState, type FormEvent } from "react";
import { Plus, Trash2, Pencil, X, Check } from "lucide-react";

import {
  saveStudentCredentials,
  updateStudentCredentials,
  type CredentialResponse,
} from "../../services/api";

type SubjectRow = {
  id: number;
  subject: string;
  grade: string;
};

type Props = {
  studentIndex: string;
  credential: CredentialResponse | null;
  onSaved: (credential: CredentialResponse) => void;
};

const SUBJECTS = [
  "English Language",
  "Mathematics",
  "Biology",
  "Chemistry",
  "Physics",
  "Economics",
  "Government",
  "Geography",
  "Commerce",
  "Financial Accounting",
  "Agricultural Science",
  "Further Mathematics",
  "Literature in English",
  "Civic Education",
  "Computer Studies",
  "Yoruba",
  "Igbo",
  "Hausa",
];

const GRADES = [
  "A1", "B2", "B3", "C4", "C5",
  "C6", "D7", "E8", "F9",
];

function credentialToRows(
  credential: CredentialResponse | null
): SubjectRow[] {
  if (!credential || credential.results.length === 0) {
    return [{ id: 1, subject: "", grade: "" }];
  }

  return credential.results.map((result, index) => ({
    id: index + 1,
    subject: result.subject,
    grade: result.grade,
  }));
}

export default function WaecResultsForm({
  studentIndex,
  credential,
  onSaved,
}: Props) {
  const [rows, setRows] = useState<SubjectRow[]>(() =>
    credentialToRows(credential)
  );
  const [editing, setEditing] = useState(!credential);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setRows(credentialToRows(credential));
    setEditing(!credential);
  }, [credential]);

  function updateRow(
    id: number,
    field: "subject" | "grade",
    value: string
  ) {
    setRows((previous) =>
      previous.map((row) =>
        row.id === id ? { ...row, [field]: value } : row
      )
    );
  }

  function addRow() {
    setRows((previous) => [
      ...previous,
      {
        id: Math.max(0, ...previous.map((row) => row.id)) + 1,
        subject: "",
        grade: "",
      },
    ]);
  }

  function removeRow(id: number) {
    setRows((previous) =>
      previous.filter((row) => row.id !== id)
    );
  }

  function cancelEditing() {
    setRows(credentialToRows(credential));
    setEditing(false);
    setError("");
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (rows.length === 0) {
      setError("Add at least one subject.");
      return;
    }

    if (rows.some((row) => !row.subject || !row.grade)) {
      setError("Select a subject and grade for every row.");
      return;
    }

    const subjects = rows.map((row) =>
      row.subject.trim().toLowerCase()
    );

    if (new Set(subjects).size !== subjects.length) {
      setError("You cannot add the same subject twice.");
      return;
    }

    setSaving(true);

    try {
      const data = {
        credential_type: "WAEC",
        results: rows.map(({ subject, grade }) => ({
          subject,
          grade,
        })),
      };

      const saved = credential
        ? await updateStudentCredentials(
            studentIndex,
            credential.id,
            data
          )
        : await saveStudentCredentials(studentIndex, data);

      onSaved(saved);
      setEditing(false);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to save your results."
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-gray-200 bg-white p-6 sm:p-9"
    >
      <div className="mb-7 flex items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">
            WAEC Results
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Add your examination subjects and grades.
          </p>
        </div>

        {credential && !editing && (
          <button
            type="button"
            onClick={() => {
              setError("");
              setEditing(true);
            }}
            className="inline-flex items-center gap-2 rounded-xl border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <Pencil size={16} />
            Edit results
          </button>
        )}
      </div>

      {credential && !editing && (
        <div className="mb-6 rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800">
          Your WAEC results have been saved.
        </div>
      )}

      <div className="space-y-4">
        {rows.map((row, index) => (
          <div
            key={row.id}
            className="grid grid-cols-1 items-end gap-3 sm:grid-cols-[1fr_150px_44px]"
          >
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Subject {index + 1}
              </label>

              <select
                value={row.subject}
                onChange={(event) =>
                  updateRow(row.id, "subject", event.target.value)
                }
                disabled={!editing || saving}
                required
                className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3.5 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-500"
              >
                <option value="">Select subject</option>
                {SUBJECTS.map((subject) => (
                  <option
                    key={subject}
                    value={subject}
                    disabled={rows.some(
                      (other) =>
                        other.id !== row.id &&
                        other.subject === subject
                    )}
                  >
                    {subject}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Grade
              </label>

              <select
                value={row.grade}
                onChange={(event) =>
                  updateRow(row.id, "grade", event.target.value)
                }
                disabled={!editing || saving}
                required
                className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3.5 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-500"
              >
                <option value="">Select grade</option>
                {GRADES.map((grade) => (
                  <option key={grade} value={grade}>
                    {grade}
                  </option>
                ))}
              </select>
            </div>

            {editing && (
              <button
                type="button"
                onClick={() => removeRow(row.id)}
                disabled={saving || rows.length === 1}
                aria-label={`Remove subject ${index + 1}`}
                className="flex h-12 items-center justify-center rounded-xl text-gray-400 hover:bg-red-50 hover:text-red-600 disabled:opacity-30"
              >
                <Trash2 size={19} />
              </button>
            )}
          </div>
        ))}
      </div>

      {editing && (
        <button
          type="button"
          onClick={addRow}
          disabled={saving || rows.length >= SUBJECTS.length}
          className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-emerald-700 hover:text-emerald-900 disabled:opacity-40"
        >
          <Plus size={18} />
          Add another subject
        </button>
      )}

      {error && (
        <div
          role="alert"
          className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
        >
          {error}
        </div>
      )}

      <div className="mt-8 flex flex-wrap justify-end gap-3 border-t border-gray-100 pt-6">
        {editing && credential && (
          <button
            type="button"
            onClick={cancelEditing}
            disabled={saving}
            className="inline-flex items-center gap-2 rounded-xl border border-gray-200 px-5 py-3 text-gray-700"
          >
            <X size={17} />
            Cancel
          </button>
        )}

        {editing && (
          <button
            type="submit"
            disabled={saving || !studentIndex}
            className="inline-flex items-center gap-2 rounded-xl bg-[#176B54] px-6 py-3 font-semibold text-white hover:bg-[#115540] disabled:opacity-60"
          >
            <Check size={18} />
            {saving
              ? "Saving..."
              : credential
                ? "Save changes"
                : "Save results"}
          </button>
        )}
      </div>
    </form>
  );
}
