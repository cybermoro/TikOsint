import os
import re
import sys
import time
import json
import random
import platform
import requests
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from pystyle import Colors, Colorate, Write

# ---------------------------
# CONFIG
# ---------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile Safari/604.1"
]

# ---------------------------
# Helper Functions
# ---------------------------
def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def slow_type(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def find_linked_accounts(text):
    links = {
        "instagram": re.findall(r"(?:instagram\.com/|@)([A-Za-z0-9_.]+)", text, re.I),
        "youtube": re.findall(r"(?:youtube\.com/(?:c/|channel/|user/)|youtu\.be/)([A-Za-z0-9_-]+)", text, re.I),
        "twitter": re.findall(r"(?:twitter\.com/|@)([A-Za-z0-9_]+)", text, re.I),
        "discord": re.findall(r"(?:discord\.gg/|discordapp\.com/invite/)([A-Za-z0-9_-]+)", text, re.I),
        "emails": re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text, re.I)
    }
    return {k: list(set(v)) for k, v in links.items() if v}

# ---------------------------
# TikTok Scraper
# ---------------------------
class TikTokScraper:
    def __init__(self, username):
        self.username = username.strip().lstrip('@')
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": random.choice(USER_AGENTS)
        })
        self.data = None

    def fetch(self):
        url = f"https://www.tiktok.com/@{self.username}"
        try:
            r = self.session.get(url, timeout=10)
            if r.status_code != 200 or '<div id="captcha_verify_container">' in r.text:
                return False
            soup = BeautifulSoup(r.text, "html.parser")
            script_tag = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
            if not script_tag:
                return False
            json_data = json.loads(script_tag.text.strip())
            self.data = json_data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
            return True
        except Exception:
            return False

    def get_profile_info(self):
        u = self.data.get("user", {})
        s = self.data.get("stats", {})
        linked = find_linked_accounts(u.get("bio", ""))

        profile = {
            "Username": u.get("uniqueId", "N/A"),
            "Display Name": u.get("nickname", "N/A"),
            "Verified": u.get("verified", False),
            "Private Account": u.get("privateAccount", False),
            "Bio": u.get("bio", "N/A"),
            "Followers": s.get("followerCount", 0),
            "Following": s.get("followingCount", 0),
            "Likes": s.get("heartCount", 0),
            "Videos": s.get("videoCount", 0),
            "Region": u.get("region", "Unknown"),
            "Account Created": datetime.fromtimestamp(u.get("createTime", 0), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") if u.get("createTime") else "Unknown",
            "secUid": u.get("secUid", ""),
            "Privacy Flags": {
                "secret": u.get("secret", False),
                "openFavorite": u.get("openFavorite", False),
                "showFavoriteList": u.get("showFavoriteList", False)
            },
            "Linked Accounts": linked
        }

        return profile

    def print_profile_info(self, profile):
        Write.Print("\n[+] Hydration Metadata Extracted:\n\n", Colors.cyan_to_blue)
        for key, val in profile.items():
            if isinstance(val, dict):
                Write.Print(f"{key}:\n", Colors.yellow_to_red)
                for subk, subv in val.items():
                    Write.Print(f"  {subk}: {subv}\n", Colors.green_to_cyan)
            else:
                Write.Print(f"{key}: {val}\n", Colors.green_to_yellow)

# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":
    clear_screen()
    banner = """
 /$$$$$$$$ /$$$$$$ /$$   /$$  /$$$$$$   /$$$$$$  /$$$$$$ /$$   /$$ /$$$$$$$$
|__  $$__/|_  $$_/| $$  /$$/ /$$__  $$ /$$__  $$|_  $$_/| $$$ | $$|__  $$__/
   | $$     | $$  | $$ /$$/ | $$  \ $$| $$  \__/  | $$  | $$$$| $$   | $$   
   | $$     | $$  | $$$$$/  | $$  | $$|  $$$$$$   | $$  | $$ $$ $$   | $$   
   | $$     | $$  | $$  $$  | $$  | $$ \____  $$  | $$  | $$  $$$$   | $$   
   | $$     | $$  | $$\  $$ | $$  | $$ /$$  \ $$  | $$  | $$\  $$$   | $$   
   | $$    /$$$$$$| $$ \  $$|  $$$$$$/|  $$$$$$/ /$$$$$$| $$ \  $$   | $$   
   |__/   |______/|__/  \__/ \______/  \______/ |______/|__/  \__/   |__/   
    """
    print(Colorate.Vertical(Colors.rainbow, banner))
    slow_type("TikTok OSINT Beast Mode — For Educational Use Only!\n", 0.005)

    username = Write.Input("[?] Enter TikTok username: ", Colors.cyan_to_blue, interval=0.005)

    scraper = TikTokScraper(username)
    if scraper.fetch():
        profile = scraper.get_profile_info()
        scraper.print_profile_info(profile)
    else:
        Write.Print("\n[✘] Failed to retrieve profile or hydration data.\n", Colors.red_to_yellow)
