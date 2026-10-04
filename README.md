# 🍛 Mandi 1 — Restaurant Ordering Website (Django)

A takeaway ordering website for **Mandi 1**, built with Django. Customers browse the menu,
add items to a cart, and confirm an order with their contact details (no online payment yet —
pay on pickup only). Staff manage the entire menu, deals, and orders from an easy,
non-technical **Staff Dashboard**, separate from the low-level Django admin.

---

## 1. Features

- 🎨 **"Mandi House" editorial design** — dark coffee hero sections, cream content sections,
  mustard-gold + terracotta accents, Playfair Display serif headings, fully responsive
  (mobile, tablet, desktop)
- ✨ Subtle hover "tilt" micro-interactions on cards and buttons (`static/js/tilt.js`) —
  they lean gently toward the cursor and ease back on mouse-leave
- 🛒 Session-based cart — browse and add items without logging in
- 📞 Checkout only asks for **name, phone number, and an optional note**
- 📋 **My Orders** page — customers can track order status without an account
- 📅 **Reserve a Table** page — shows weekly opening hours/available times and takes a
  booking request (name, phone, party size, date, time); confirmed by staff on the phone,
  same pattern as food orders
- 👨‍🍳 **Staff Dashboard** (`/staff/`) — big buttons, plain language, built for non-technical
  people. Two separate roles/logins (see section 5)
- 🤖 Built-in rule-based AI chat assistant (works fully offline, no API key required)
- 🇦🇺 Australian locale: `en-au`, `Australia/Sydney` timezone, AUD currency
- 🔒 Security-conscious defaults (CSRF, secure cookies in production, env-based secrets)
- 🔐 HTTPS-ready — see section 7
- 🚫 Online payment & delivery buttons are visibly present but **disabled** for now
- 📄 Use-case & analysis diagrams under `docs/` for client discussions
- 🖼️ Dishes/deals show a decorative placeholder "plate" graphic until you upload real
  photos — see section 12

---

## 2. Project Structure

```
mandi1/
├── mandi1/          # Project settings, URLs
├── menu/            # Public menu: categories, dishes, deals
├── orders/          # Cart, checkout, order models
├── bookings/        # Table reservations + opening hours
├── chatbot/         # Rule-based chat assistant API
├── dashboard/       # Staff-friendly management panel
├── templates/        # Shared base template
├── static/           # CSS/JS (theme, hover-tilt effect, chatbot widget)
├── docs/             # Use case + analysis diagrams (Mermaid)
├── requirements.txt
├── .env.example
└── manage.py
```

---

## 3. Local Setup (Windows / macOS / Linux)

**Requirements:** Python 3.11+ installed.

```bash
# 1. Go into the project folder
cd mandi1

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create a staff/admin account
python manage.py createsuperuser

# 6. (Optional) Load sample menu data to see the site fully populated
python manage.py seed_data

# 7. Run the development server
python manage.py runserver
```

Now open:
- **Customer site:** http://127.0.0.1:8000/
- **Staff Dashboard:** http://127.0.0.1:8000/staff/login/
- **Django admin (advanced/technical use only):** http://127.0.0.1:8000/django-admin/

> `seed_data` is a custom management command (`menu/management/commands/seed_data.py`)
> that adds sample categories, dishes, and one deal — delete this data any time from
> the Staff Dashboard once you add your real menu.

---

## 4. How Ordering Works

1. Customer browses the **Menu** or **Deals** page and adds items to the cart (no login needed).
2. On the **Cart** page they review items, then click **Confirm Order**.
3. They enter just **name, phone number, and an optional note** — that's all that's required.
4. The order is saved with status **Pending**, the cart is emptied, and the customer sees a
   confirmation screen.
5. The order is remembered in the customer's browser session, so they can revisit
   **My Orders** any time to see its live status. If they switch devices, they can look an
   order up there by phone number instead.
6. Staff sees the new order in the **Staff Dashboard → Orders**, calls the customer's phone
   number to confirm details, then marks the order **Confirmed** → **Completed**.
7. Payment happens **in person on pickup**. Online payment and delivery buttons are shown
   as disabled — remove `disabled` in `orders/templates/orders/checkout.html` once you're
   ready to build those out.

---

## 5. Staff Dashboard (built for non-technical people) — Two Roles

The dashboard at `/staff/` is **not linked anywhere on the public website** — its URL is only
given directly to the owner and staff. It replaces the low-level Django admin for day-to-day
use, and follows basic **HCI (Human-Computer Interaction)** principles: large buttons, plain
English labels, one task per screen, clear success/error messages, and confirmation prompts
before destructive actions.

There are two account types, each with its **own separate login page** — an owner
account can't be used on the staff page and vice versa:

- **Owner login:** `/staff/owner-login/` — keep this URL private, share it with the owner only.
- **Staff login:** `/staff/login/` — give this URL to staff members.

### 🧑‍💼 Owner (superuser account)
The account created with `createsuperuser` is the **owner** account. The owner can:
- Add / edit / delete dishes — name, description, photo, price, discount %, stock quantity
- Create and manage categories
- Create deals/combos with a bundled price
- **Add or remove staff logins** (Staff Accounts page) — just a name, a login ID, and a
  password; no technical knowledge needed
- View, confirm, and update the status of every order
- See at-a-glance stats: pending orders, total dishes, sold-out items, active deals

### 🧑‍🍳 Staff (created by the owner)
A regular staff account (created from the owner's **Staff Accounts** page) can **only**:
- View incoming orders
- Update an order's status (Confirm it after calling the customer, mark Completed, or Cancel)

Staff accounts cannot see or change dishes, prices, deals, or other staff accounts — those
pages return "permission denied" if a staff account tries to visit their URL directly.

> The technical Django admin (`/django-admin/`) still exists underneath, but the owner
> should not need it — the Staff Dashboard covers everything day-to-day.

---

## 6. Reserve a Table

The **Reserve a Table** page (`/bookings/reserve/`) shows the week's opening hours on
one side and a short booking form on the other — name, phone, party size, date, and
time. Like food orders, a booking is **not final until staff calls to confirm it**; no
online payment or deposit is taken.

- The owner edits opening hours from **Staff Dashboard → Opening Hours** — toggle a day
  open/closed, and set its open time, close time, and last seating time. The booking
  form automatically rejects a date/time outside those hours.
- Staff and the owner both see incoming bookings under **Staff Dashboard → Table
  Bookings**, and can mark each one Confirmed, Completed, or Cancelled after calling
  the customer.
- Customers can revisit **My Bookings** (linked from the booking confirmation page) to
  check status, the same way **My Orders** works for food orders.

## 7. Security Notes

- `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` are read from environment variables
  (see `.env.example`) — **never commit a real secret key to source control**.
- CSRF protection is on for every form and the chatbot API.
- Passwords are hashed by Django's built-in auth system (PBKDF2).
- When `DJANGO_DEBUG=False` (i.e. in production), the app automatically enables:
  HTTPS redirect, secure cookies, and HSTS headers.
- All prices are re-validated against the database at checkout — the cart in the
  browser session is never trusted blindly for the final total.
- Staff Dashboard and Django admin both require a **staff** account (`is_staff=True`).
- Before going live, run: `python manage.py check --deploy` and address any warnings.

---

## 8. Running Over HTTPS

**Locally (for testing):** the project includes `django-extensions` + Werkzeug, which
can serve the site over HTTPS with an auto-generated, self-signed certificate:

```bash
python manage.py runserver_plus 127.0.0.1:8443 --cert-file adhoc
```

Then open `https://127.0.0.1:8443/` (your browser will warn about the self-signed
certificate — that's expected on localhost; click through to proceed).

**In production (once you have a domain):** set `DJANGO_DEBUG=False`. The security
settings in `mandi1/settings.py` then automatically:
- Redirect all HTTP traffic to HTTPS (`SECURE_SSL_REDIRECT`)
- Mark cookies as HTTPS-only (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- Send HSTS headers so browsers always use HTTPS for your domain going forward

You'll still need a real TLS certificate for your domain — most hosts offer this for
free via **Let's Encrypt** (often just one click if using a platform like
PythonAnywhere, Render, or Railway; or `certbot` if self-hosting with Nginx).

## 9. Deploying Later (once you buy a domain/host)

1. Pick a host that supports Python/Django (e.g. a VPS, PythonAnywhere, Railway, Render).
2. Set real environment variables on the host:
   - `DJANGO_SECRET_KEY` — generate a new long random string
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
3. Point your domain's DNS to the host.
4. Swap SQLite for PostgreSQL/MySQL if you expect real traffic (edit `DATABASES` in
   `mandi1/settings.py`).
5. Run `python manage.py collectstatic` so static files (CSS/JS) are served correctly.
6. Use a production server (e.g. Gunicorn + Nginx) instead of `runserver`.
7. Enable HTTPS (e.g. via Let's Encrypt) — the security settings in `settings.py`
   will then automatically enforce it.

---

## 10. Diagrams (for client conversations)

- `docs/use_case_diagram.md` — who does what (Customer vs Admin)
- `docs/analysis_diagram.md` — domain model (classes/relationships) + order lifecycle
  sequence diagram

Both are written in **Mermaid** — GitHub, most Markdown viewers, and the Mermaid Live
Editor (https://mermaid.live) will render them visually.

---

## 11. Default Login (change this immediately)

A default **owner** account ships with the project:
- **Login page:** `/staff/owner-login/`
- **Username:** `Mand1owner`
- **Password:** `@Mandi1___`

**Change this password as soon as you go live** (Owner Login → log in → use
`/django-admin/` → Users → Mand1owner → set a new password, or run
`python manage.py changepassword Mand1owner`).

Neither login page is linked anywhere on the public website — bookmark them, or give
each URL directly to the right person. From the owner dashboard, the owner adds staff
logins from the **Staff Accounts** page (no `createsuperuser` or Django admin needed
for that).

---

## 12. Adding Your Own Photos Later

Every dish, deal, and card on the site currently shows a decorative placeholder
"plate" graphic (a CSS circle) instead of a real photo, so the site looks finished
even before you have photography ready. Swapping in a real photo takes one step:

1. Go to **Staff Dashboard → Dishes** (or **Deals**), edit the item, and upload a photo
   in the **Photo** field. That's it — the template automatically uses the uploaded
   photo instead of the placeholder graphic the moment one exists.

If you're customising the templates yourself, every placeholder in the code is marked
with a comment like:
```html
<!-- Placeholder plate graphic — replace with dish.image once real photos are ready -->
```
so you can find every spot at a glance (`menu/templates/menu/*.html`).

## 13. Extending the Chatbot

The chatbot (`chatbot/views.py`) is currently rule-based (keyword matching) so it
works fully offline with zero configuration. To connect it to a real AI model later,
replace the body of `_generate_reply()` with a call to your AI provider's API,
keeping the same `{"reply": "..."}` JSON response shape — the frontend widget
(`static/js/chatbot.js`) doesn't need to change.
