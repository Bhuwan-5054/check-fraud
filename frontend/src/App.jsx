import { useState } from "react";
import axios from "axios";


export default function App() {
  const [url, setUrl] = useState("");
  const [emailText, setEmailText] = useState("");
  const [emailID, setEmailID] = useState("");
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const BASE_URL = "http://127.0.0.1:8000";

  const analyze = async (endpoint, payload, isForm = false) => {
    setLoading(true);
    try {
      const res = await axios.post(`${BASE_URL}/${endpoint}`, payload, isForm ? {} : {
        headers: { "Content-Type": "application/json" }
      });
      setResult(res.data);
    } catch (err) {
      console.error("API Error:", err);
      setResult({ status: "Error ❌", risk: 0, reasons: ["Server error or backend not running"] });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col justify-between">

      {/* HEADER */}
      <div className="p-6">
        <h1
          
          className="text-4xl font-bold text-center mb-2"
        >
          🚨 Check Fraud
        </h1>

        <p className="text-center text-gray-400 mb-8">
          Detect phishing, scams, and suspicious content instantly
        </p>

        {/* GRID */}
        <div className="grid md:grid-cols-2 gap-6">

          {/* URL */}
          <Card title="🔗 URL Scanner">
            <input
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter suspicious URL"
              className="input"
            />
            <Button onClick={() => analyze("check-url", { url })} />
          </Card>

          {/* EMAIL CONTENT */}
          <Card title="📧 Email Content">
            <textarea
              value={emailText}
              onChange={(e) => setEmailText(e.target.value)}
              placeholder="Paste email content"
              className="input"
            />
            <Button onClick={() => analyze("check-email", { content: emailText })} />
          </Card>

          {/* EMAIL ID */}
          <Card title="📨 Email ID">
            <input
              value={emailID}
              onChange={(e) => setEmailID(e.target.value)}
              placeholder="Enter email ID"
              className="input"
            />
            <Button onClick={() => analyze("check-email-id", { email: emailID })} />
          </Card>

          {/* IMAGE */}
          <Card title="🖼️ Screenshot Analyzer">
            <input
              type="file"
              onChange={(e) => setImage(e.target.files[0])}
              className="input"
            />
            <Button
              onClick={() => {
                if (!image) return alert("Upload image first");
                const formData = new FormData();
                formData.append("file", image);
                analyze("analyze-image", formData, true);
              }}
            />
          </Card>

        </div>

        {/* LOADING */}
        {loading && (
          <div className="text-center mt-6 animate-pulse">
            🔍 Analyzing...
          </div>
        )}

        {/* RESULT */}
        {result && (
          <div
           
            className="mt-8 p-5 bg-zinc-900 rounded-lg border border-zinc-700"
          >
            <h2 className="text-xl mb-2">📊 Result</h2>

            <p className="font-semibold">Status: {result.status}</p>
            <p>Risk Score: {result.risk}</p>

            <ul className="mt-2">
              {result.reasons?.map((r, i) => (
                <li key={i}>• {r}</li>
              ))}
            </ul>

            {result.text && (
              <div className="mt-3 text-sm text-gray-400">
                <h4>Extracted Text:</h4>
                <p>{result.text}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* FOOTER */}
      <footer className="text-center text-sm text-gray-400 p-4 border-t border-gray-700">
        <p>🚧 Beta Version v1.0.0</p>
        <p>This tool is under development. Results may not be fully accurate.</p>

        <div className="mt-3 space-x-4">
          <a href="https://github.com/Bhuwan-5054" target="_blank" className="hover:underline">GitHub  |   </a>
          <a href="https://www.linkedin.com/in/bhuwan-kirnapure-b3563a241/" target="_blank" className="hover:underline">LinkedIn   |  </a>
          <a href="mailto:bhuwankirnapure60@gmail.com" className="hover:underline">Contact   |   </a>
          <a href="#" className="hover:underline">Terms</a>
        </div>

        <p className="mt-2 text-xs">Made with ❤️ by You</p>
      </footer>
    </div>
  );
}

function Card({ title, children }) {
  return (
    <div className="bg-zinc-900 p-4 rounded-lg border border-zinc-800">
      <h2 className="mb-2 font-medium">{title}</h2>
      {children}
    </div>
  );
}

function Button({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="w-full mt-2 bg-blue-600 hover:bg-blue-700 p-2 rounded"
    >
      Analyze
    </button>
  );
}
