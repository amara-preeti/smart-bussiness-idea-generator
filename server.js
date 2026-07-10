// Simple proxy server — no npm install needed, uses only Node built-ins
// Run: node server.js
// Then open: http://localhost:3000

const http = require("http");
const https = require("https");
const fs = require("fs");
const path = require("path");

const PORT = 3000;
const API_KEY = "gRG0zZ5T0CkfbWvkw0I2q9xSpmTTTS9JPpGRogSczggF";
const WATSONX_URL = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29";
const IAM_URL = "https://iam.cloud.ibm.com/identity/token";

// ── IAM token cache ──────────────────────────────────────────────────────────
let cachedToken = null;
let tokenExpiry = 0;

function getIAMToken() {
  return new Promise((resolve, reject) => {
    if (cachedToken && Date.now() < tokenExpiry) return resolve(cachedToken);

    const body = `grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey=${encodeURIComponent(API_KEY)}`;
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": Buffer.byteLength(body),
        Accept: "application/json",
      },
    };

    const req = https.request(IAM_URL, options, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        if (res.statusCode !== 200) return reject(new Error(`IAM ${res.statusCode}: ${data}`));
        const json = JSON.parse(data);
        cachedToken = json.access_token;
        tokenExpiry = Date.now() + (json.expires_in - 300) * 1000;
        resolve(cachedToken);
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

// ── Static file helper ───────────────────────────────────────────────────────
const MIME = { ".html": "text/html", ".css": "text/css", ".js": "application/javascript" };

function serveStatic(res, filePath) {
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); res.end("Not found"); return; }
    res.writeHead(200, { "Content-Type": MIME[path.extname(filePath)] || "text/plain" });
    res.end(data);
  });
}

// ── Server ───────────────────────────────────────────────────────────────────
http.createServer(async (req, res) => {
  // Proxy endpoint
  if (req.method === "POST" && req.url === "/api/generate") {
    let body = "";
    req.on("data", (c) => (body += c));
    req.on("end", async () => {
      try {
        const token = await getIAMToken();
        const payload = Buffer.from(body);
        const options = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            "Content-Length": payload.length,
          },
        };
        const apiReq = https.request(WATSONX_URL, options, (apiRes) => {
          let data = "";
          apiRes.on("data", (c) => (data += c));
          apiRes.on("end", () => {
            res.writeHead(apiRes.statusCode, { "Content-Type": "application/json" });
            res.end(data);
          });
        });
        apiReq.on("error", (e) => { res.writeHead(502); res.end(JSON.stringify({ error: e.message })); });
        apiReq.write(payload);
        apiReq.end();
      } catch (e) {
        res.writeHead(500);
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  // Static files
  const urlPath = req.url === "/" ? "/index.html" : req.url;
  serveStatic(res, path.join(__dirname, urlPath));

}).listen(PORT, () => {
  console.log(`✅ Server running → http://localhost:${PORT}`);
});
