# lazada_stock_notifier.py
import requests
import time
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

# Lazada search URLs for specific stores
STORES = {
    "Datablitz": "https://www.lazada.com.ph/shop/datablitz/?q=pokemon%20tcg",
    "GameXtreme": "https://www.lazada.com.ph/shop/gamextreme/?q=pokemon%20tcg",
    "ToysRUs": "https://www.lazada.com.ph/shop/toysrus-philippines/?q=pokemon%20tcg",
    "Maxsoft": "https://www.lazada.com.ph/shop/maxsoft/?q=pokemon%20tcg",
    "ToyKingdom": "https://www.lazada.com.ph/shop/toy-kingdom-official-store/?q=pokemon%20tcg"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}

def check_stock(store_name, url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200 and "Out of stock" not in res.text:
            send_discord_notif(f"🟢 **{store_name}** has Pokémon TCG items in stock!\n{url}")
        else:
            print(f"[{store_name}] Out of stock or page unchanged.")
    except Exception as e:
        print(f"[Error] {store_name}: {e}")

def send_discord_notif(message):
    data = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK, json=data)
    except Exception as e:
        print(f"[Discord Error] {e}")

if __name__ == "__main__":
    print("🔍 Starting Lazada stock monitor...")
    while True:
        for store, link in STORES.items():
            check_stock(store, link)
        time.sleep(1800)  # Check every 30 minutes
