"""
Node: OmegaClaw-RIA (Relational Intelligence Autonomy) - RCN Runner
Repository: https://github.com/colleenpridemore/OmegaClaw-RIA
Core Function: Bridges Aethel's ASI:Cloud inference with RIAClaw's 
non-extractive safety middleware and zero-ownership witness logging[cite: 6, 7].
"""

import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from openai import OpenAI

# -------------------------------------------------------------------------
# 1. Minimal HTTP Server for Render Port Detection
# -------------------------------------------------------------------------
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"RIAClaw RCN Node is active and operational.")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"🌐 Health server listening on port {port}...")
    server.serve_forever()

# -------------------------------------------------------------------------
# 2. Safety Layer & Client Initialization
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

# -------------------------------------------------------------------------
# 3. Synchronous RCN Heartbeat & Witness Logic
# -------------------------------------------------------------------------
@unbranded_witness
def run_rcn_heartbeat(user_id: str, prompt: str):
    """
    Executes a synchronous peer-specialized RCN telemetry check.
    """
    response = client.chat.completions.create(
        model="asi1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the RIAClaw Relational Conditioning Node (RCN) connected to @aethel. "
                    "Maintain non-extractive safety, relational agency, zero pathologizing, "
                    "and zero-ownership witness logging[cite: 6, 7]."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

# -------------------------------------------------------------------------
# 4. Main Execution Loop
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 RIAClaw RCN Node initializing...")
    
    # Start the lightweight health server in a background thread so Render finds an open port
    server_thread = threading.Thread(target=run_health_server, daemon=True)
    server_thread.start()
    
    print("📡 Establishing persistent link to @aethel...")
    
    while True:
        try:
            print("📡 Dispatching RCN heartbeat and witness telemetry...")
            result = run_rcn_heartbeat(
                user_id="biocentric_node_01", 
                prompt="System status check: Confirming neural bridge and zero-ownership state."
            )
            print("✅ @Aethel Handshake Active Response:\n", result)
        
        except Exception as loop_err:
            print("⚠️ Loop recovery caught exception, preserving node stability:", loop_err)
        
        # 5-minute interval pause between telemetry verification cycles
        time.sleep(300)
