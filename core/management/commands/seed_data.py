import io
import random
from datetime import date, time, timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from PIL import Image, ImageDraw, ImageFont

from core.models import AchievementMilestone, ContactMessage
from team.models import Player, Staff
from matches.models import Match
from news.models import NewsPost
from gallery.models import GalleryImage

GREEN = (11, 46, 40)
GOLD = (201, 162, 75)
CREAM = (245, 239, 224)


def make_placeholder_image(label, size=(600, 800), bg=GREEN, fg=GOLD):
    """Generate a simple branded placeholder image in memory (no external assets needed)."""
    img = Image.new('RGB', size, color=bg)
    draw = ImageDraw.Draw(img)

    # Border
    draw.rectangle([8, 8, size[0] - 8, size[1] - 8], outline=fg, width=6)

    # Centered label text
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    text = label
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    else:
        tw, th = len(text) * 6, 11
    draw.text(((size[0] - tw) / 2, (size[1] - th) / 2), text, fill=fg, font=font)

    draw.text((size[0] / 2 - 60, size[1] - 60), "KIPSOLU CENTRAL FC", fill=CREAM, font=font)

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"{slugify(label)}.jpg")


class Command(BaseCommand):
    help = "Seed the Kipsolu Central FC database with sample players, staff, matches, news, and gallery images."

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Delete existing seeded data before re-seeding.'
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write('Flushing existing data...')
            Player.objects.all().delete()
            Staff.objects.all().delete()
            Match.objects.all().delete()
            NewsPost.objects.all().delete()
            GalleryImage.objects.all().delete()
            AchievementMilestone.objects.all().delete()

        self.seed_players()
        self.seed_staff()
        self.seed_matches()
        self.seed_news()
        self.seed_gallery()
        self.seed_achievements()

        self.stdout.write(self.style.SUCCESS('Kipsolu Central FC seed data created successfully.'))

    def seed_players(self):
        if Player.objects.exists():
            self.stdout.write('Players already exist, skipping.')
            return

        players_data = [
            (1, 'Brian', 'Kiptoo', 'GK', 190, date(1998, 3, 12)),
            (22, 'Felix', 'Rono', 'GK', 188, date(2001, 7, 4)),
            (2, 'Dennis', 'Mutai', 'DF', 180, date(1999, 1, 20)),
            (3, 'Collins', 'Barno', 'DF', 178, date(2000, 5, 9)),
            (4, 'Amos', 'Kiprotich', 'DF', 182, date(1997, 11, 30)),
            (5, 'Erick', 'Langat', 'DF', 176, date(2002, 2, 14)),
            (6, 'Joseph', 'Ndiema', 'MF', 174, date(1999, 9, 21)),
            (8, 'Kevin', 'Cheruiyot', 'MF', 172, date(2000, 4, 3)),
            (10, 'Victor', 'Kiptum', 'MF', 175, date(1998, 12, 17)),
            (14, 'Samuel', 'Korir', 'MF', 170, date(2001, 6, 25)),
            (9, 'Emmanuel', 'Sang', 'FW', 179, date(1999, 8, 8)),
            (11, 'Patrick', 'Bett', 'FW', 177, date(2000, 10, 2)),
            (17, 'Ian', 'Kosgei', 'FW', 181, date(2002, 1, 15)),
        ]

        for number, first, last, position, height, dob in players_data:
            player = Player.objects.create(
                first_name=first,
                last_name=last,
                squad_number=number,
                position=position,
                nationality='Kenya',
                date_of_birth=dob,
                height_cm=height,
                bio=(
                    f"{first} {last} joined Kipsolu Central FC as part of the club's commitment to "
                    f"developing local talent. Known for embodying our motto: Central to the core, "
                    f"greatness achieved through excellence."
                ),
                appearances=random.randint(5, 40),
                goals=random.randint(0, 15) if position in ('MF', 'FW') else random.randint(0, 2),
                assists=random.randint(0, 10),
                clean_sheets=random.randint(0, 12) if position in ('GK', 'DF') else 0,
                is_active=True,
                joined_date=date(2021, random.randint(1, 12), random.randint(1, 28)),
            )
            player.photo.save(
                f"{slugify(first)}-{slugify(last)}.jpg",
                make_placeholder_image(f"#{number} {first[0]}. {last}"),
                save=True,
            )
        self.stdout.write(f'Created {len(players_data)} players.')

    def seed_staff(self):
        if Staff.objects.exists():
            self.stdout.write('Staff already exist, skipping.')
            return

        staff_data = [
            ('Michael Onyango', 'HC'),
            ('Peter Waweru', 'AC'),
            ('Grace Chebet', 'GK'),
            ('Nancy Achieng', 'PHYS'),
            ('Daniel Kimutai', 'MGR'),
        ]
        for full_name, role in staff_data:
            member = Staff.objects.create(
                full_name=full_name,
                role=role,
                bio=f"{full_name} supports Kipsolu Central FC's coaching and management structure.",
            )
            member.photo.save(
                f"{slugify(full_name)}.jpg",
                make_placeholder_image(full_name),
                save=True,
            )
        self.stdout.write(f'Created {len(staff_data)} staff members.')

    def seed_matches(self):
        if Match.objects.exists():
            self.stdout.write('Matches already exist, skipping.')
            return

        opponents_upcoming = ['Chelaba United', 'Sotik Rangers', 'Bomet Stars', 'Litein Athletic']
        opponents_past = ['Mulot FC', 'Kericho Leopards', 'Konoin United', 'Buret Warriors', 'Belgut FC']

        today = timezone.localdate()

        for i, opp in enumerate(opponents_upcoming):
            Match.objects.create(
                opponent=opp,
                competition='County League',
                match_date=today + timedelta(days=7 * (i + 1)),
                kickoff_time=time(15, 0),
                venue='HOME' if i % 2 == 0 else 'AWAY',
                stadium='Kipsolu Green Ground' if i % 2 == 0 else f'{opp} Stadium',
                status='UPCOMING',
            )

        for i, opp in enumerate(opponents_past):
            our_score = random.randint(0, 4)
            their_score = random.randint(0, 4)
            Match.objects.create(
                opponent=opp,
                competition='County League',
                match_date=today - timedelta(days=7 * (i + 1)),
                kickoff_time=time(15, 0),
                venue='HOME' if i % 2 == 0 else 'AWAY',
                stadium='Kipsolu Green Ground' if i % 2 == 0 else f'{opp} Stadium',
                status='COMPLETED',
                our_score=our_score,
                opponent_score=their_score,
                match_report=(
                    f"Kipsolu Central FC faced {opp} in a competitive County League fixture, "
                    f"finishing {our_score}-{their_score}. The team showed the discipline and "
                    f"excellence that defines our badge."
                ),
            )

        Match.objects.create(
            opponent='Kaplong FC',
            competition='County League',
            match_date=today + timedelta(days=21),
            kickoff_time=time(15, 0),
            venue='AWAY',
            stadium='Kaplong Grounds',
            status='POSTPONED',
        )

        self.stdout.write('Created sample fixtures and results.')

    def seed_news(self):
        if NewsPost.objects.exists():
            self.stdout.write('News posts already exist, skipping.')
            return

        posts_data = [
            (
                'Kipsolu Central FC Kicks Off 2026 Season',
                'CLUB',
                'The club opens its 2026 campaign with renewed ambition and a refreshed squad.',
                (
                    "Kipsolu Central FC has officially opened its 2026 season with a renewed sense of "
                    "purpose. Since our founding in 2021, the club has grown from a community project "
                    "into a competitive force in county football.\n\n"
                    "Head Coach Michael Onyango addressed the squad ahead of pre-season training, "
                    "reminding players that the club's identity remains unchanged: central to the core, "
                    "and committed to greatness achieved through excellence.\n\n"
                    "Fans can expect a busy fixture calendar this season, with home matches at Kipsolu "
                    "Green Ground drawing bigger crowds each year."
                ),
            ),
            (
                'Match Report: Hard-Fought Draw Against Kericho Leopards',
                'MATCH',
                'A gritty performance saw Kipsolu Central FC share the points in a tense encounter.',
                (
                    "Kipsolu Central FC produced a determined display against Kericho Leopards, "
                    "battling to a share of the spoils in front of a spirited home crowd.\n\n"
                    "Chances were shared throughout, with our forwards testing the visiting goalkeeper "
                    "on several occasions. Defensively, the back line held firm, reflecting the values "
                    "of discipline the club is built on.\n\n"
                    "The result keeps Kipsolu Central FC firmly in contention in the County League table."
                ),
            ),
            (
                'Club Launches Youth Community Outreach Program',
                'COMMUNITY',
                'Kipsolu Central FC extends its mission beyond the pitch with a new youth initiative.',
                (
                    "True to our belief that the club is more than a football team, Kipsolu Central FC "
                    "has launched a youth community outreach program aimed at giving young people in "
                    "Kipsolu access to structured football coaching and mentorship.\n\n"
                    "The program reflects our founding statement: we are a place to belong, a platform "
                    "for possibility, and a badge that means something.\n\n"
                    "Sessions will run every weekend at Kipsolu Green Ground, open to boys and girls "
                    "aged 8 to 16."
                ),
            ),
            (
                'New Signing Strengthens Midfield Options',
                'TRANSFER',
                'Kipsolu Central FC bolsters its midfield ahead of a demanding fixture schedule.',
                (
                    "Kipsolu Central FC has added further depth to its midfield ranks this transfer "
                    "window, bringing in a versatile player known for both defensive discipline and "
                    "creative distribution.\n\n"
                    "Club management expressed confidence that the new arrival embodies the values the "
                    "club looks for both on and off the pitch."
                ),
            ),
        ]

        for i, (title, category, excerpt, content) in enumerate(posts_data):
            post = NewsPost.objects.create(
                title=title,
                slug=slugify(title),
                category=category,
                excerpt=excerpt,
                content=content,
                publish_date=timezone.now() - timedelta(days=i * 3),
                is_published=True,
            )
            post.featured_image.save(
                f"{slugify(title)}.jpg",
                make_placeholder_image(title[:20], size=(800, 450)),
                save=True,
            )
        self.stdout.write(f'Created {len(posts_data)} news posts.')

    def seed_gallery(self):
        if GalleryImage.objects.exists():
            self.stdout.write('Gallery images already exist, skipping.')
            return

        gallery_data = [
            ('Matchday Atmosphere', 'MATCHDAY'),
            ('Pre-Season Training', 'TRAINING'),
            ('Fans at Kipsolu Green Ground', 'FANS'),
            ('Trophy Presentation', 'CLUB'),
            ('Squad Training Session', 'TRAINING'),
            ('Community Youth Day', 'FANS'),
            ('Matchday Warm-Up', 'MATCHDAY'),
            ('Club Jersey Launch', 'CLUB'),
        ]

        for title, category in gallery_data:
            image = GalleryImage.objects.create(
                title=title,
                category=category,
                caption=f"{title} — Kipsolu Central FC",
            )
            image.image.save(
                f"{slugify(title)}.jpg",
                make_placeholder_image(title, size=(800, 600)),
                save=True,
            )
        self.stdout.write(f'Created {len(gallery_data)} gallery images.')

    def seed_achievements(self):
        if AchievementMilestone.objects.exists():
            self.stdout.write('Achievements already exist, skipping.')
            return

        milestones = [
            (2021, 'Club Founded', 'Kipsolu Central FC was established in Kipsolu, Kenya, with a mission to unite the community through football.'),
            (2022, 'First County League Season', 'The club competed in its first full County League season, finishing a respectable mid-table.'),
            (2023, 'New Training Facility', 'Kipsolu Green Ground received upgraded training facilities to support player development.'),
            (2024, 'County Cup Semi-Finalists', 'Kipsolu Central FC reached the semi-finals of the County Cup for the first time in club history.'),
            (2025, 'Youth Academy Launched', 'The club opened its youth academy, extending opportunities to the next generation of local talent.'),
        ]
        for year, title, description in milestones:
            AchievementMilestone.objects.create(year=year, title=title, description=description)
        self.stdout.write(f'Created {len(milestones)} achievement milestones.')
