import { useNavigate, useParams } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, Play, AlertCircle } from "lucide-react";
import { fetchBatch, runBatch } from "../api/batches";
import { createTask, deleteTask } from "../api/tasks";
import StatusBadge from "../components/StatusBadge";
import TaskTable from "../components/TaskTable";
import TemplatePanel from "../components/TemplatePanel";
import AIImportPanel from "../components/AIImportPanel";
import type { TaskCreate } from "../types/task";

export default function BatchEditor() {
  const { id } = useParams<{ id: string }>();
  const batchId = Number(id);
  const navigate = useNavigate();
  const qc = useQueryClient();

  const { data: batch, isLoading, error } = useQuery({
    queryKey: ["batch", batchId],
    queryFn: () => fetchBatch(batchId),
    refetchInterval: (q) =>
      q.state.data?.status === "running" ? 3000 : false,
  });

  const runMut = useMutation({
    mutationFn: () => runBatch(batchId),
    onSuccess: () => navigate(`/batches/${batchId}/run`),
  });

  const deleteMut = useMutation({
    mutationFn: (taskId: number) => deleteTask(batchId, taskId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["batch", batchId] }),
  });

  async function addTasks(tasks: TaskCreate[]) {
    for (const task of tasks) {
      await createTask(batchId, task);
    }
    qc.invalidateQueries({ queryKey: ["batch", batchId] });
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen text-gray-400 text-sm">
        Загрузка…
      </div>
    );
  }

  if (error || !batch) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-3">
        <AlertCircle className="text-red-400" size={32} />
        <p className="text-gray-600 text-sm">Батч не найден</p>
        <button
          onClick={() => navigate("/")}
          className="text-blue-600 text-sm hover:underline"
        >
          ← Назад
        </button>
      </div>
    );
  }

  const isRunning = batch.status === "running";
  const canRun = batch.status !== "running" && batch.tasks.length > 0;
  const sortedTasks = [...batch.tasks].sort(
    (a, b) => a.sort_order - b.sort_order || a.id - b.id,
  );

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-4 shrink-0">
        <button
          onClick={() => navigate("/")}
          className="text-gray-400 hover:text-gray-700 transition-colors"
        >
          <ArrowLeft size={18} />
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h1 className="text-base font-semibold text-gray-900 truncate">
              {batch.name}
            </h1>
            <StatusBadge status={batch.status} type="batch" />
          </div>
          <p className="text-xs text-gray-400">
            {batch.tasks_count} задач
            {batch.error && (
              <span className="ml-2 text-red-400">· {batch.error}</span>
            )}
          </p>
        </div>

        {isRunning ? (
          <button
            onClick={() => navigate(`/batches/${batchId}/run`)}
            className="flex items-center gap-1.5 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Смотреть прогресс
          </button>
        ) : (
          <button
            onClick={() => {
              if (confirm(`Запустить батч «${batch.name}» (${batch.tasks_count} задач)?`)) {
                runMut.mutate();
              }
            }}
            disabled={!canRun || runMut.isPending}
            className="flex items-center gap-1.5 rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            <Play size={14} />
            {runMut.isPending ? "Запускаю…" : "Запустить"}
          </button>
        )}
      </header>

      {runMut.isError && (
        <div className="bg-red-50 border-b border-red-200 px-6 py-2 text-sm text-red-600">
          {runMut.error?.message ?? "Ошибка запуска"}
        </div>
      )}

      {/* 3-column layout */}
      <div className="flex flex-1 min-h-0 overflow-hidden">
        {/* Left: Templates */}
        <aside className="w-56 shrink-0 border-r border-gray-200 bg-white px-4 py-4 overflow-y-auto">
          <TemplatePanel onAdd={addTasks} />
        </aside>

        {/* Center: Task table */}
        <main className="flex-1 min-w-0 overflow-y-auto px-6 py-4">
          <TaskTable
            tasks={sortedTasks}
            showStatus={batch.status !== "draft"}
            onDelete={
              !isRunning ? (taskId) => deleteMut.mutate(taskId) : undefined
            }
          />
        </main>

        {/* Right: AI Import */}
        <aside className="w-72 shrink-0 border-l border-gray-200 bg-white px-4 py-4 overflow-y-auto flex flex-col">
          <AIImportPanel onAdd={addTasks} />
        </aside>
      </div>
    </div>
  );
}
