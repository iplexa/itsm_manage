import { Trash2 } from "lucide-react";
import type { TaskRead } from "../types/task";
import StatusBadge from "./StatusBadge";

const SERVICE_LABELS: Record<string, string> = {
  EDU_SERVICE: "Учебный процесс",
  IU_SERVICE: "ИУ",
  VKS_SERVICE: "ВКС",
  MOUNT_SERVICE: "Монтаж",
  MODPC_SERVICE: "МодПК",
  REGWORKS_SERVICE: "Регламент",
};

function formatDate(iso: string | null) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

interface Props {
  tasks: TaskRead[];
  showStatus?: boolean;
  onDelete?: (taskId: number) => void;
  streamStatuses?: Map<number, { status: string; itsm_request_id: string | null; error: string | null }>;
}

export default function TaskTable({ tasks, showStatus, onDelete, streamStatuses }: Props) {
  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-gray-400">
        <p className="text-sm">Задач нет — добавьте через шаблон или AI Import</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-200 text-left text-xs text-gray-500 uppercase tracking-wide">
            <th className="py-2 pr-3 font-medium w-8">#</th>
            <th className="py-2 pr-3 font-medium">Название</th>
            <th className="py-2 pr-3 font-medium w-36">Сервис</th>
            <th className="py-2 pr-3 font-medium w-16 text-right">Мин</th>
            <th className="py-2 pr-3 font-medium w-32">Дата закрытия</th>
            {showStatus && <th className="py-2 pr-3 font-medium w-28">Статус</th>}
            {onDelete && <th className="py-2 w-8" />}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {tasks.map((task, i) => {
            const live = streamStatuses?.get(task.id);
            const status = live?.status ?? task.status;
            const reqId = live?.itsm_request_id ?? task.itsm_request_id;
            const error = live?.error ?? task.error;

            return (
              <tr key={task.id} className="hover:bg-gray-50 group">
                <td className="py-2.5 pr-3 text-gray-400">{i + 1}</td>
                <td className="py-2.5 pr-3">
                  <div className="font-medium text-gray-900 leading-snug">{task.name}</div>
                  {reqId && (
                    <div className="text-xs text-blue-600 mt-0.5">
                      <a
                        href={`https://help.ranepa.ru/record/itsm_request/${reqId}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:underline"
                      >
                        REQ #{reqId}
                      </a>
                    </div>
                  )}
                  {error && (
                    <div className="text-xs text-red-500 mt-0.5 truncate max-w-xs" title={error}>
                      {error}
                    </div>
                  )}
                </td>
                <td className="py-2.5 pr-3 text-gray-500 text-xs">
                  {SERVICE_LABELS[task.service] ?? task.service}
                </td>
                <td className="py-2.5 pr-3 text-right tabular-nums text-gray-600">
                  {task.time_minutes}
                </td>
                <td className="py-2.5 pr-3 text-gray-500 text-xs">
                  {formatDate(task.closure_date)}
                </td>
                {showStatus && (
                  <td className="py-2.5 pr-3">
                    <StatusBadge status={status} type="task" />
                  </td>
                )}
                {onDelete && (
                  <td className="py-2.5">
                    <button
                      onClick={() => onDelete(task.id)}
                      className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-red-50 text-gray-400 hover:text-red-500 transition-all"
                    >
                      <Trash2 size={14} />
                    </button>
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
