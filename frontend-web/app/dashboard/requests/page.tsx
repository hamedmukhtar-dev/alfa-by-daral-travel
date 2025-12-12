"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function RequestsPage() {
  const [serviceType, setServiceType] = useState("");
  const [details, setDetails] = useState("");
  const [requestId, setRequestId] = useState<number | null>(null);
  const [method, setMethod] = useState("cash");
  const [reference, setReference] = useState("");
  const [message, setMessage] = useState("");

  const createRequest = async () => {
    // Demo request creation (replace with real API if needed)
    setRequestId(1);
    setMessage("Service request created. Please confirm offline payment.");
  };

  const submitOfflinePayment = async () => {
    try {
      await api.post("/offline-payments/submit", {
        service_request_id: requestId,
        payment_method: method,
        reference_note: reference,
      });
      setMessage("Offline payment submitted successfully.");
    } catch (err) {
      setMessage("Error submitting offline payment.");
    }
  };

  return (
    <main>
      <h3>Create Service Request</h3>

      <input
        placeholder="Service Type"
        value={serviceType}
        onChange={(e) => setServiceType(e.target.value)}
      />
      <br /><br />

      <textarea
        placeholder="Details"
        value={details}
        onChange={(e) => setDetails(e.target.value)}
      />
      <br /><br />

      <button onClick={createRequest}>Create Request</button>

      {requestId && (
        <>
          <hr />
          <h4>Confirm Offline Payment</h4>

          <select value={method} onChange={(e) => setMethod(e.target.value)}>
            <option value="cash">Cash</option>
            <option value="bank">Bank Transfer</option>
            <option value="agent">Agent</option>
          </select>
          <br /><br />

          <input
            placeholder="Reference / Note"
            value={reference}
            onChange={(e) => setReference(e.target.value)}
          />
          <br /><br />

          <button onClick={submitOfflinePayment}>
            Submit Offline Payment
          </button>
        </>
      )}

      {message && <p style={{ marginTop: 20 }}>{message}</p>}
    </main>
  );
}
