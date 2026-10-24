# NAIA ExpressPass: Terminal 3 Queue App

Queue management app for **CCC181 Week 3: User-Centered Interface Development**.
It handles passenger bag-drop reservations and staff queue operations at NAIA Terminal 3.

## Project structure

```
naia-expresspass/
├── app.py              # creates the app and defines routes
├── requirements.txt    # packages to rebuild the environment
├── .gitignore          # keeps .venv, caches and secrets out of Git
├── .venv/              # your virtual environment (not committed)
├── templates/          # Jinja2 HTML files for render_template()
│   ├── base.html       # shared layout with navbar, alerts and footer
│   ├── index.html      # home page with quick CTA
│   ├── join.html       # form to join queue with flight details
│   ├── ticket.html     # "My place" page for /queue/<ticket_id>
│   └── staff.html      # staff dashboard for /staff
└── static/             # served at /static/...
    ├── css/style.css
    └── js/main.js
```

## Routes

| URL | View function | What you see |
|---|---|---|
| `/` | `index()` | Welcome page with system overview and "Join the queue" button |
| `/join` | `join_form()` / `join()` | Form to join the queue with server-side validation |
| `/queue/<int:ticket_id>` | `ticket()` | Ticket status, position in line, and option to leave |
| `/queue/<int:ticket_id>/status.json` | `ticket_status()` | JSON endpoint returning status and position for live updates |
| `/staff` | `staff_dashboard()` | Dashboard listing tickets with service filter and call/serve actions |

## 1. Set up the Python environment

```bash
# create (once per project)
python -m venv .venv

# activate (every new terminal)
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# install the packages
pip install -r requirements.txt
```

Your prompt shows `(.venv)` when the environment is active. Some systems use `python3` or `py` instead of `python`.
If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt.

If you add more packages later, record them with:

```bash
pip freeze > requirements.txt
```

## 2. Run the app

```bash
flask --app app run --debug
```

Open http://127.0.0.1:5000. With `--debug`, the server reloads every time you save a file. Never use debug mode in production.

## 3. Put it on GitHub

### Once per computer

```bash
git config --global user.name "Your Name"
git config --global user.email you@g.msuiit.edu.ph   # same email as your GitHub account
git config --list
```

### Create the local repository and first commit

```bash
git init
git branch -M main
git status              # .venv should NOT appear, thanks to .gitignore
git add .
git commit -m "Add Flask starter app"
```

### Connect to GitHub and push

1. On GitHub, create a new **empty** repository (no README, no .gitignore).
2. Copy its URL, then:

```bash
git remote add origin <repo-url>
git push -u origin main
```

GitHub does not accept your account password for Git over HTTPS. Sign in through Git Credential Manager or the GitHub CLI, or use a personal access token or SSH key.

### Everyday loop

```bash
git pull origin main     # before you start working
git status
git add <file>
git commit -m "Add join-queue form"
git push origin main     # when you have commits to share
```

## 4. Lab: ship it through a pull request

1. On GitHub, open an issue: **"Week 3: first interface (join, my place, staff dashboard)"**.
2. Pull the latest `main`, then create a branch:
   ```bash
   git switch main
   git pull origin main
   git switch -c feature/week3-interface
   ```
3. Create `.venv`, install Flask, write `requirements.txt` and `.gitignore`.
4. Build `app.py` with routes for join form, ticket position, and staff dashboard, rendered with Bootstrap templates.
5. Commit in small steps, then push the branch:
   ```bash
   git push -u origin feature/week3-interface
   ```
6. On GitHub, click **Compare & pull request** and write `Closes #N` in the description (N is your issue number). Merge it, then:
   ```bash
   git switch main
   git pull origin main
   ```

## Commit message tips

- Short summary in the imperative: "Add...", "Fix..."
- One logical change per commit
- Commit early and often
- Good: "Add join-queue form". Unhelpful: "update", "asdf", "final na talaga".