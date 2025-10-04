import requests
import time
import os
import threading
from flask import Flask

app = Flask(__name__)

DISCORD_WEBHOOK = os.getenv("https://discord.com/api/webhooks/1423996895247995002/RS5TaUvQ9jYk84MRzLbtNlX21hPx08i56U7j5O1PLfo6qxqbKZT31yopdZ0TWQs-qExw")

STORES = {
    "Datablitz": "https://www.lazada.com.ph/shop/datablitz/?q=pokemon%20tcg",
    "GameXtreme": "https://www.lazada.com.ph/shop/gamextreme/?q=pokemon%20tcg",
    "ToysRUs": "https://www.lazada.com.ph/shop/toysrus-philippines/?q=pokemon%20tcg",
    "Maxsoft": "https://www.lazada.com.ph/shop/maxsoft/?q=pokemon%20tcg",
    "ToyKingdom": "https://www.lazada.com.ph/shop/toy-kingdom-official-store/?q=pokemon%20tcg"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
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
    if not DISCORD_WEBHOOK:
        print("⚠️ Missing Discord webhook!")
        return

    USER_ID = "457158232356421640"  # 👈 replace this with your real ID (e.g. "1234567890123456789")
    full_message = f"<@{USER_ID}> 🔔 {message}"

    try:
        res = requests.post(DISCORD_WEBHOOK, json={"content": full_message})
        print(f"Discord response: {res.status_code}")
    except Exception as e:
        print(f"[Discord Error] {e}")


def background_task():
    print("🔍 Starting Lazada stock monitor...")
    while True:
        for store, link in STORES.items():
            check_stock(store, link)
        time.sleep(1800)  # 30 minutes

# Start the background monitoring in a separate thread
threading.Thread(target=background_task, daemon=True).start()

@app.route('/')
def home():
    return "✅ Lazada Stock Notifier is running!"
@app.route('/test')
def test():
    import requests
    res = requests.get("https://www.lazada.com.ph", timeout=10)
    return f"Lazada status: {res.status_code}"
@app.route("/test_discord")
def test_discord():
    import requests

    WEBHOOK_URL = "https://discord.com/api/webhooks/1423996895247995002/RS5TaUvQ9jYk84MRzLbtNlX21hPx08i56U7j5O1PLfo6qxqbKZT31yopdZ0TWQs-qExw"
    message = {"content": "✅ Test message from Lazada stock notifier!"}

    res = requests.post(WEBHOOK_URL, json=message)
    return f"Discord response: {res.status_code}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)




