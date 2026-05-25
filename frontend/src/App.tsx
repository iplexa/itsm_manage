import { Routes, Route, Navigate } from "react-router-dom";
import BatchList from "./pages/BatchList";
import BatchEditor from "./pages/BatchEditor";
import RunProgress from "./pages/RunProgress";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<BatchList />} />
      <Route path="/batches/:id" element={<BatchEditor />} />
      <Route path="/batches/:id/run" element={<RunProgress />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
