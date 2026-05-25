import type { BatchStatus } from "../types/batch";
import type { TaskStatus } from "../types/task";

const BATCH_CONFIG: Record<BatchStatus, { label: string; cls: string }> = {
  draft:   { label: "Черновик",    cls: "bg-gray-100 text-gray-600" },
  running: { label: "Выполняется", cls: "bg-blue-100 text-blue-700 animate-pulse" },
  done:    { label: "Готово",      cls: "bg-green-100 text-green-700" },
  failed:  { label: "Ошибка",      cls: "bg-red-100 text-red-700" },
};

const TASK_CONFIG: Record<string, { label: string; cls: string }> = {
  draft:   { label: "Черновик",    cls: "bg-gray-100 text-gray-500" },
  pending: { label: "Ожидает",     cls: "bg-yellow-100 text-yellow-700" },
  running: { label: "Выполняется", cls: "bg-blue-100 text-blue-700 animate-pulse" },
  done:    { label: "Готово",      cls: "bg-green-100 text-green-700" },
  failed:  { label: "Ошибка",      cls: "bg-red-100 text-red-700" },
  skipped: { label: "Пропущена",   cls: "bg-gray-100 text-gray-400" },
};

interface Props {
  status: BatchStatus | TaskStatus | string;
  type?: "batch" | "task";
}

export default function StatusBadge({ status, type = "batch" }: Props) {
  const cfg =
    type === "batch"
      ? (BATCH_CONFIG[status as BatchStatus] ?? { label: status, cls: "bg-gray-100 text-gray-600" })
      : (TASK_CONFIG[status] ?? { label: status, cls: "bg-gray-100 text-gray-600" });

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${cfg.cls}`}
    >
      {cfg.label}
    </span>
  );
}
