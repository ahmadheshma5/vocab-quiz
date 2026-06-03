# vocab-quiz

Run the full server-backed vocabulary quiz system locally:

1. Create a Python virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

2. Start the server:

```bash
python app.py
```

This serves the app at http://localhost:8000

Pages:
- http://localhost:8000/quiz.html — main quiz (contains leaderboard at top)
- http://localhost:8000/login.html — alternate simple login page (name-only)
- http://localhost:8000/leaderboard.html — standalone leaderboard viewer (reads localStorage)

Notes:
- The app is designed to work as a static GitHub Pages site: features such as name-only login, adding words, and the leaderboard are stored in the browser's `localStorage` so they work without a server.
- If you run the provided Flask server (`app.py`) the server will persist `words.json`, `users.json`, and `leaderboard.json` on the filesystem. Running a server is optional.
# vocab-quiz