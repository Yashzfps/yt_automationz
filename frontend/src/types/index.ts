export type SourceConfig = { id: number; path: string; recursive: boolean };
export type Asset = {
  id: number;
  source_path: string;
  file_name: string;
  extension: string;
  size_bytes: number;
  duration_seconds: number | null;
  valid: boolean;
  invalid_reason: string | null;
  approval_state: string;
};

export type Job = {
  id: number;
  kind: string;
  status: string;
  stage: string;
  progress: number;
  error_message: string | null;
};
