import os
import platform
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pycountry
from colorama import Fore, Style, init

init(autoreset=True)

# ========== Util Functions ==========

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def flag_from_code(code):
    try:
        return ''.join(chr(ord(c.upper()) + 127397) for c in code)
    except:
        return "🏳️"

def convert_country(code):
    if not code or code.strip() == "":
        return "🌐 Unknown"
    code = code.upper().strip()

    # Special cases and TikTok internal codes
    special_cases = {
        "ZZ": "🌐 Unknown",
        "AN": "🇳🇱 Netherlands Antilles",
        "XK": "🇽🇰 Kosovo",
        "XE": "🌐 Experimental Region",
    }

    if code in special_cases:
        return special_cases[code]

    try:
        country = pycountry.countries.get(alpha_2=code)
        return f"{flag_from_code(code)} {country.name}" if country else f"🌐 Unknown ({code})"
    except:
        return f"🌐 Unknown ({code})"

def guess_country_by_language(language_code):
    language_map = {
        "en": "US",
        "ru": "RU",
        "es": "ES",
        "fr": "FR",
        "ar": "SA",
        "de": "DE",
        "pt": "BR",
        "ja": "JP",
        "ko": "KR",
        "tr": "TR",
        "id": "ID",
        "vi": "VN",
        "zh": "CN"
    }
    return convert_country(language_map.get(language_code, "ZZ"))

def format_unix_timestamp(ts):
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return "Invalid timestamp"

# ========== Scraper Class ==========

class TikTokScraper:
    def __init__(self, username):
        self.username = username.strip().lstrip('@')
        self.url = f"https://www.tiktok.com/@{self.username}"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            )
        }
        self.data = None

    def fetch_data(self):
        try:
            resp = requests.get(self.url, headers=self.headers)
            soup = BeautifulSoup(resp.text, "html.parser")
            script = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
            json_data = json.loads(script.text)
            self.data = json_data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
            return True
        except Exception as e:
            print(Fore.RED + f"[✘] Failed to fetch or parse data: {e}")
            return False

    def extract_info(self):
        u = self.data.get("user", {})
        s = self.data.get("stats", {})

        region_code = u.get("region", "")
        if not region_code:
            region_code = guess_country_by_language(u.get("language", ""))

        info = {
            "Username": u.get("uniqueId"),
            "Display Name": u.get("nickname"),
            "Verified": u.get("verified", False),
            "Private Account": u.get("privateAccount", False),
            "Bio": u.get("bio"),
            "Followers": s.get("followerCount"),
            "Following": s.get("followingCount"),
            "Likes": s.get("heartCount"),
            "Videos": s.get("videoCount"),
            "Region": convert_country(region_code),
            "Language": u.get("language"),
            "Account Created": format_unix_timestamp(u.get("createTime", 0)),
            "secUid": u.get("secUid"),
            "openId": u.get("openId"),
            "unionId": u.get("unionId"),
            "Profile Link": u.get("profileDeepLink"),
            "Privacy Flags": {
                "secret": u.get("secret", False),
                "openFavorite": u.get("openFavorite", False),
                "showFavoriteList": u.get("showFavoriteList", False)
            }
        }

        return info

    def display_info(self, info):
        print(Fore.CYAN + "\n[+] TikTok OSINT Metadata Extracted:\n")
        for key, val in info.items():
            if isinstance(val, dict):
                print(f"{Fore.YELLOW}{key}:")
                for subk, subv in val.items():
                    print(f"  {Fore.GREEN}{subk}: {Fore.WHITE}{subv}")
            else:
                color = Fore.RED if key in ["secUid", "Region", "Account Created"] else Fore.GREEN
                print(f"{color}{key}: {Fore.WHITE}{val}")

    def save_as_json(self, info, filename="output.json"):
        try:
            with open(filename, "w") as f:
                json.dump(info, f, indent=4)
            print(Fore.MAGENTA + f"\n[✓] Data saved to {filename}")
        except Exception as e:
            print(Fore.RED + f"[✘] Failed to save JSON: {e}")

# ========== Main Entry ==========

def main():
    clear_screen()
    print(Fore.MAGENTA + """




 ______   __     __  __     ______     ______     __     __   __     ______  
/\__  _\ /\ \   /\ \/ /    /\  __ \   /\  ___\   /\ \   /\ "-.\ \   /\__  _\ 
\/_/\ \/ \ \ \  \ \  _"-.  \ \ \/\ \  \ \___  \  \ \ \  \ \ \-.  \  \/_/\ \/ 
   \ \_\  \ \_\  \ \_\ \_\  \ \_____\  \/\_____\  \ \_\  \ \_\\"\_\    \ \_\ 
    \/_/   \/_/   \/_/\/_/   \/_____/   \/_____/   \/_/   \/_/ \/_/     \/_/ 
                                                                             

 
                                                          


        [ TikTok Metadata Recon Tool v2.0 ]
    """)

    username = input(Fore.CYAN + "[?] Enter TikTok username: ").strip()
    scraper = TikTokScraper(username)

    if scraper.fetch_data():
        info = scraper.extract_info()
        scraper.display_info(info)
        save = input(Fore.YELLOW + "\n[?] Save output as JSON? (y/n): ").lower()
        if save == 'y':
            scraper.save_as_json(info)
    else:
        print(Fore.RED + "[✘] Failed to retrieve data.")

if __name__ == "__main__":
    main()
