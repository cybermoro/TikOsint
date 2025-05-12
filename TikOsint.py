import os
import platform
import requests
from bs4 import BeautifulSoup
import json
from pystyle import Colors, Write, Colorate
import time
import pycountry

# Function to clear the screen
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Clear the screen at the start
clear_screen()

banner = """
  _______  _  _      ____        _         _   
 |__   __|(_)| |    / __ \      (_)       | |  
    | |    _ | | __| |  | | ___  _  _ __  | |_ 
    | |   | || |/ /| |  | |/ __|| || '_ \ | __|
    | |   | ||   < | |__| |\__ \| || | | || |_ 
    |_|   |_||_|\_\ \____/ |___/|_||_| |_| \__|
                                               
    By : Moro                                           
    Github : https://github.com/zqgc
    Insta : https://instagram.com/zq.gc
    Discord : @r_jm
"""

def country_code_to_flag(code):
    if not code:
        return "🌐 Unknown"
    return ''.join(chr(ord(c.upper()) + 127397) for c in code)

def get_country_name(code):
    country = pycountry.countries.get(alpha_2=code.upper())
    return country.name if country else "Unknown"

def convert_country(code):
    return f"{country_code_to_flag(code)} {get_country_name(code)}"

print(Colorate.Vertical(Colors.rainbow, banner))
Write.Print('This Tool is for educational purposes Only!!!\n', Colors.blue_to_purple, interval=0.1)

Target = Write.Input("Enter TikTok Username: ", Colors.blue_to_purple, interval=0.01)

class TikTokUserScraper:
    def __init__(self, username: str):
        self.username = username
        self.data = None
        self.fetch()

    def fetch(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            )
        }
        url = f"https://www.tiktok.com/@{self.username}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
        if script_tag:
            try:
                json_data = json.loads(script_tag.text.strip())
                self.data = json_data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
            except Exception:
                Write.Print("❌ Failed to parse user data.\n", Colors.red, interval=0.01)
                exit()
        else:
            Write.Print("❌ USER NOT FOUND or TikTok layout changed.\n", Colors.red, interval=0.01)
            exit()

    def show_info(self):
        u = self.data.get("user", {})
        s = self.data.get("stats", {})

        user_info = {
            "Username": u.get("uniqueId", "N/A"),
            "Display Name": u.get("nickname", "N/A"),
            "Bio": u.get("bio", "N/A"),
            "Avatar URL": u.get("avatarLarger", "N/A"),
            "Verified": "YES" if u.get("verified") else "NO",
            "Private Account": "YES" if u.get("privateAccount") else "NO",
            "Followers": s.get("followerCount", "N/A"),
            "Following": s.get("followingCount", "N/A"),
            "Friend Count": s.get("friendCount", "N/A"),
            "Likes": s.get("heartCount", "N/A"),
            "Video Count": s.get("videoCount", "N/A"),
            "Region": convert_country(u.get("region", "")),
            "Language": u.get("language", "N/A"),
            "SecUID": u.get("secUid", "N/A"),
            "OpenID": u.get("openId", "N/A"),
            "UnionID": u.get("unionId", "N/A"),
            "Profile Deep Link": u.get("profileDeepLink", "N/A")
        }

        time.sleep(1)
        Write.Print("\n========== TikTok User Info ==========\n", Colors.rainbow, interval=0.01)
        for key, value in user_info.items():
            Write.Print(f"{key}: ", Colors.rainbow, interval=0.005)
            Write.Print(f"{value}\n", Colors.green_to_yellow, interval=0.005)
        Write.Print("\n=======================================\n", Colors.rainbow, interval=0.01)

if __name__ == "__main__":
    scraper = TikTokUserScraper(Target)
    scraper.show_info()
