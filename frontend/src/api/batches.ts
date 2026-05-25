import api from "./client";
import type { BatchDetail, BatchRead } from "../types/batch";

export const fetchBatches = async (): Promise<BatchRead[]> => {
  const { data } = await api.get<BatchRead[]>("/batches");
  return data;
};

export const fetchBatch = async (id: number): Promise<BatchDetail> => {
  const { data } = await api.get<BatchDetail>(`/batches/${id}`);
  return data;
};

export const createBatch = async (name: string): Promise<BatchRead> => {
  const { data } = await api.post<BatchRead>("/batches", { name });
  return data;
};

export const deleteBatch = async (id: number): Promise<void> => {
  await api.delete(`/batches/${id}`);
};

export const runBatch = async (id: number): Promise<void> => {
  await api.post(`/batches/${id}/run`);
};
