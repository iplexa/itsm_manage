import api from "./client";
import type { TaskCreate } from "../types/task";

export const importTemplate = async (
  template: string,
  params: Record<string, unknown>,
): Promise<TaskCreate[]> => {
  const { data } = await api.post<{ tasks: TaskCreate[] }>("/import/template", {
    template,
    params,
  });
  return data.tasks;
};

export const importLinks = async (links: string[]): Promise<TaskCreate[]> => {
  const { data } = await api.post<{ tasks: TaskCreate[] }>("/import/links", {
    links,
  });
  return data.tasks;
};
