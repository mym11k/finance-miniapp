import requests
import json

TOKEN = "8942665117:AAHVFjc9mQYSnomlODaxxYS1Z2UFvz98PC0"
APP_URL = "https://mym11k.github.io/finance-miniapp/"
API = f"https://api.telegram.org/bot{TOKEN}"

def send(chat_id, text, markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if markup:
        data["reply_markup"] = json.dumps(markup)
    requests.post(f"{API}/sendMessage", json=data)

def handle(update):
    msg = update.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text", "")

    if text == "/start":
        send(chat_id, "💳 <b>Мои финансы</b>\n\nОткрой дашборд — там твои расходы по категориям, советы по экономии и история операций.", {
            "inline_keyboard": [[{
                "text": "📊 Открыть дашборд",
                "web_app": {"url": APP_URL}
            }]]
        })

def main():
    offset = 0
    print("Бот запущен...")
    while True:
        try:
            r = requests.get(f"{API}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=35)
            updates = r.json().get("result", [])
            for u in updates:
                offset = u["update_id"] + 1
                handle(u)
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
