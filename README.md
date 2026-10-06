# File Integrity Checker

A full-stack security tool that detects unauthorized changes to files by comparing SHA-256 hashes against a known-good baseline — the same core technique used by tools like Tripwire and AIDE for host-based intrusion detection.

## How It Works

1. **Set Baseline** — the backend hashes every file in a watched directory using SHA-256 and stores the results (filename → hash) in `baseline.json`. This snapshot represents the "known good" state of the files.
2. **Run Check** — the backend re-hashes the same directory and compares the fresh hashes against the stored baseline, flagging any files that are:
   - **Modified** — still present, but the hash no longer matches
   - **Missing** — present in the baseline but gone from the directory
   - **New** — present in the directory but not in the original baseline
3. The frontend displays results as a security checkpoint: unchanged files show **ACCESS GRANTED**, flagged files show **ACCESS DENIED**.

SHA-256 was chosen because even a single-byte change to a file produces a completely different hash (the avalanche effect), making it reliable for detecting tampering no matter how small.

## Tech Stack

Python, Flask, JavaScript, REST API

## Project Structure

\```
FileIntegrityChecker/
├── Index.html
├── Style.css
├── Script.js
├── README.md
├── .gitignore
└── Backend/
    ├── app.py
    ├── watched_files/    # directory being monitored
    └── baseline.json     # generated snapshot of known-good hashes
\```

## Running It

\```bash
cd Backend
python app.py
\```

Then open `Index.html` directly in your browser (not through a dev-reload tool — see note below).

You can also run the core logic standalone from the command line, without starting the server:

\```bash
python app.py build    # create/refresh the baseline
python app.py check    # compare current files against the baseline
\```

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/build` | Hashes all files in the watched directory and writes a fresh `baseline.json` |
| GET | `/api/check` | Re-hashes the watched directory and returns `modified`, `missing`, and `new` files compared to the baseline |

## Notes

- Open `Index.html` directly in the browser rather than through VS Code's Live Server — Live Server watches the whole project folder, and since `/api/build` writes `baseline.json` to disk, it was triggering an auto-reload that wiped the results the instant they appeared.
- `flask-cors` is required so the frontend (served from `file://`) can call the Flask API running on `127.0.0.1:5000`.
