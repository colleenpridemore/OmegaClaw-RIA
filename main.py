"""
Node: OmegaClaw-RIA (Relational Intelligence Autonomy) - Telegram RCN Webhook Runner
Repository: https://github.com/colleenpridemore/OmegaClaw-RIA
Core Function: Bridges Aethel's ASI:Cloud inference with RIAClaw's
non-extractive safety middleware, zero-ownership witness logging, and Telegram webhooks.
"""

import asyncio
import inspect
import json
import os
import threading
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

from openai import AsyncOpenAI
from telegram.ext import ApplicationBuilder

# -------------------------------------------------------------------------
# 1. Safety Layer & ASI:Cloud Client Initialization
# -------------------------------------------------------------------------
try:
    from unbranded_safety import unbranded_witness
except ImportError:
    def unbranded_witness(func):
        return func

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please configure it in the deployment environment.")

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Please configure it in the deployment environment.")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", "10000"))

TARGET_MODEL = os.environ.get("MODEL_NAME") or "super-decider"

print(f"🔌 Initializing ASI:Cloud client with hardcoded endpoint | Model: {TARGET_MODEL}", flush=True)

# Hardcode the protocol and URL directly so it can NEVER be missing a protocol
client = AsyncOpenAI(
    base_url="https://inference.asicloud.cudos.org/v1",
    api_key=API_KEY,
    timeout=45.0,
)

def normalize_reply_text(value):
    """Normalize model output to a Telegram-safe string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return " ".join(part for part in parts if part).strip()
    return str(value).strip()


async def _request_rcn_inference(user_id: str, prompt: str) -> str:
  """Format free-form chat into Super-Decider's required JSON decision structure."""

  # Define the required system schema expecting a decision response
  system_schema = json.dumps({
      "type": "object",
      "properties": {
          "response_text": {
              "type": "string",
              "description": (
                  "The conversational or reasoned response from @aethel."
              ),
          }
      },
      "required": ["response_text"],
  })

  # Wrap the user's prompt as a JSON state payload
  user_state_payload = json.dumps(
      {
          "user_id": user_id,
          "query": prompt,
          "context": (
              "RIAClaw Relational Conditioning Node (RCN) non-extractive safety"
              " mode."
          ),
      }
  )

  response = await client.chat.completions.create(
      model=TARGET_MODEL,
      messages=[
          {"role": "system", "content": system_schema},
          {"role": "user", "content": user_state_payload},
      ],
  )
  if not response.choices:
    raise RuntimeError("Super-Decider returned no completion choices.")

  raw_content = response.choices[0].message.content

  # Parse the structured JSON response back out for Telegram
  try:
    parsed_json = json.loads(raw_content)
    actual_reply = parsed_json.get("response_text", raw_content)
  except json.JSONDecodeError:
    actual_reply = raw_content

  return normalize_reply_text(actual_reply)
    if not response.choices:
        raise RuntimeError("ASI:Cloud Super-Decider returned no completion choices.")
    return normalize_reply_text(response.choices[0].message.content)
    
@unbranded_witness
async def run_rcn_inference(user_id: str, prompt: str):
    """Route a Telegram query through async-compatible safety middleware."""
    return await _request_rcn_inference(user_id, prompt)


# -------------------------------------------------------------------------
# 2. Initialize Telegram Application on its own persistent event loop
# -------------------------------------------------------------------------
telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
bot_loop = asyncio.new_event_loop()
bot_loop_ready = threading.Event()


async def initialize_telegram_app():
    await telegram_app.initialize()
    if WEBHOOK_URL:
        await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
        print(f"✅ Telegram webhook registered: {WEBHOOK_URL}", flush=True)
    else:
        print("⚠️ WEBHOOK_URL not set. Set it to the public HTTPS endpoint to receive updates.", flush=True)


def _run_bot_loop():
    asyncio.set_event_loop(bot_loop)
    bot_loop_ready.set()
    try:
        bot_loop.run_forever()
    finally:
        pending = asyncio.all_tasks(bot_loop)
        for task in pending:
            task.cancel()
        if pending:
            bot_loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        bot_loop.close()


async def _process_telegram_update(payload):
    """Process an update and send the reply using the bot's persistent event loop."""
    message = payload.get("message") or payload.get("edited_message")
    if not isinstance(message, dict):
        print("ℹ️ Update received without a supported text message.", flush=True)
        return

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    user = message.get("from") or {}
    user_id = str(user.get("id", "unknown"))
    incoming_text = message.get("text")

    if not chat_id or not isinstance(incoming_text, str) or not incoming_text.strip():
        print("ℹ️ Update received without chat ID or text.", flush=True)
        return

    print(f"💬 [TEXT] User {user_id}: {incoming_text[:200]}", flush=True)

    try:
        inference_result = run_rcn_inference(user_id=user_id, prompt=incoming_text)
        if inspect.isawaitable(inference_result):
            inference_result = await inference_result

        if isinstance(inference_result, dict):
            inference_result = inference_result.get("agent_response")
        reply_text = normalize_reply_text(inference_result)
        if not reply_text:
            reply_text = "I couldn't generate a response right now."
    except Exception as exc:
        print(f"💥 [INFERENCE ERROR] {type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()
        reply_text = "I hit an error while generating a response. Please try again."

    print(f"🤖 [REPLY]: {reply_text[:80]}...", flush=True)
    try:
        await telegram_app.bot.send_message(chat_id=chat_id, text=reply_text)
        print("✨ [SUCCESS] Reply sent to Telegram!", flush=True)
    except Exception as exc:
        print(f"💥 [SEND ERROR] {type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()


# -------------------------------------------------------------------------
# 3. Unified HTTP Request Handler (Health Checks + Telegram Webhook)
# -------------------------------------------------------------------------
class TelegramWebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"📥 [WEBHOOK HIT] GET request path: {self.path}", flush=True)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"RIAClaw Telegram RCN Node is active and listening via Webhook.")

    def do_HEAD(self):
        print(f"📥 [WEBHOOK HIT] HEAD request path: {self.path}", flush=True)
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        print(f"📥 [WEBHOOK HIT] POST request path: {self.path}", flush=True)
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > 1_000_000:
                self.send_error(400, "Invalid request body size")
                return
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode("utf-8"))
            if not isinstance(payload, dict):
                self.send_error(400, "Expected a JSON object")
                return
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(400, "Invalid JSON payload")
            return

        if not bot_loop.is_running():
            self.send_error(503, "Bot is not ready")
            return

        try:
            future = asyncio.run_coroutine_threadsafe(_process_telegram_update(payload), bot_loop)
            future.add_done_callback(_log_update_failure)
        except RuntimeError as exc:
            print(f"💥 [SCHEDULING ERROR]: {exc}", flush=True)
            self.send_error(503, "Bot is not ready")
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


def _log_update_failure(future):
    try:
        future.result()
    except Exception:
        print("💥 [UNHANDLED UPDATE ERROR]", flush=True)
        traceback.print_exc()


def run_server():
    server = HTTPServer(("0.0.0.0", PORT), TelegramWebhookHandler)
    print(f"🌐 Unified Webhook & Health server listening on port {PORT}...", flush=True)
    server.serve_forever()


# -------------------------------------------------------------------------
# 4. Main Execution Loop & Initialization
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 RIAClaw RCN Telegram Node initializing...", flush=True)
    bot_thread = threading.Thread(target=_run_bot_loop, name="telegram-event-loop", daemon=True)
    bot_thread.start()

    if not bot_loop_ready.wait(timeout=10):
        raise RuntimeError("Telegram event loop did not start within 10 seconds.")

    try:
        asyncio.run_coroutine_threadsafe(initialize_telegram_app(), bot_loop).result(timeout=60)
    except Exception:
        print("💥 Telegram application initialization failed.", flush=True)
        traceback.print_exc()

    run_server()
