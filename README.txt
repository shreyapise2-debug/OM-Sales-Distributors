# OM Sales Distributors — PostgreSQL DBMS Case Study

## Files
- `OM_Sales_Distributors_DBMS_Case_Study.docx` — report formatted around the requested case-study points.
- `schema.sql` — PostgreSQL table definitions, keys, constraints and indexes.
- `seed.sql` — 20 rows in each of six tables (120 total).
- `queries.sql` — SQL operations and demonstration transactions.
- `app.py` — Flask backend connected to PostgreSQL.
- `templates/` and `static/style.css` — HTML pages and styling.
- `ER_Diagram.png` — ER diagram image.
- `frontend_screenshot_preview.png` — illustrative dashboard preview, not a live browser capture.
- `.env.example` — environment variable template.

## Setup
1. In pgAdmin or psql, create database `shreya_pise_om_sales`.
2. Connect to that database and execute `schema.sql`, then `seed.sql`.
3. Copy `.env.example` to `.env`; set `PGPASSWORD` to your PostgreSQL password.
4. In this folder run `python -m venv .venv`.
5. Install dependencies: `python -m pip install -r requirements.txt`.
6. Run `python app.py`; open `http://127.0.0.1:5000`.

If PowerShell script activation is blocked, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe app.py` instead. Do not include `.env` or your real password in a submission.
