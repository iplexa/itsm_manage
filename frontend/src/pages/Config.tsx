import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, CheckCircle2, XCircle } from "lucide-react";
import { fetchConfig } from "../api/config";
import type { ConfigStatus } from "../types/config";

const CONFIG_LABELS: { key: keyof ConfigStatus; label: string }[] = [
  { key: "itsm_base_url_set",    label: "ITSM_BASE_URL" },
  { key: "bearer_token_set",     label: "BEARER_TOKEN" },
  { key: "cookies_set",          label: "COOKIES" },
  { key: "assigned_user_set",    label: "ASSIGNED_USER" },
  { key: "deepseek_api_key_set", label: "DEEPSEEK_API_KEY" },
  { key: "database_url_set",     label: "DATABASE_URL" },
  { key: "redis_url_set",        label: "REDIS_URL" },
];

export default function Config() {
  const navigate = useNavigate();
  const { data, isLoading } = useQuery({
    queryKey: ["config"],
    queryFn: fetchConfig,
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-4">
        <button onClick={() => navigate("/")} className="text-gray-400 hover:text-gray-700">
          <ArrowLeft size={18} />
        </button>
        <h1 className="text-base font-semibold text-gray-900">Конфигурация</h1>
      </header>

      <main className="max-w-lg mx-auto px-6 py-8">
        <p className="text-xs text-gray-400 mb-6">
          Показывает, заданы ли переменные окружения. Значения не отображаются.
        </p>

        {isLoading ? (
          <div className="text-sm text-gray-400">Загрузка…</div>
        ) : data ? (
          <div className="bg-white rounded-xl border border-gray-200 divide-y divide-gray-100">
            {CONFIG_LABELS.map(({ key, label }) => (
              <div key={key} className="flex items-center justify-between px-5 py-3">
                <span className="font-mono text-sm text-gray-700">{label}</span>
                {data[key] ? (
                  <span className="flex items-center gap-1.5 text-green-600 text-xs font-medium">
                    <CheckCircle2 size={14} />
                    Задано
                  </span>
                ) : (
                  <span className="flex items-center gap-1.5 text-red-500 text-xs font-medium">
                    <XCircle size={14} />
                    Не задано
                  </span>
                )}
              </div>
            ))}
          </div>
        ) : null}
      </main>
    </div>
  );
}
