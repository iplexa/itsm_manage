import { useNavigate, useParams } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, CheckCircle2, XCircle, Clock, Loader2, RotateCcw, SkipForward } from "lucide-react";
import { fetchBatch } from "../api/batches";
import { retryTask, skipTask } from "../api/tasks";
import { useBatchStream } from "../hooks/useBatchStream";
import StatusBadge from "../components/StatusBadge";
import type { TaskRead } from "../types/task";

function TaskIcon({ status }: { status: string }) {
  switch (status) {
    case "done":    return <CheckCircle2 size={16} className="text-green-500 shrink-0" />;
    case "failed":  return <XCircle size={16} className="text-red-500 shrink-0" />;
    case "running": return <Loader2 size={16} className="text-blue-500 animate-spin shrink-0" />;
    case "skipped": return <Clock size={16} className="text-gray-300 shrink-0" />;
    default:        return <Clock size={16} className="text-gray-300 shrink-0" />;
  }
}

export default function RunProgress() {
  const { id } = useParams<{ id: string }>();
  const batchId = Number(id);
  const navigate = useNavigate();
  const qc = useQueryClient();

  const { data: batch, isLoading } = useQuery({
    queryKey: ["batch", batchId],
    queryFn: () => fetchBatch(batchId),
  });

  const { taskEvents, batchDone, connected } = useBatchStream(batchId);

  const retryMut = useMutation({
    mutationFn: (taskId: number) => retryTask(batchId, taskId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["batch", batchId] }),
  });

  const skipMut = useMutation({
    mutationFn: (taskId: number) => skipTask(batchId, taskId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["batch", batchId] }),
  });

  if (isLoading || !batch) {
    return (
      <div className="flex items-center justify-center min-h-screen text-gray-400 text-sm">
        Загрузка…
      </div>
    );
  }

  const sortedTasks = [...batch.tasks].sort(
    (a, b) => a.sort_order - b.sort_order || a.id - b.id,
  );

  const doneCount = sortedTasks.filter((t) => {
    const live = taskEvents.get(t.id);
    return (live?.status ?? t.status) === "done";
  }).length;

  const failedCount = sortedTasks.filter((t) => {
    const live = taskEvents.get(t.id);
    return (live?.status ?? t.status) === "failed";
  }).length;

  const finalStatus = batchDone?.status ?? batch.status;
  const isFinished = batchDone || ["done", "failed"].includes(batch.status);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-4">
        <button
          onClick={() => navigate(`/batches/${batchId}`)}
          className="text-gray-400 hover:text-gray-700"
        >
          <ArrowLeft size={18} />
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h1 className="text-base font-semibold text-gray-900 truncate">{batch.name}</h1>
            <StatusBadge status={finalStatus} type="batch" />
            {connected && (
              <span className="flex items-center gap-1 text-xs text-green-600">
                <span className="inline-block w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                Live
              </span>
            )}
          </div>
          <p className="text-xs text-gray-400">
            {doneCount} / {sortedTasks.length} выполнено
            {failedCount > 0 && (
              <span className="ml-2 text-red-400">· {failedCount} ошибок</span>
            )}
          </p>
        </div>

        {isFinished && (
          <button
            onClick={() => navigate("/")}
            className="rounded-lg border border-gray-300 px-4 py-2 text-sm text-gray-600 hover:bg-gray-50"
          >
            К списку
          </button>
        )}
      </header>

      {/* Progress bar */}
      <div className="h-1 bg-gray-200">
        <div
          className={`h-full transition-all duration-500 ${
            failedCount > 0 ? "bg-red-500" : "bg-green-500"
          }`}
          style={{
            width: sortedTasks.length > 0
              ? `${((doneCount + failedCount) / sortedTasks.length) * 100}%`
              : "0%",
          }}
        />
      </div>

      {/* Final status banner */}
      {batchDone && (
        <div
          className={`px-6 py-3 text-sm font-medium ${
            batchDone.status === "done"
              ? "bg-green-50 text-green-700 border-b border-green-200"
              : "bg-red-50 text-red-700 border-b border-red-200"
          }`}
        >
          {batchDone.status === "done"
            ? `Батч выполнен. ${doneCount} задач создано.`
            : `Батч завершился с ошибкой. ${batchDone.error ?? ""}`}
        </div>
      )}

      {/* Task list */}
      <main className="max-w-3xl mx-auto px-6 py-6 space-y-2">
        {sortedTasks.map((task: TaskRead, i: number) => {
          const live = taskEvents.get(task.id);
          const status = live?.status ?? task.status;
          const reqId = live?.itsm_request_id ?? task.itsm_request_id;
          const error = live?.error ?? task.error;
          const canRetry = isFinished && status === "failed";
          const canSkip = isFinished && status !== "done" && status !== "skipped";

          return (
            <div
              key={task.id}
              className={`flex items-start gap-3 rounded-xl border bg-white px-4 py-3 transition-all ${
                status === "running"
                  ? "border-blue-300 shadow-sm"
                  : status === "done"
                  ? "border-green-200"
                  : status === "failed"
                  ? "border-red-200"
                  : "border-gray-200"
              }`}
            >
              <span className="text-xs text-gray-300 w-5 pt-0.5 text-right shrink-0">
                {i + 1}
              </span>
              <TaskIcon status={status} />

              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-gray-900">{task.name}</div>
                {reqId && (
                  <a
                    href={`https://help.ranepa.ru/record/itsm_request/${reqId}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-blue-600 hover:underline mt-0.5 block"
                  >
                    REQ #{reqId}
                  </a>
                )}
                {error && (
                  <p className="text-xs text-red-500 mt-0.5">{error}</p>
                )}
              </div>

              <div className="flex items-center gap-1 shrink-0">
                <span className="text-xs text-gray-400">
                  {task.time_minutes} мин
                </span>
                {canRetry && (
                  <button
                    onClick={() => retryMut.mutate(task.id)}
                    disabled={retryMut.isPending}
                    title="Повторить"
                    className="ml-1 p-1 rounded hover:bg-blue-50 text-gray-400 hover:text-blue-600 transition-colors"
                  >
                    <RotateCcw size={13} />
                  </button>
                )}
                {canSkip && (
                  <button
                    onClick={() => skipMut.mutate(task.id)}
                    disabled={skipMut.isPending}
                    title="Пропустить"
                    className="p-1 rounded hover:bg-yellow-50 text-gray-400 hover:text-yellow-600 transition-colors"
                  >
                    <SkipForward size={13} />
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </main>
    </div>
  );
}
