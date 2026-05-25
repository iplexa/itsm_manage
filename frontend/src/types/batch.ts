import type { TaskRead } from "./task";

export type BatchStatus = "draft" | "running" | "done" | "failed";

export interface BatchRead {
  id: number;
  name: string;
  status: BatchStatus;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
  error: string | null;
  tasks_count: number;
}

export interface BatchDetail extends BatchRead {
  tasks: TaskRead[];
}
