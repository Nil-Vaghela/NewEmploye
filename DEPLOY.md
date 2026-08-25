# Deploying to DigitalOcean (gsucfa.com)

This app stores everything in local Excel files, so it needs a normal always-on
server with a persistent disk - a DigitalOcean Droplet is a good fit (this would
NOT work on a serverless platform like Vercel, since those don't keep local files
between requests).

## 0. What you'll end up with

Browser -> Nginx (port 80/443, handles gsucfa.com + HTTPS) -> Gunicorn (running
this Flask app) -> your Excel files on disk. Gunicorn and Nginx both restart
automatically if the droplet reboots.

## 1. Create the Droplet

1. digitalocean.com -> Create -> Droplets.
2. Image: **Ubuntu 24.04 LTS**.
3. Plan: the cheapest "Basic" shared-CPU droplet ($4-6/mo) is plenty for this app.
4. Authentication: choose SSH key (recommended) or a password. # 2y0UUTck9tfjHnx
5. Create it, then copy its public IPv4 address - you'll need it for DNS.

## 2. Point the domain at it

In whatever registrar gsucfa.com is registered with (GoDaddy, Namecheap, etc.),
open DNS management for the domain and add:

| Type | Host | Value                  |
|------|------|------------------------|
| A    | @    | <droplet IPv4 address> |
| A    | www  | <droplet IPv4 address> |

DNS changes can take anywhere from a few minutes to a few hours to propagate.
You can move on to the next steps while you wait.

## 3. SSH in and install the base packages

Your droplet is set up with **password auth** (not an SSH key), so:

```
ssh root@<droplet IPv4 address>
```

- Enter the root password DigitalOcean showed you when the droplet was created.
- DigitalOcean forces a password change the moment you log in for the first
  time - you'll be prompted to enter the old one once more, then a new one
  twice. Actually go through with this (don't skip it) - treat the original
  password as burned the moment you've seen/shared it anywhere.
- Every future `ssh root@<ip>` will prompt for whatever password you just set.

Once you're in:

```
apt update && apt upgrade -y
apt install -y python3-venv python3-pip nginx git certbot python3-certbot-nginx

# Create a dedicated, non-root user to run the app under - adduser will ask
# you to set a password for this account too, separate from the root one.
adduser gsucfa
usermod -aG sudo gsucfa
su - gsucfa
```

(Optional, worth doing once everything below is working: password-based SSH
is more exposed to brute-force login attempts than a key would be. `sudo apt
install fail2ban` will auto-block IPs after repeated failed login attempts,
and is a quick way to close most of that gap without switching to keys.)

(Run everything from here on as the `gsucfa` user, not root.)

## 4. Get the code onto the server

Easiest without git: from your own machine, upload the project folder with `scp`
(run this on YOUR machine, not the server):

```
scp -r "/Users/nilvaghela/Downloads/GSU-Employe-Attendance-old-state" gsucfa@<droplet IP>:/home/gsucfa/
```

(If you'd rather use git, push this folder to a private GitHub repo first, then
`git clone` it on the server instead.)

Skip the local venv/ folder if scp is slow - it doesn't need to come along
(you'll build a fresh one on the server anyway):

```
scp -r --exclude=venv "/Users/nilvaghela/Downloads/GSU-Employe-Attendance-old-state" gsucfa@<droplet IP>:/home/gsucfa/
```

(macOS's built-in scp doesn't support --exclude - if that errors, just let the
old venv/ come along, it's harmless, or delete it locally first.)

## 5. Set up the app on the server

```
cd /home/gsucfa/GSU-Employe-Attendance-old-state
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

Edit `.env` (it came over with the folder) and set real production values:

```
nano .env
```

- Generate a **new** `FLASK_SECRET_KEY` (don't reuse the dev one):
  `python3 -c "import secrets; print(secrets.token_hex(32))"`
- Set `EMAIL_ADDRESS` / `EMAIL_PASSWORD` to a rotated Gmail app password
  (Google Account -> Security -> App passwords) - the current one has been
  sitting in source code, so treat it as compromised and generate a new one.
- Leave `FLASK_DEBUG=0`.

## 6. Run it under systemd (keeps it running, restarts on crash/reboot)

```
sudo cp deploy/gsucfa.service /etc/systemd/system/gsucfa.service
sudo systemctl daemon-reload
sudo systemctl enable --now gsucfa
sudo systemctl status gsucfa   # should say "active (running)"
```

If it's not starting, check logs with `sudo journalctl -u gsucfa -e`.

## 7. Put Nginx in front of it

```
sudo cp deploy/nginx_gsucfa.conf /etc/nginx/sites-available/gsucfa
sudo ln -s /etc/nginx/sites-available/gsucfa /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

At this point, http://gsucfa.com should load the login page (once DNS has
propagated).

## 8. Turn on HTTPS

```
sudo certbot --nginx -d gsucfa.com -d www.gsucfa.com
```

Follow the prompts (enter an email, agree to terms). Certbot edits the Nginx
config for you and sets up auto-renewal. Afterwards https://www.gsucfa.com
should work with a padlock.

## 9. Firewall (optional but recommended)

```
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## Updating the app later

```
ssh gsucfa@<droplet IP>
cd GSU-Employe-Attendance-old-state
# upload new/changed files here (scp, or git pull if using git)
sudo systemctl restart gsucfa
```

## Notes / things worth knowing

- The Excel files (attendance sheets, Employee Names.xlsx, points.xlsx, etc.)
  live on this one droplet's disk. Back them up periodically (e.g. a nightly
  `scp` or `rsync` to your own machine, or DigitalOcean's droplet backups
  feature) - there's no redundancy otherwise.
- Two different admin passwords still exist in this app (`/login` uses
  `32156`, `/admin` uses `qwerty`) - worth deciding on and unifying before
  this is public-facing, since both are trivially guessable. Happy to fix
  this whenever you want.
- `get-pip.py` (a 2.5MB file sitting in the project root) doesn't need to be
  on the server at all - fine to leave out of the upload.
