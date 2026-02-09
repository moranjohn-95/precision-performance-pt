# Repo Housekeeping Audit

## Current structure summary
- Django project split into `precision_performance/` (project), `accounts/`,
  and `training/` apps.
- Templates live in `templates/` with app-specific subfolders plus
  `base.html`, `dashboard_base.html`, and `index.html`.
- Static assets are organised under `assets/css/`, `assets/js/`, and
  `assets/images/`.
- Documentation assets are grouped under `documentation/` with
  `agile/`, `design/`, `features/`, `screenshots/`, and `testing/`.
- Project root includes `README.md`, `requirements.txt`, `runtime.txt`,
  `Procfile`, and `manage.py`.

## Summary table
| Area | Status | Notes |
| --- | --- | --- |
| App structure | Good | `accounts/` and `training/` contain models, views, forms. |
| Templates | Good | App folders under `templates/` match usage. |
| Static assets | Good | `assets/css`, `assets/js`, `assets/images` in place. |
| Documentation | Needs tidy | File naming has typos and duplicates. |
| Git hygiene | Needs tidy | `venv/`, `__pycache__/`, `tmp_emails/`, `db.sqlite3` exist in repo. |
| Migrations | Needs review | Two `0014_` migrations in `training/migrations`. |
| Stray files | Needs review | `accounts/views.py (append)` appears to be a leftover file. |
| Settings | Good | Env-driven `DEBUG`, `ALLOWED_HOSTS`, and static config present. |

## Findings
### What is great
- Standard Django layout with clear app separation.
- Static assets grouped by type and separate from templates.
- Documentation folders are structured by topic.
- `requirements.txt`, `runtime.txt`, and `Procfile` are present.
- `.gitignore` covers common Python, Django, and environment files.

### What is messy or inconsistent
- `venv/` and `__pycache__/` directories exist inside the repo.
- `db.sqlite3` and `tmp_emails/` are present even though `.gitignore` covers them.
- Documentation filenames contain typos and inconsistent naming, such as
  `feature-trainerdahsbaord-desktop-responsive.png`,
  `feature-cllient-bodymetricscheckin.jpg`,
  `owner-clientassignmnet.jpg`, and
  `wave-ownertrianer-dasbaord-explain.png`.
- `accounts/views.py (append)` appears to be a stray or duplicate file.
- `training/migrations/` contains two `0014_` migration files, which is
  a merge artifact risk.
- One template references `assets/js/...` via `{% static %}`, while most
  templates use `js/...`, which can lead to broken paths if inconsistent.

## Recommendations
- Remove or untrack `venv/`, `__pycache__/`, `db.sqlite3`, and `tmp_emails/`
  from git history if they were committed.
- Standardise documentation filenames to correct typos and keep naming
  consistent (update README links if they reference these files).
- Delete or archive `accounts/views.py (append)` if it is not in use.
- Resolve the duplicate `0014_` migrations by squashing or renaming.
- Align static file references to the same path convention
  (`{% static 'js/...'%}` vs `{% static 'assets/js/...'%}`).

## Action list
1. Verify git status to confirm no tracked `venv/`, `__pycache__/`,
   `db.sqlite3`, or `tmp_emails/` files remain.
2. Create a naming cleanup plan for documentation images and apply
   consistent naming once README links are confirmed.
3. Confirm whether `accounts/views.py (append)` is used anywhere, then
   remove or archive it.
4. Review `training/migrations/` for duplicate migration numbers and
   clean up with a safe migration merge plan.
5. Check template static references and standardise the JS path pattern.
