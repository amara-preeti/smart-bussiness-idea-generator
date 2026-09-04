const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const root = __dirname;
const output = path.join(root, "dist");
const assets = ["index.html", "style.css", "app.js"];

execFileSync(process.execPath, ["--check", "app.js"], { cwd: root, stdio: "inherit" });
execFileSync(process.execPath, ["--check", "server.js"], { cwd: root, stdio: "inherit" });
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(output, { recursive: true });
for (const asset of assets) fs.copyFileSync(path.join(root, asset), path.join(output, asset));
console.log(`Built ${assets.length} browser assets in ${path.relative(root, output)}/`);