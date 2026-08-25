Version 1.0.0
    - Login
    - Clock in / Clock out / lunch start / lunch End
    - Edit time
    - View previous Excel sheet
    - Send mail of current excel sheet
    - Add user
    - Delete User
    
Version 1.0.1
    - Add points
    - Apply for leave

Version 1.0.2
    - Bug fixed for points system

Version 1.0.3
    - Detial employe time system
    - Point systme upgraded
    - Graphical Improvment of Employe Data Page

Version 1.0.4
    - Bug fixed for points system
    - Employe Can access now

Version 2.0.0
    - Files sorted
    - Design Updated
    - FeedBack option added
    - Public Feedback added

Version 3.0.0
    - Ratting System 
    - Improvement
Version 3.0.1
    - Fixed: requirements.txt was missing pytz and an unpinned Werkzeug pulled
      in a version incompatible with Flask 2.2.3, so the app could not even
      start on a fresh install. Pinned Werkzeug/Jinja2/click/itsdangerous and
      added pytz.
    - Fixed: /leaderboard and /rate_students crashed (500) whenever they were
      opened without first visiting a user's points page (no session yet).
    - Fixed: /edit_points/<id> crashed (500) for an unknown/mistyped User ID
      instead of showing a normal "not found" message.
    - Fixed: duplicate route on '/Feedback' meant the public feedback form
      silently required login to even view, breaking the "Public Feedback"
      feature from v2.0.0. Merged into a single public GET/POST route.
    - Fixed: a duplicate, unreachable route on '/' was removed (dead code
      shadowed by the login redirect).
    - Fixed: /assign could crash with a ZeroDivisionError if there were no
      Student Leaders yet, and modified pandas slices with a copy warning.
    - Fixed: a typo in Location.ShowLocation() ("MovementLog'.xlsx") meant
      stock movement log files were never filtered out of the location list.
    - Fixed: deprecated DataFrame.append() calls (removed in pandas 2.x)
      replaced with pd.concat() so the app won't break on a pandas upgrade.
    - Added .gitignore (venv/, __pycache__/, .env, .DS_Store).
    - Known issue (not fixed yet, needs a decision): /ims, /Dashboard,
      /AddStocks and /ListToBringDown route to templates that don't exist
      in templates/ (location.html, dashboard.html, Add_Stocks.html,
      ListToBringDown.html) - this inventory/stock module has never worked.
    - Known issue (not fixed yet, security): the Gmail app password used to
      send email is hardcoded in app.py in three places, and /login (admin
      password "32156") and /admin (admin password "qwerty") use two
      different, inconsistent admin passwords.

How to run locally:
    1. python3 -m venv venv          (or reuse the existing venv/ folder)
    2. source venv/bin/activate      (Windows: venv\Scripts\activate)
    3. pip install -r requirements.txt
    4. python app.py
    5. Open http://localhost:8000/attendance in your browser
       - Admin login (via /login): user id "admin", password "32156"
       - Simple admin file browser (/admin): user id "admin", password "qwerty"
       - Employee: enter their numeric User ID from "Employee Names.xlsx"

Version 3.0.2
    - Removed the inventory/stock module (/ims, /Dashboard, /AddStocks,
      /ListToBringDown and their supporting Location/, Addstocks/, Database/,
      Dashboard/, ListToBringDown/ folders) per request - it never worked
      (missing templates) and isn't part of the attendance system. Moved the
      folders to _to_delete/ instead of removing them outright, in case
      anything in there is still wanted.

Version 3.0.3
    - Reverted the login / admin-login / attendance page styling back to the
      original background-image look after trying a couple of glass-theme
      redesigns that didn't land. No functional changes, UI only.

Version 3.0.4
    - Prepped for deploying to a DigitalOcean droplet behind www.gsucfa.com:
      moved the Flask secret key and the Gmail sender/password out of source
      code into a .env file (python-dotenv), turned off Flask debug mode by
      default (was a real security risk to leave on for a public site),
      added gunicorn as the production WSGI server, and added deploy/
      (systemd service + Nginx config) plus DEPLOY.md with the full
      step-by-step runbook. See DEPLOY.md for how to actually go live.
