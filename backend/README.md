# Learning Tracker Backend

This folder archives the Flask + SQLite backend currently deployed at:

- Public API: `https://47.250.40.117.sslip.io`
- Server path: `/root/learning-tracker-api/app.py`
- Database path: `/root/learning-tracker-api/tracker.db`

The backend was hotfixed on 2026-06-10 to restore the sharing APIs expected by
the v6 frontend:

- `GET/POST /api/learning_tracker_profiles`
- `GET/POST/PATCH/DELETE /api/learning_tracker_pairs`
- `GET /api/learning_tracker_data`

It also restricts `/api/data` writes to the authenticated owner while allowing
accepted partners to read shared data.
