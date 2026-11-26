import type {
  RecommendationResponse,
} from "../types/recommendation";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export type RegisterRequest = {
  email: string;
  password: string;
};

export type UserResponse = {
  id: number;
  email: string;
};

export async function registerUser(
  data: RegisterRequest
): Promise<UserResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      typeof error?.detail === "string"
        ? error.detail
        : "Unable to create your account. Please try again."
    );
  }

  return response.json();
}

export type LoginRequest = {
  email: string;
  password: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export async function loginUser(
  data: LoginRequest
): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      typeof error?.detail === "string"
        ? error.detail
        : "Unable to log in. Please try again."
    );
  }

  return response.json();
}

export type StudentProfileRequest = {
  country: string;
  education_level: string;
};

export type StudentProfileResponse = {
  id: number;
  student_index: string;
  email: string;
  country: string;
  education_level: string;
};

function authHeaders(): HeadersInit {
  const token = sessionStorage.getItem("access_token");

  if (!token) {
    throw new Error("Please log in to continue.");
  }

  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
}

export async function getStudentProfile(): Promise<StudentProfileResponse | null> {
  const response = await fetch(`${API_BASE_URL}/students/me`, {
    headers: authHeaders(),
  });

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error("Unable to load your student profile.");
  }

  return response.json();
}

export async function createStudentProfile(
  data: StudentProfileRequest
): Promise<StudentProfileResponse> {
  const response = await fetch(`${API_BASE_URL}/students`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      typeof error?.detail === "string"
        ? error.detail
        : "Unable to save your academic profile."
    );
  }

  return response.json();
}


export type AcademicResultRequest = {
  subject: string;
  grade: string;
};

export type CredentialRequest = {
  credential_type: string;
  results: AcademicResultRequest[];
};

export type SavedAcademicResult = {
  id: number;
  subject: string;
  grade: string;
};

export type CredentialResponse = {
  id: number;
  student_id: number;
  country: string;
  credential_type: string;
  results: SavedAcademicResult[];
};

export async function getStudentCredentials(): Promise<CredentialResponse[]> {
  const response = await fetch(`${API_BASE_URL}/students/me/credentials`, {
    headers: authHeaders(),
  });

  if (!response.ok) {
    throw new Error("Unable to load your examination results.");
  }

  return response.json();
}

export async function saveStudentCredentials(
  studentIndex: string,
  data: CredentialRequest
): Promise<CredentialResponse> {
  const response = await fetch(
    `${API_BASE_URL}/students/${encodeURIComponent(studentIndex)}/credentials`,
    {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      typeof error?.detail === "string"
        ? error.detail
        : "Unable to save your examination results."
    );
  }

  return response.json();
}


export async function updateStudentCredentials(
  studentIndex: string,
  credentialId: number,
  data: CredentialRequest
): Promise<CredentialResponse> {
  const response = await fetch(
    `${API_BASE_URL}/students/${encodeURIComponent(studentIndex)}/credentials/${credentialId}`,
    {
      method: "PUT",
      headers: authHeaders(),
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      typeof error?.detail === "string"
        ? error.detail
        : "Unable to update your examination results."
    );
  }

  return response.json();
}


export async function updateStudentProfile(
  data: { education_level: string }
): Promise<StudentProfileResponse> {
  const response = await fetch(
    `${API_BASE_URL}/students/me`,
    {
      method: "PATCH",
      headers: authHeaders(),
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      typeof error?.detail === "string"
        ? error.detail
        : "Unable to update your academic background."
    );
  }

  return response.json();
}

export async function getRecommendations(
  intendedMajor: string,
  useAi: boolean = true
): Promise<RecommendationResponse> {
  const params = new URLSearchParams({
    use_ai: String(useAi),
  });

  if (intendedMajor.trim()) {
    params.set("intended_major", intendedMajor.trim());
  }

  const response = await fetch(
    `${API_BASE_URL}/recommendations/me?${params.toString()}`,
    {
      headers: authHeaders(),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      typeof error?.detail === "string"
        ? error.detail
        : "Unable to generate university recommendations."
    );
  }

  return response.json();
}