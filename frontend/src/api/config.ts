import api from "./client";
import type { ConfigStatus } from "../types/config";

export const fetchConfig = async (): Promise<ConfigStatus> => {
  const { data } = await api.get<ConfigStatus>("/config");
  return data;
};
