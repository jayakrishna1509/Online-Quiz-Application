// Vercel serverless proxy function to forward all /api/* requests to a backend service.
// Configure the backend endpoint in Vercel as the env var BACKEND_URL (e.g. https://my-backend.example.com/api)

const BACKEND_URL = (
  process.env.BACKEND_URL ||
  process.env.VITE_API_BASE_URL ||
  "http://localhost:5000/api"
).replace(/\/$/, "");

async function getRequestBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks)));
    req.on("error", reject);
  });
}

module.exports = async (req, res) => {
  try {
    // Build target URL by appending the incoming path after /api
    const incomingPath = req.url || "";
    // If req.url starts with /api, strip it; otherwise append as-is
    const pathAfterApi = incomingPath.replace(/^\/api/, "") || "/";
    const targetUrl = BACKEND_URL + pathAfterApi;

    // Build headers: copy except host
    const headers = { ...req.headers };
    delete headers.host;

    const fetchOptions = {
      method: req.method,
      headers,
    };

    if (req.method !== "GET" && req.method !== "HEAD") {
      const body = await getRequestBody(req);
      if (body && body.length) fetchOptions.body = body;
    }

    const nodeFetch = globalThis.fetch || (await import("node-fetch")).default;
    const backendRes = await nodeFetch(targetUrl, fetchOptions);

    // Copy status and headers
    res.statusCode = backendRes.status;
    backendRes.headers.forEach((value, name) => {
      // Vercel may reject some headers; skip transfer-encoding
      if (name.toLowerCase() === "transfer-encoding") return;
      res.setHeader(name, value);
    });

    const arrayBuffer = await backendRes.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    res.end(buffer);
  } catch (err) {
    console.error("Proxy error:", err);
    res.statusCode = 500;
    res.end(JSON.stringify({ error: "Proxy error", message: String(err) }));
  }
};
