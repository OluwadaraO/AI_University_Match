import {
  GraduationCap,
  MapPin,
  Sparkles,
  ExternalLink,
  CheckCircle2,
  CircleHelp,
  XCircle,
} from "lucide-react";

import type {
  AssessmentStatus,
  ProgramRecommendation,
} from "../../types/recommendation";

type Props = {
  recommendation: ProgramRecommendation;
};

const statusConfig = {
  SATISFIED: {
    label: "Requirement met",
    style: "bg-emerald-50 text-emerald-700",
    icon: CheckCircle2,
  },
  NOT_SATISFIED: {
    label: "Requirement not met",
    style: "bg-red-50 text-red-700",
    icon: XCircle,
  },
  UNKNOWN: {
    label: "More information needed",
    style: "bg-amber-50 text-amber-700",
    icon: CircleHelp,
  },
};

function StatusBadge({
  status,
}: {
  status: AssessmentStatus;
}) {
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-medium ${config.style}`}
    >
      <Icon size={14} />
      {config.label}
    </span>
  );
}

function formatRequirement(type: string) {
  const labels: Record<string, string> = {
    minimum_credits: "Minimum WAEC credits",
    minimum_gpa: "Minimum GPA",
    minimum_percentage: "Minimum academic average",
  };

  return labels[type] ?? type.replaceAll("_", " ");
}

export default function UniversityCard({
  recommendation,
}: Props) {
  const assessments = [
    ...recommendation.subject_assessments,
    ...recommendation.aggregate_assessments,
  ];

  const sources = Array.from(
    new Map(
      assessments
        .flatMap((assessment) => assessment.sources)
        .map((source) => [source.url, source])
    ).values()
  );

  const metCount = assessments.filter(
    (assessment) => assessment.status === "SATISFIED"
  ).length;

  const aiExplanation = recommendation.ai_assessment
    ?.replace(/^Evaluation Status:.*$/im, "")
    .replace(/^\s*Explanation:\s*/i, "")
    .trim();

  return (
    <article className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">

      {/* University information */}
      <div className="border-b border-gray-100 p-6">
        <div className="flex items-start gap-4">
          <div className="rounded-xl bg-[#EAF3EF] p-3 text-[#123D35]">
            <GraduationCap size={28} />
          </div>

          <div className="flex-1">
            <h2 className="text-xl font-semibold text-[#172B26]">
              {recommendation.university_name}
            </h2>

            <p className="mt-1 text-sm text-gray-600">
              {recommendation.program_name}
            </p>

            <div className="mt-2 flex items-center gap-1.5 text-sm text-gray-500">
              <MapPin size={15} />
              {recommendation.university_country}
            </div>
          </div>
        </div>

        <div className="mt-5">
          <StatusBadge
            status={recommendation.academic_status}
          />
        </div>
      </div>

      {/* Academic assessments */}
      <div className="p-6">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
          <h3 className="font-semibold text-gray-900">
            Academic requirements
          </h3>

          <span className="text-sm text-gray-500">
            {metCount} of {assessments.length} evaluated
            requirements met
          </span>
        </div>

        {assessments.length === 0 && (
          <p className="text-sm text-gray-500">
            Admission requirements are not yet available
            for this program.
          </p>
        )}

        <div className="space-y-3">
          {recommendation.subject_assessments.map(
            (assessment) => (
              <div
                key={assessment.subject_requirement_id}
                className="rounded-xl border border-gray-100 bg-gray-50 p-4"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h4 className="font-medium text-gray-800">
                    {assessment.subject}
                  </h4>

                  <StatusBadge status={assessment.status} />
                </div>

                <p className="mt-2 text-sm text-gray-600">
                  Your grade:{" "}
                  <strong>
                    {assessment.student_grade ?? "Not available"}
                  </strong>
                </p>

                {assessment.minimum_grade !== null && (
                  <p className="mt-1 text-sm text-gray-600">
                    Minimum grade: {assessment.minimum_grade}
                  </p>
                )}

                {assessment.minimum_years !== null && (
                  <p className="mt-1 text-sm text-gray-600">
                    Required coursework:{" "}
                    {assessment.minimum_years} years
                  </p>
                )}

                {assessment.minimum_course_level && (
                  <p className="mt-1 text-sm text-gray-600">
                    Course level:{" "}
                    {assessment.minimum_course_level}
                  </p>
                )}

                <p className="mt-3 text-sm leading-6 text-gray-500">
                  {assessment.reason}
                </p>
              </div>
            )
          )}

          {recommendation.aggregate_assessments.map(
            (assessment) => (
              <div
                key={`${assessment.requirement_id}-${assessment.requirement_type}`}
                className="rounded-xl border border-gray-100 bg-gray-50 p-4"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h4 className="font-medium text-gray-800">
                    {formatRequirement(
                      assessment.requirement_type
                    )}
                  </h4>

                  <StatusBadge status={assessment.status} />
                </div>

                <p className="mt-2 text-sm text-gray-600">
                  Required:{" "}
                  <strong>
                    {assessment.required_value ?? "Not specified"}
                    {assessment.requirement_type ===
                      "minimum_percentage" && "%"}
                    {assessment.gpa_scale !== null &&
                      ` / ${assessment.gpa_scale}`}
                  </strong>
                </p>

                <p className="mt-1 text-sm text-gray-600">
                  Your recorded value:{" "}
                  <strong>
                    {assessment.student_value ?? "Not available"}
                  </strong>
                </p>

                {assessment.minimum_grade && (
                  <p className="mt-1 text-sm text-gray-600">
                    Qualifying grade:{" "}
                    {assessment.minimum_grade} or better
                  </p>
                )}

                <p className="mt-3 text-sm leading-6 text-gray-500">
                  {assessment.reason}
                </p>
              </div>
            )
          )}
        </div>

        {/* AI explanation */}
        <div className="mt-6 rounded-xl bg-[#EEF5F1] p-5">
          <div className="flex items-center gap-2 text-[#123D35]">
            <Sparkles size={19} />

            <h3 className="font-semibold">
              {recommendation.ai_generated
                ? "AI insights"
                : "Academic insights"}
            </h3>
          </div>

          <p className="mt-3 text-sm leading-6 text-gray-700">
            {recommendation.ai_verified && aiExplanation
              ? aiExplanation
              : recommendation.explanation}
          </p>

          {recommendation.ai_verified && (
            <p className="mt-3 text-xs text-emerald-700">
              AI assessment checked against academic
              matching results.
            </p>
          )}
        </div>

        {/* Admission sources */}
        {sources.length > 0 && (
          <div className="mt-6">
            <h3 className="mb-3 text-sm font-semibold text-gray-800">
              Admission sources
            </h3>

            <div className="space-y-3">
              {sources.map((source) => (
                <a
                  key={source.url}
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-sm text-emerald-700 hover:underline"
                >
                  <ExternalLink size={15} />
                  {source.title}
                </a>
              ))}
            </div>
          </div>
        )}

        <p className="mt-6 border-t border-gray-100 pt-4 text-xs leading-5 text-gray-400">
          {recommendation.disclaimer}
        </p>
      </div>
    </article>
  );
}