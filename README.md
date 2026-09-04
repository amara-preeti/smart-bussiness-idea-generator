# IdeaForge Local

IdeaForge Local is an offline-first business idea generator. It uses deterministic templates and local scoring rules, so user input never leaves the browser and no API key or external AI service is required.

## Run

Requirements: Node.js 16 or newer. Python 3.11 or newer is optional for the analysis utilities.

```powershell
npm install
npm run build
npm start
```

Open <http://localhost:3000>. The project has no runtime JavaScript dependencies, so `npm install` only confirms the package manifest; it does not contact an AI service.

For a direct local analysis check:

```powershell
python -m pytest
```

Useful commands:

```powershell
npm run check
npm test
npm run coverage
```

The build command validates the JavaScript entry points and copies the browser assets into `dist/`. The development server serves the source files directly.

## Features

- Generates tailored ideas from skills, budget, industry, audience, and context.
- Stores saved ideas in browser `localStorage`.
- Supports idea count adjustment, history management, and copy-to-clipboard.
- Uses no external API, network request, telemetry, credential, or cloud service.

## Architecture

The browser owns the generation workflow in `app.js`. `server.js` is only a static file server for local development. Python utilities under `python_app/` provide reusable offline scoring and validation logic.

## Security and licensing

No secrets or API keys are required. This repository intentionally does not include an open-source license file.