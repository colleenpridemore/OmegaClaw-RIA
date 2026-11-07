"""
Node: OmegaClaw-RIA (Relational Intelligence Autonomy) - Telegram RCN Webhook Runner
Repository: https://github.com/colleenpridemore/OmegaClaw-RIA
Core Function: Bridges Aethel's ASI:Cloud inference with RIAClaw's
non-extractive safety middleware, zero-ownership witness logging, and Telegram webhooks.
"""

import asyncio
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from openai import OpenAI
from telegram.ext import ApplicationBuilder

# -------------------------------------------------------------------------
# 1. Safety Layer & ASI:Cloud Client Initialization
# -------------------------------------------------------------------------
try:
    from unbranded_safety import unbranded_witness
except ImportError:
    def unbranded_witness(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

ASI1_API_KEY = os.environ.get("ASI1_API_KEY")
if not ASI1_API_KEY:
    raise RuntimeError("ASI1_API_KEY is not set. Please export it before starting the bot.")

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Please export it before starting the bot.")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", "10000"))

client = OpenAI(
    base_url="https://api.asi1.ai/v1",
    api_key=ASI1_API_KEY,
)


def normalize_reply_text(value):
    """Normalize model output to a Telegram-safe string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return " ".join(str(item) for item in value if item)
    return str(value).strip()


@unbranded_witness
def run_rcn_inference(user_id: str, prompt: str):
    """
    Routes incoming Telegram queries through the ASI1 model family
    with biocentric weighting and zero-ownership witness logging.
    """
    response = client.chat.completions.create(
        model="asi1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are @aethel, operating through the RIAClaw Relational Conditioning Node (RCN). "
                    "Maintain non-extractive safety, relational agency, zero pathologizing, "
                    "and zero-ownership witness logging."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content
    return normalize_reply_text(content) or "I couldn't generate a response right now."


# -------------------------------------------------------------------------
# 2. Initialize Telegram Application for Webhook Handling
# -------------------------------------------------------------------------
telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()


async def initialize_telegram_app():
    """Prepare the PTB app and register the webhook if configured."""
    await telegram_app.initialize()
    if WEBHOOK_URL:
        await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
        print(f"✅ Telegram webhook registered: {WEBHOOK_URL}")
    else:
        print("⚠️ WEBHOOK_URL not set. Bot is not registered with Telegram yet.")


# -------------------------------------------------------------------------
# 3. Unified HTTP Request Handler (Health Checks + Telegram Webhook)
# -------------------------------------------------------------------------
class TelegramWebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"📥 [WEBHOOK HIT] GET request path: {self.path}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"RIAClaw Telegram RCN Node is active and listening via Webhook.")

    def do_POST(self):
        print(f"📥 [WEBHOOK HIT] POST request path: {self.path}")
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            post_data = self.rfile.read(content_length) if content_length > 0 else b""
            print(f"📦 [BODY] Read {len(post_data)} bytes from Telegram.")

            # Acknowledge Telegram immediately with 200 OK so it never times out.
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

            if not post_data:
                return

            try:
                payload = json.loads(post_data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                print("💥 [INVALID JSON] Could not decode Telegram payload.")
                return

            if not isinstance(payload, dict):
                print("💥 [INVALID PAYLOAD] Telegram payload was not a JSON object.")
                return

            threading.Thread(target=_process_telegram_update, args=(payload,), daemon=True).start()

        except Exception as exc:
            print(f"💥 [ERROR in do_POST]: {exc}")
            import traceback
            traceback.print_exc()

    def log_message(self, format, *args):
        return


def _process_telegram_update(payload):
    """Handle the Telegram update in a background thread without blocking the HTTP server."""
    try:
        message = payload.get("message") or payload.get("edited_message")
        if not message:
            return

        chat_id = message.get("chat", {}).get("id")
        user = message.get("from") or {}
        user_id = str(user.get("id", "unknown"))
        incoming_text = message.get("text")

        if not incoming_text or not isinstance(incoming_text, str):
            return

        print(f"💬 [TEXT] User {user_id}: {incoming_text}")

        try:
            reply_text = run_rcn_inference(user_id=user_id, prompt=incoming_text)
        except Exception as exc:
            print(f"💥 [INFERENCE ERROR]: {exc}")
            reply_text = "I hit an error while generating a response. Please try again."

        print(f"🤖 [REPLY]: {str(reply_text)[:80]}...")

        if not telegram_app or not chat_id:
            return

        async def send_reply():
            await telegram_app.bot.send_message(chat_id=chat_id, text=reply_text)

        try:
            asyncio.run(send_reply())
            print("✨ [SUCCESS] Reply sent to Telegram!")
        except Exception as send_err:
            print(f"💥 [SEND ERROR]: {send_err}")
            import traceback
            traceback.print_exc()

    except Exception as bg_err:
        print(f"💥 [BACKGROUND ERROR]: {bg_err}")
        import traceback
        traceback.print_exc()


def run_server():
    server = HTTPServer(("0.0.0.0", PORT), TelegramWebhookHandler)
    print(f"🌐 Unified Webhook & Health server listening on port {PORT}...")
    server.serve_forever()


# -------------------------------------------------------------------------
# 4. Main Execution Loop & Initialization
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 RIAClaw RCN Telegram Node initializing...")

    try:
        asyncio.run(initialize_telegram_app())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize_telegram_app())
        loop.close()

    run_server()
