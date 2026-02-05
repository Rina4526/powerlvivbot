from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import imagehash
import os

URL = "https://poweron.loe.lviv.ua/"
TARGET_WIDTH = 1000

def trim(img):
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    return img.crop(bbox) if bbox else img

def resize(img):
    w, h = img.size
    ratio = TARGET_WIDTH / w
    return img.resize((TARGET_WIDTH, int(h * ratio)), Image.LANCZOS)

def make_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(URL, timeout=60000)

        page.wait_for_selector("canvas", timeout=30000)
        canvas = page.locator("canvas")
        canvas.screenshot(path="raw.png")

        browser.close()

    img = Image.open("raw.png")
    img = trim(img)
    img = resize(img)
    img.save("current.png")
    os.remove("raw.png")

def is_updated():
    make_screenshot()
    new_hash = imagehash.phash(Image.open("current.png"))

    if not os.path.exists("hash.txt"):
        with open("hash.txt", "w") as f:
            f.write(str(new_hash))
        return False

    with open("hash.txt") as f:
        old_hash = imagehash.hex_to_hash(f.read().strip())

    if new_hash != old_hash:
        with open("hash.txt", "w") as f:
            f.write(str(new_hash))
        return True

    return False
