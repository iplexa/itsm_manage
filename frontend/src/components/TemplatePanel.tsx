import { useState } from "react";
import { X } from "lucide-react";
import { importTemplate } from "../api/import_";
import type { TaskCreate } from "../types/task";

interface Template {
  id: string;
  label: string;
  desc: string;
  hasDateEnd: boolean;
  hasTimeMinutes: boolean;
  hasMountOptions: boolean;
}

const TEMPLATES: Template[] = [
  { id: "iu_tasks", label: "ИУ",       desc: "Монтаж + сопровождение + демонтаж", hasDateEnd: true,  hasTimeMinutes: false, hasMountOptions: true  },
  { id: "vks",      label: "ВКС",      desc: "Видеоконференцсвязь",                hasDateEnd: true,  hasTimeMinutes: false, hasMountOptions: true  },
  { id: "regworks", label: "Регламент",desc: "Регламентные работы",                hasDateEnd: false, hasTimeMinutes: true,  hasMountOptions: false },
  { id: "rooms1",   label: "Обход П/1",desc: "Регламентный обход П/1",             hasDateEnd: false, hasTimeMinutes: true,  hasMountOptions: false },
  { id: "rooms2",   label: "Обход П/2",desc: "Регламентный обход П/2",             hasDateEnd: false, hasTimeMinutes: true,  hasMountOptions: false },
  { id: "mount",    label: "Монтаж",   desc: "Монтаж оборудования",               hasDateEnd: false, hasTimeMinutes: true,  hasMountOptions: false },
  { id: "modpc",    label: "МодПК",    desc: "Модернизация ПК",                    hasDateEnd: false, hasTimeMinutes: true,  hasMountOptions: false },
];

interface Props {
  onAdd: (tasks: TaskCreate[]) => Promise<void>;
}

export default function TemplatePanel({ onAdd }: Props) {
  const [active, setActive] = useState<Template | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [audience, setAudience] = useState("");
  const [dateStart, setDateStart] = useState("");
  const [dateEnd, setDateEnd] = useState("");
  const [timeMinutes, setTimeMinutes] = useState(60);
  const [needMount, setNeedMount] = useState(true);
  const [needSupport, setNeedSupport] = useState(true);
  const [needDismount, setNeedDismount] = useState(true);

  function openTemplate(t: Template) {
    setActive(t);
    setError(null);
    setAudience("");
    setDateStart("");
    setDateEnd("");
    setTimeMinutes(60);
    setNeedMount(true);
    setNeedSupport(true);
    setNeedDismount(true);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!active) return;
    setError(null);
    setLoading(true);

    const params: Record<string, unknown> = {
      audience,
      date_start: dateStart,
      date_end: active.hasDateEnd ? dateEnd : dateStart,
      time_minutes: timeMinutes,
    };
    if (active.hasMountOptions) {
      params.need_mount   = needMount;
      params.need_support = needSupport;
      params.need_dismount = needDismount;
    }

    try {
      const tasks = await importTemplate(active.id, params);
      await onAdd(tasks);
      setActive(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="space-y-1.5">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
          Шаблоны
        </p>
        {TEMPLATES.map((t) => (
          <button
            key={t.id}
            onClick={() => openTemplate(t)}
            className="w-full text-left rounded-lg border border-gray-200 bg-white px-3 py-2.5 hover:border-blue-400 hover:bg-blue-50 transition-colors"
          >
            <div className="font-medium text-sm text-gray-800">{t.label}</div>
            <div className="text-xs text-gray-400 mt-0.5">{t.desc}</div>
          </button>
        ))}
      </div>

      {/* Modal */}
      {active && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md mx-4 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-semibold">{active.label}</h2>
              <button onClick={() => setActive(null)} className="text-gray-400 hover:text-gray-700">
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Аудитория</label>
                <input
                  required
                  value={audience}
                  onChange={(e) => setAudience(e.target.value)}
                  placeholder="П/2 305"
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">
                  {active.hasDateEnd ? "Начало" : "Дата"}
                </label>
                <input
                  required
                  type="datetime-local"
                  value={dateStart}
                  onChange={(e) => setDateStart(e.target.value)}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                />
              </div>

              {active.hasDateEnd && (
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Конец</label>
                  <input
                    required
                    type="datetime-local"
                    value={dateEnd}
                    onChange={(e) => setDateEnd(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  />
                </div>
              )}

              {active.hasTimeMinutes && (
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Время (минут)</label>
                  <input
                    required
                    type="number"
                    min={5}
                    max={480}
                    value={timeMinutes}
                    onChange={(e) => setTimeMinutes(Number(e.target.value))}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  />
                </div>
              )}

              {active.hasMountOptions && (
                <div className="flex gap-4">
                  {[
                    { key: "needMount",    label: "Монтаж",       val: needMount,    set: setNeedMount },
                    { key: "needSupport",  label: "Сопровождение",val: needSupport,  set: setNeedSupport },
                    { key: "needDismount", label: "Демонтаж",     val: needDismount, set: setNeedDismount },
                  ].map(({ key, label, val, set }) => (
                    <label key={key} className="flex items-center gap-1.5 text-sm text-gray-700 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={val}
                        onChange={(e) => set(e.target.checked)}
                        className="rounded border-gray-300"
                      />
                      {label}
                    </label>
                  ))}
                </div>
              )}

              {error && <p className="text-xs text-red-500">{error}</p>}

              <div className="flex gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setActive(null)}
                  className="flex-1 rounded-lg border border-gray-300 py-2 text-sm text-gray-600 hover:bg-gray-50"
                >
                  Отмена
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 rounded-lg bg-blue-600 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? "Добавляю…" : "Добавить в батч"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
