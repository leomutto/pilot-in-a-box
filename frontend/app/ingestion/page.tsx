"use client";

import { useState } from "react";
import {
  validateRequest,
  normalizeRequest,
  saveRequest,
  sendToBlackbox,
  getRequest,
  getLogs,
} from "@/services/ingestionApi";

export default function IngestionPage() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState<any>(null);
  const [requestId, setRequestId] = useState<number | null>(null);

  async function handleValidate() {
    const json = JSON.parse(input);
    const res = await validateRequest(json);
    setOutput(res);
  }

  async function handleNormalize() {
    const json = JSON.parse(input);
    const res = await normalizeRequest(json);
    setOutput(res);
  }

  async function handleSave() {
    const json = JSON.parse(input);
    const res = await saveRequest(json);
    setRequestId(res.request_db_id);
    setOutput(res);
  }

  async function handleSend() {
    if (!requestId) return;
    const res = await sendToBlackbox(requestId);
    setOutput(res);
  }

  async function handleGet() {
    if (!requestId) return;
    const res = await getRequest(requestId);
    setOutput(res);
  }

  async function handleLogs() {
    if (!requestId) return;
    const res = await getLogs(requestId);
    setOutput(res);
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Ingestion Pipeline</h1>

      <textarea
        rows={20}
        style={{ width: "100%" }}
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <div style={{ marginTop: 20 }}>
        <button onClick={handleValidate}>Validate</button>
        <button onClick={handleNormalize}>Normalize</button>
        <button onClick={handleSave}>Save</button>
        <button onClick={handleSend}>Send</button>
        <button onClick={handleGet}>Get</button>
        <button onClick={handleLogs}>Logs</button>
      </div>

      <pre style={{ marginTop: 20 }}>
        {output ? JSON.stringify(output, null, 2) : ""}
      </pre>
    </div>
  );
}