export type AssessmentStatus =
  | "SATISFIED"
  | "NOT_SATISFIED"
  | "UNKNOWN";

export type AdmissionSource = {
  id: number;
  title: string;
  url: string;
  verified_date: string;
  evidence_text: string | null;
  admission_cycle: string | null;
};

export type SubjectAssessment = {
  requirement_id: number;
  subject_requirement_id: number;
  subject: string;
  requirement_level: string;
  student_grade: string | null;
  minimum_grade: string | null;
  minimum_years: number | null;
  minimum_course_level: string | null;
  status: AssessmentStatus;
  reason: string;
  sources: AdmissionSource[];
};

export type AggregateAssessment = {
  requirement_id: number;
  requirement_type: string;
  requirement_level: string;
  required_value: number | null;
  student_value: number | null;
  minimum_grade: string | null;
  gpa_scale: number | null;
  status: AssessmentStatus;
  reason: string;
  sources: AdmissionSource[];
};

export type ProgramRecommendation = {
  university_id: number;
  university_name: string;
  university_country: string;
  program_id: number;
  program_name: string;

  academic_status: AssessmentStatus;
  evaluated_requirements_status: AssessmentStatus;

  explanation: string;
  subject_assessments: SubjectAssessment[];
  aggregate_assessments: AggregateAssessment[];

  requirements_complete: boolean;
  ai_generated: boolean;
  ai_verified: boolean;
  ai_assessment: string | null;
  ai_revisions: number;

  disclaimer: string;
};

export type RecommendationResponse = {
  student_index: string;
  student_country: string;
  credential_type: string;
  total_recommendations: number;
  recommendations: ProgramRecommendation[];
};