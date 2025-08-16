# 🎯 TikOsint — TikTok OSINT Toolkit

**TikOsint** is an educational OSINT (Open Source Intelligence) tool that scrapes publicly available TikTok user metadata by username.

It leverages the hydration payload embedded in TikTok profile pages to extract detailed account information — no login or API keys required.

> 🧠 Useful for recon, bug bounty reporting, or passive intelligence gathering.

---

## 📋 Features

- 📝 Username  
- 👤 Display Name  
- 🖋️ Bio  
- 🖼️ Avatar URL  
- ✅❌ Verified Status  
- 🔒🔓 Private Account Flag  
- 👥 Followers  
- 🔄 Following  
- ❤️ Likes  
- 🎥 Video Count  
- 🌍 Region (with flag + full country name)  
- 🌐 Language  
- 🔑 `secUid`  
- 🔓 `openId`  
- 🔗 `unionId`  
- 🔗 Profile Deep Link  
- 🤝 Friend Count  

---

## 🐧 Installation (Linux)

```bash
git clone https://github.com/cybermoro/TikOsint.git
cd TikOsint
sudo apt update && sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt
python3 TikOsint.py
