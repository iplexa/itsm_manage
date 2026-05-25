import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Trash2, ChevronRight, Settings } from "lucide-react";
import { fetchBatches, createBatch, deleteBatch } from "../api/batches";
import StatusBadge from "../components/StatusBadge";
import type { BatchRead, BatchStatus } from "../types/batch";

const FILTERS: { label: string; value: BatchStatus | "all" }[] = [
  { label: "Все",         value: "all" },
  { label: "Черновики",   value: "draft" },
  { label: "Выполняются", value: "running" },
  { label: "Готово",      value: "done" },
  { label: "Ошибки",      value: "failed" },
];

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function BatchList() {
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [filter, setFilter] = useState<BatchStatus | "all">("all");
  const [newName, setNewName] = useState("");
  const [creating, setCreating] = useState(false);

  const { data: batches = [], isLoading } = useQuery({
    queryKey: ["batches"],
    queryFn: fetchBatches,
    refetchInterval: 5000,
  });

  const createMut = useMutation({
    mutationFn: (name: string) => createBatch(name),
    onSuccess: (batch) => {
      qc.invalidateQueries({ queryKey: ["batches"] });
      navigate(`/batches/${batch.id}`);
    },
  });

  const deleteMut = useMutation({
    mutationFn: (id: number) => deleteBatch(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["batches"] }),
  });

  const visible = filter === "all"
    ? batches
    : batches.filter((b) => b.status === filter);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    const name = newName.trim() || `Батч от ${new Date().toLocaleDateString("ru-RU")}`;
    await createMut.mutateAsync(name);
    setNewName("");
    setCreating(false);
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <h1 className="text-lg font-semibold text-gray-900">ITSM Manage</h1>
        <div className="flex items-center gap-2">
          <button
            onClick={() => navigate("/config")}
            className="p-2 rounded-lg text-gray-400 hover:text-gray-700 hover:bg-gray-100 transition-colors"
            title="Конфигурация"
          >
            <Settings size={16} />
          </button>
          <button
            onClick={() => setCreating(true)}
            className="flex items-center gap-1.5 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
          >
            <Plus size={15} />
            Новый батч
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-6">
        {/* Filters */}
        <div className="flex gap-1 mb-4">
          {FILTERS.map((f) => (
            <button
              key={f.value}
              onClick={() => setFilter(f.value)}
              className={`rounded-full px-3 py-1 text-sm font-medium transition-colors ${
                filter === f.value
                  ? "bg-gray-900 text-white"
                  : "text-gray-500 hover:text-gray-900 hover:bg-gray-100"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>

        {/* Create form */}
        {creating && (
          <form
            onSubmit={handleCreate}
            className="mb-4 flex gap-2 rounded-xl border border-blue-200 bg-blue-50 p-4"
          >
            <input
              autoFocus
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder={`Батч от ${new Date().toLocaleDateString("ru-RU")}`}
              className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
            />
            <button
              type="submit"
              disabled={createMut.isPending}
              className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
            >
              {createMut.isPending ? "Создаю…" : "Создать"}
            </button>
            <button
              type="button"
              onClick={() => setCreating(false)}
              className="rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-600 hover:bg-gray-50"
            >
              Отмена
            </button>
          </form>
        )}

        {/* Batch list */}
        {isLoading ? (
          <div className="py-12 text-center text-gray-400 text-sm">Загрузка…</div>
        ) : visible.length === 0 ? (
          <div className="py-12 text-center text-gray-400 text-sm">
            {filter === "all" ? "Батчей нет — создайте первый" : "Нет батчей с таким статусом"}
          </div>
        ) : (
          <div className="space-y-2">
            {visible.map((batch: BatchRead) => (
              <div
                key={batch.id}
                onClick={() =>
                  navigate(
                    batch.status === "running"
                      ? `/batches/${batch.id}/run`
                      : `/batches/${batch.id}`,
                  )
                }
                className="flex items-center gap-4 rounded-xl border border-gray-200 bg-white px-5 py-4 hover:border-blue-300 hover:shadow-sm cursor-pointer transition-all group"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-900 truncate">{batch.name}</span>
                    <StatusBadge status={batch.status} type="batch" />
                  </div>
                  <div className="text-xs text-gray-400 mt-1">
                    {batch.tasks_count} задач · {formatDate(batch.created_at)}
                    {batch.error && (
                      <span className="ml-2 text-red-400">· {batch.error}</span>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm(`Удалить батч «${batch.name}»?`)) {
                        deleteMut.mutate(batch.id);
                      }
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg hover:bg-red-50 text-gray-400 hover:text-red-500 transition-all"
                  >
                    <Trash2 size={15} />
                  </button>
                  <ChevronRight size={16} className="text-gray-300 group-hover:text-gray-500" />
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
