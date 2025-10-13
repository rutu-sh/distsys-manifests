Overview

This workspace includes a static frontend (the T-Rex game) and a small Python Flask 'score' server.

What I added
- `middleware/main.py` - Flask app with POST /save-score and GET /scores, persistence in `middleware/scores.json`.
- `middleware/requirements.txt` - Python deps.
- `server.js` and `package.json` - small Node/Express static server that serves `frontend/public` and exposes `/config` with SCORE server URL from env.
- Frontend changes in `frontend/public/index.html` to show a save-score modal and POST to the score server.

Run locally

1) Start the Python score server (uses env SCORE_SERVER_PORT and SCORE_SERVER_HOST):

```bash
python3 -m pip install -r middleware/requirements.txt
SCORE_SERVER_PORT=8080 python3 middleware/main.py
```

2) Start the dev server (Node) to serve the frontend and provide `/config`:

```bash
npm install
SCORE_SERVER_URL=http://localhost SCORE_SERVER_PORT=8080 npm run start:dev
```

3) Open http://localhost:3000 in your browser.

Notes
- The frontend will try these sources, in order, to discover the score server: `window.__SCORE_SERVER`, `/config` endpoint, `http://localhost:8080`.
- If you want the frontend to post directly to the Python server without the Node dev server, set `window.__SCORE_SERVER = 'http://localhost:8080'` in the browser console before triggering the modal.

Next steps
- Add authentication/rate-limiting on the score endpoint.
- Add input sanitization.
- Add a scoreboard UI that fetches `/scores`.
