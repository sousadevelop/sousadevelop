from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from pathlib import Path

USERNAME = "joaovictorss"
PROFILE_URL = f"https://tryhackme.com/p/{USERNAME}"
BADGE_URL = f"https://tryhackme-badges.s3.amazonaws.com/{USERNAME}.png"

OUTPUT_DIR = Path("assets")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "tryhackme-banner.png"

WIDTH = 900
HEIGHT = 230

bg = Image.new("RGB", (WIDTH, HEIGHT), "#0d1117")
draw = ImageDraw.Draw(bg)

try:
    title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    text_font = ImageFont.truetype("DejaVuSans.ttf", 22)
    small_font = ImageFont.truetype("DejaVuSans.ttf", 18)
except:
    title_font = text_font = small_font = None

draw.rounded_rectangle(
    [20, 20, WIDTH - 20, HEIGHT - 20],
    radius=24,
    fill="#111827",
    outline="#ef4444",
    width=2
)

draw.text((50, 45), "TryHackMe", fill="#ffffff", font=title_font)
draw.text((50, 92), f"@{USERNAME}", fill="#9ca3af", font=text_font)
draw.text((50, 128), "Cybersecurity Labs • Pentest • Web Security", fill="#d1d5db", font=small_font)
draw.text((50, 162), PROFILE_URL, fill="#ef4444", font=small_font)

try:
    response = requests.get(BADGE_URL, timeout=20)
    response.raise_for_status()

    badge = Image.open(BytesIO(response.content)).convert("RGBA")
    badge.thumbnail((360, 160))

    x = WIDTH - badge.width - 60
    y = (HEIGHT - badge.height) // 2

    bg.paste(badge, (x, y), badge)

except Exception:
    draw.text(
        (WIDTH - 380, 95),
        "TryHackMe badge unavailable",
        fill="#ef4444",
        font=text_font
    )

bg.save(OUTPUT_FILE)
print(f"Banner generated: {OUTPUT_FILE}")
