import { useEffect, useState } from "react";

export interface TaskStreamEvent {
  task_id: number;
  name: string;
  status: string;
  itsm_request_id: string | null;
  error: string | null;
}

interface BatchDoneEvent {
  status: string;
  error: string | null;
}

export function useBatchStream(batchId: number) {
  const [taskEvents, setTaskEvents] = useState<Map<number, TaskStreamEvent>>(
    new Map(),
  );
  const [batchDone, setBatchDone] = useState<BatchDoneEvent | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const es = new EventSource(`/api/batches/${batchId}/stream`);
    setConnected(true);

    es.addEventListener("task_update", (e) => {
      const event: TaskStreamEvent = JSON.parse(e.data);
      setTaskEvents((prev) => new Map(prev).set(event.task_id, event));
    });

    es.addEventListener("batch_done", (e) => {
      const event: BatchDoneEvent = JSON.parse(e.data);
      setBatchDone(event);
      es.close();
      setConnected(false);
    });

    es.onerror = () => {
      setConnected(false);
    };

    return () => {
      es.close();
    };
  }, [batchId]);

  return { taskEvents, batchDone, connected };
}
