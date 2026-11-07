"""
Node: OmegaClaw-RIA (Relational Intelligence Autonomy) - Telegram RCN Webhook Runner
Repository: https://github.com/colleenpridemore/OmegaClaw-RIA
Core Function: Bridges Aethel's ASI:Cloud inference with RIAClaw's 
non-extractive safety middleware, zero-ownership witness logging, and Telegram webhooks.
"""

import os
import json
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from openai import OpenAI
from telegram import Update
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

client = OpenAI(
    base_url="https://api.asi1.ai/v1",
    api_key=os.environ.get("ASI1_API_KEY"),
)

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
    return response.choices[0].message.content

# -------------------------------------------------------------------------
# 2. Initialize Telegram Application for Webhook Handling
# -------------------------------------------------------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
telegram_app = None

if TELEGRAM_TOKEN:
    telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
else:
    print("⚠️ TELEGRAM_BOT_TOKEN not found in environment variables.")

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
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            print(f"📦 [BODY] Read {len(post_data)} bytes from Telegram.")

            # Acknowledge Telegram immediately with 200 OK
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

            if not post_data:
                return

            # Parse payload
            data = json.loads(post_data.decode('utf-8'))
            message = data.get("message") or data.get("edited_message")
            
            if message:
                chat_id = message.get("chat", {}).get("id")
                user_id = str(message.get("from", {}).get("id", "unknown"))
                incoming_text = message.get("text")
                
                if incoming_text:
                    print(f"💬 [TEXT] User {user_id}: {incoming_text}")
                    reply_text = run_rcn_inference(user_id=user_id, prompt=incoming_text)
                    print(f"🤖 [REPLY]: {reply_text[:80]}...")
                    
                    if telegram_app and chat_id:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(telegram_app.bot.send_message(
                            chat_id=chat_id, 
                            text=reply_text
                        ))
                        loop.close()
                        print("✨ [SUCCESS] Reply sent to Telegram!")
        except Exception as e:
            print(f"💥 [ERROR in do_POST]: {e}")
            import traceback
            traceback.print_exc()

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), TelegramWebhookHandler)
    print(f"🌐 Unified Webhook & Health server listening on port {port}...")
    server.serve_forever()

# -------------------------------------------------------------------------
# 4. Main Execution Loop & Initialization (Thread-Safe Event Loop)
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 RIAClaw RCN Telegram Node initializing...")
    
    if telegram_app:
        async def init_bot():
            await telegram_app.initialize()
        
        try:
            asyncio.run(init_bot())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(init_bot())
    
    # Start the HTTP server capturing Render traffic
    run_server()
