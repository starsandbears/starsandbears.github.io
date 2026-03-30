# Stars&Bears

Non-profit building AI-augmented human brain interfaces to help people with neural diseases and other health issues, with the long-term vision to unlock human potential.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Run

```bash
.venv/bin/python server.py
# Open http://localhost:8080
```

## API

### Subscribe

```
POST /api/subscribe
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "interest": "bci"
}
```

Interest options: `neural-disease`, `bci`, `mental-health`, `rehabilitation`, `cognitive`, `open-data`, `other`

### List subscribers (admin)

```
GET /api/subscribers
```

> Note: Protect this endpoint with authentication before deploying to production.

## Project Structure

```
server.py            — Flask backend (subscription API + static file serving)
requirements.txt     — Python dependencies
static/
  index.html         — Landing page
  style.css          — Styles (dark theme, responsive)
  app.js             — Form handling, scroll animations
data/
  subscribers.json   — Subscriber data (auto-created, gitignored)
```
