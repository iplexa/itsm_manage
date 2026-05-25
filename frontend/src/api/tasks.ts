import api from "./client";
import type { TaskCreate, TaskRead } from "../types/task";

export const createTask = async (
  batchId: number,
  task: TaskCreate,
): Promise<TaskRead> => {
  const { data } = await api.post<TaskRead>(`/batches/${batchId}/tasks`, task);
  return data;
};

export const deleteTask = async (
  batchId: number,
  taskId: number,
): Promise<void> => {
  await api.delete(`/batches/${batchId}/tasks/${taskId}`);
};
