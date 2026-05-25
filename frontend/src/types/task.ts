export type TaskStatus =
  | "draft"
  | "pending"
  | "running"
  | "done"
  | "failed"
  | "skipped";

export interface TaskRead {
  id: number;
  batch_id: number;
  name: string;
  desc: string;
  service: string;
  time_minutes: number;
  closure_text: string;
  closure_date: string | null;
  status: TaskStatus;
  itsm_request_id: string | null;
  error: string | null;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  name: string;
  desc: string;
  service: string;
  time_minutes: number;
  closure_text: string;
  closure_date: string | null;
}
