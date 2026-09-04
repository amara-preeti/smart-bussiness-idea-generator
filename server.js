// Simple local static server — no npm install or API connection needed
// Run: node server.js
// Then open: http://localhost:3000

const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = 3000;

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
http.createServer((req, res) => {
  // Static files
  const urlPath = req.url === "/" ? "/index.html" : req.url;
  serveStatic(res, path.join(__dirname, urlPath));

}).listen(PORT, () => {
  console.log(`✅ Server running → http://localhost:${PORT}`);
});
