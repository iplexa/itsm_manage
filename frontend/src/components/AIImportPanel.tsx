import { useState } from "react";
import { Sparkles } from "lucide-react";
import { importLinks } from "../api/import_";
import type { TaskCreate } from "../types/task";

const SERVICE_LABELS: Record<string, string> = {
  EDU_SERVICE: "Учебный процесс",
  IU_SERVICE: "ИУ",
  VKS_SERVICE: "ВКС",
  MOUNT_SERVICE: "Монтаж",
  MODPC_SERVICE: "МодПК",
  REGWORKS_SERVICE: "Регламент",
};

interface Props {
  onAdd: (tasks: TaskCreate[]) => Promise<void>;
}

export default function AIImportPanel({ onAdd }: Props) {
  const [links, setLinks] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<TaskCreate[]>([]);
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [adding, setAdding] = useState(false);

  async function handleParse() {
    const linkList = links
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);

    if (linkList.length === 0) return;
    setError(null);
    setLoading(true);
    setResults([]);
    setSelected(new Set());

    try {
      const tasks = await importLinks(linkList);
      setResults(tasks);
      setSelected(new Set(tasks.map((_, i) => i)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  function toggleAll() {
    if (selected.size === results.length) {
      setSelected(new Set());
    } else {
      setSelected(new Set(results.map((_, i) => i)));
    }
  }

  async function handleAdd() {
    const toAdd = results.filter((_, i) => selected.has(i));
    if (toAdd.length === 0) return;
    setAdding(true);
    try {
      await onAdd(toAdd);
      setResults([]);
      setLinks("");
      setSelected(new Set());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка добавления");
    } finally {
      setAdding(false);
    }
  }

  return (
    <div className="flex flex-col h-full space-y-3">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
        AI Import
      </p>

      <textarea
        value={links}
        onChange={(e) => setLinks(e.target.value)}
        placeholder={"https://help.ranepa.ru/record/itsm_request/177...\nhttps://help.ranepa.ru/record/itsm_request/177..."}
        className="w-full flex-shrink-0 rounded-lg border border-gray-300 px-3 py-2 text-xs text-gray-700 placeholder-gray-300 focus:outline-none focus:border-blue-500 resize-none"
        rows={5}
      />

      <button
        onClick={handleParse}
        disabled={loading || !links.trim()}
        className="flex items-center justify-center gap-2 rounded-lg bg-purple-600 py-2 text-sm font-medium text-white hover:bg-purple-700 disabled:opacity-40 transition-colors"
      >
        <Sparkles size={14} />
        {loading ? "Разбираю…" : "Разобрать"}
      </button>

      {error && (
        <p className="text-xs text-red-500 break-words">{error}</p>
      )}

      {results.length > 0 && (
        <div className="flex flex-col gap-2 overflow-y-auto flex-1 min-h-0">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-gray-600">
              {results.length} задач
            </span>
            <button
              onClick={toggleAll}
              className="text-xs text-blue-600 hover:underline"
            >
              {selected.size === results.length ? "Снять все" : "Выбрать все"}
            </button>
          </div>

          <div className="space-y-1.5 overflow-y-auto">
            {results.map((task, i) => (
              <label
                key={i}
                className={`flex items-start gap-2 rounded-lg border px-2.5 py-2 cursor-pointer transition-colors ${
                  selected.has(i)
                    ? "border-blue-300 bg-blue-50"
                    : "border-gray-200 bg-white"
                }`}
              >
                <input
                  type="checkbox"
                  checked={selected.has(i)}
                  onChange={(e) => {
                    const next = new Set(selected);
                    if (e.target.checked) next.add(i);
                    else next.delete(i);
                    setSelected(next);
                  }}
                  className="mt-0.5 rounded border-gray-300 shrink-0"
                />
                <div className="min-w-0">
                  <div className="text-xs font-medium text-gray-800 leading-snug">
                    {task.name}
                  </div>
                  <div className="text-xs text-gray-400 mt-0.5">
                    {SERVICE_LABELS[task.service] ?? task.service} · {task.time_minutes} мин
                  </div>
                </div>
              </label>
            ))}
          </div>

          <button
            onClick={handleAdd}
            disabled={adding || selected.size === 0}
            className="rounded-lg bg-blue-600 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-40 shrink-0"
          >
            {adding ? "Добавляю…" : `Добавить ${selected.size} задач`}
          </button>
        </div>
      )}
    </div>
  );
}
