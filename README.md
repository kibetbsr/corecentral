# Kipsolu Central FC — Official Website

A full-stack football club website for **Kipsolu Central FC** (Kipsolu, Kenya · Est. 2021),
built with **Django + SQLite** on the backend and **plain HTML5, CSS3, Bootstrap 5, and vanilla
JavaScript** on the frontend — no TypeScript, no React/Vue/Next.js, no npm build tooling.

Club statements: *"Central to the core."* · *"Greatness achieved through excellence."*

---

## 1. Tech Stack

| Layer      | Technology                                              |
|------------|----------------------------------------------------------|
| Backend    | Python 3 + Django (class-based views, forms, admin)      |
| Database   | SQLite (Django default, `db.sqlite3`)                    |
| Frontend   | Django Template Language + HTML5 + CSS3 + Bootstrap 5 (CDN) + vanilla JS |
| Images     | Pillow (for `ImageField` uploads)                         |

No TypeScript, no JS frameworks, no npm/build step of any kind — Bootstrap is loaded via CDN
and all custom interactivity lives in plain `.js` files under `static/js/`.

---

## 2. Project Structure

```
kipsolu/
├── kipsolu_central/       # Django project settings, root urls.py, wsgi/asgi
├── core/                  # Home, The Club (About), Contact, ContactMessage model
│   └── management/commands/seed_data.py   # sample data generator
├── team/                  # Player & Staff models — Squad page
├── matches/               # Match model — Fixtures & Results page
├── news/                  # NewsPost model — News list + detail pages
├── gallery/               # GalleryImage model — Gallery page + lightbox
├── templates/             # base.html + one folder per app
├── static/
│   ├── css/style.css      # green/gold brand styles
│   ├── js/                # nav.js, gallery-lightbox.js, form-validation.js
│   └── img/kc-crest.svg   # placeholder club crest
├── media/                 # uploaded images (players, news, gallery, staff) — created at runtime
├── requirements.txt
└── manage.py
```

---

## 3. Setup Instructions

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Move into the project folder
cd kipsolu

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create an admin account (you'll be prompted for username/email/password)
python manage.py createsuperuser

# 6. (Optional but recommended) Load sample content so the site isn't empty
python manage.py seed_data

# 7. Run the development server
python manage.py runserver
```

Then visit:
- **Public site:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

> The project ships with `db.sqlite3` already migrated and seeded with sample players, staff,
> fixtures/results, news posts, and gallery images, plus a superuser (`admin` / `admin123`) so
> you can log in immediately. **Change this password** before deploying anywhere public.
> If you'd rather start clean, delete `db.sqlite3` and the `media/` folder, then repeat steps 4–6.

---

## 4. Managing Content via the Admin Panel

Everything on the public site — players, fixtures, results, news, gallery images, and staff —
is fully editable through **Django admin** at `/admin/`. No code or template changes are ever
required.

### Adding a Player
1. Go to **Admin → Team → Players → Add Player**.
2. Fill in name, squad number, position (Goalkeeper/Defender/Midfielder/Forward), nationality,
   date of birth, height, and upload a photo.
3. Fill in stats (appearances, goals, assists, clean sheets) — these show on the player's
   profile page.
4. Save. The player instantly appears on the **Squad** page under the correct position filter.

### Creating a Fixture, Then Adding the Result Later
1. Go to **Admin → Matches → Matches → Add Match**.
2. Fill in opponent, competition, date, kickoff time, venue (Home/Away), and stadium.
3. Leave **Status** as `Upcoming` and save — it will appear in the *Upcoming* tab on the
   Fixtures page.
4. After the match is played, open the same record again, set **Status** to `Completed`, and
   fill in **Our Score** / **Opponent Score** (and optionally a short match report).
5. Save. The fixture automatically moves from *Upcoming* to *Results* on the public Fixtures
   page — no template or code edits needed. Use `Postponed` if a match is called off.

### Publishing a News Post
1. Go to **Admin → News → News Posts → Add News Post**.
2. Enter a title (the URL slug auto-fills from it), choose a category, write a short excerpt
   and the full content, and optionally upload a featured image.
3. Set the publish date and make sure **Is Published** is checked.
4. Save. It appears immediately in the News listing (paginated 6 per page) and gets its own
   detail page.

### Adding Gallery Images
1. Go to **Admin → Gallery → Gallery Images → Add Gallery Image**.
2. Upload an image, give it a title/category (Matchday, Training, Fans & Community, Club
   Events), and an optional caption.
3. Save. It appears in the responsive gallery grid; clicking it opens the vanilla-JS lightbox
   with next/previous navigation and captions.

### Adding Staff
1. Go to **Admin → Team → Staff → Add Staff**.
2. Enter name, role (Head Coach, Assistant Coach, Goalkeeping Coach, Physiotherapist, Team
   Manager, Other), photo, and bio.
3. Save. They appear in the "Coaching & Staff" section on the Squad page.

### Reviewing Contact Form Submissions
Every message submitted through the public **Contact** page is saved to
**Admin → Core → Contact Messages**, where you can mark it as read/unread or search by name,
email, or subject.

### Club History / Achievements Timeline
Manage the "Achievements Timeline" shown on **The Club** page via
**Admin → Core → Achievement Milestones** (year, title, description).

---

## 5. Image Uploads

`MEDIA_URL` / `MEDIA_ROOT` are configured in `settings.py`, and the project `urls.py` serves
uploaded media in development (`DEBUG=True`). Uploaded images (player photos, staff photos,
news featured images, gallery images) are stored under `media/` and referenced automatically
via each model's `ImageField`.

For a production deployment, serve `media/` and `static/` (after running
`python manage.py collectstatic`) through your web server or a storage service — Django's
built-in dev server should not be used in production.

---

## 6. Responsive Design Notes

- Every template uses Bootstrap's grid (`container`, `row`, `col-*`, `col-sm-*`, `col-md-*`,
  `col-lg-*`) — no fixed-width layouts.
- The navbar collapses into a hamburger menu (`navbar-toggler`) below the `lg` breakpoint.
- All images use `img-fluid` or CSS `object-fit`/`aspect-ratio` so they scale cleanly.
- Custom CSS in `static/css/style.css` uses relative units and a mobile-first media query for
  the hero section.
- The Squad, Fixtures, News, and Gallery grids reflow into single/double columns on mobile and
  tablet instead of overflowing or shrinking unreadably.

---

## 7. Re-seeding or Resetting Sample Data

```bash
# Wipe and regenerate all sample players/staff/matches/news/gallery/achievements
python manage.py seed_data --flush
```

This is safe to run at any time in development — it will not touch real content you've added
if the corresponding table already has rows (each seed step checks first), unless `--flush`
is passed.
