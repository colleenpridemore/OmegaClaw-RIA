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

API_KEY = os.environ.get("ASI_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("ASI_API_KEY is not set. Please configure it in the deployment environment.")

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Please configure it in the deployment environment.")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", "10000"))
TARGET_MODEL = os.environ.get("MODEL_NAME") or "super-decider"
ASI_DEBUG = os.environ.get("ASI_DEBUG", "false").strip().lower() in {"1", "true", "yes", "on"}
# Full prompt/response text may contain private Telegram messages. Only enable
# content logging temporarily when needed; never log API keys or auth headers.
ASI_DEBUG_LOG_CONTENT = os.environ.get("ASI_DEBUG_LOG_CONTENT", "false").strip().lower() in {"1", "true", "yes", "on"}
ASI_BASE_URL = "https://inference.asicloud.cudos.org/v1"

print(f"🔌 Initializing ASI:Cloud client | Model: {TARGET_MODEL} | Debug: {ASI_DEBUG}", flush=True)

client = AsyncOpenAI(
    base_url=ASI_BASE_URL,
    api_key=API_KEY,
    timeout=45.0,
)


def _asi_debug(event: str, details: dict) -> None:
    """Emit opt-in ASI diagnostics without exposing credentials."""
    if ASI_DEBUG:
        print(f"[ASI DEBUG] {event}: {json.dumps(details, ensure_ascii=False, default=str)}", flush=True)


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
    """Send an OpenAI-compatible chat-completion request to ASI:Cloud."""
    messages = [{"role": "user", "content": prompt}]
    request_info = {
        "method": "POST",
        "endpoint": f"{ASI_BASE_URL}/chat/completions",
        "model": TARGET_MODEL,
        "message_count": len(messages),
        "messages": [
            {
                "role": message["role"],
                "content_length": len(message["content"]),
                **({"content": message["content"]} if ASI_DEBUG_LOG_CONTENT else {}),
            }
            for message in messages
        ],
    }
    _asi_debug("request", request_info)

    try:
        response = await client.chat.completions.create(
            model=TARGET_MODEL,
            messages=messages,
        )
    except Exception as exc:
        error_info = {
            "exception_type": type(exc).__name__,
            "status_code": getattr(exc, "status_code", None),
            "code": getattr(exc, "code", None),
            "message": str(exc),
        }
        _asi_debug("request_failed", error_info)
        raise

    if not response.choices:
        _asi_debug("empty_response", {"response_id": getattr(response, "id", None)})
        raise RuntimeError("ASI:Cloud Super-Decider returned no completion choices.")

    raw_content = response.choices[0].message.content
    _asi_debug("response", {
        "response_id": getattr(response, "id", None),
        "model": getattr(response, "model", None),
        "choices": len(response.choices),
        "finish_reason": response.choices[0].finish_reason,
        "content_length": len(raw_content) if isinstance(raw_content, str) else None,
        **({"content": raw_content} if ASI_DEBUG_LOG_CONTENT else {}),
    })

    if raw_content is None:
        return ""

    # Accept plain-text completions and common JSON-wrapped response formats.
    try:
        parsed_json = json.loads(raw_content)
    except (TypeError, ValueError):
        return normalize_reply_text(raw_content)

    if isinstance(parsed_json, dict):
        for key in ("answer", "answers", "decision", "decisions", "response_text", "text"):
            if key in parsed_json:
                return normalize_reply_text(parsed_json[key])

    return normalize_reply_text(raw_content)


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
