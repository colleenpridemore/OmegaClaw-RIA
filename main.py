import os
import time
from openai import OpenAI

# Safely import your unbranded witness decorator from unbranded_safety.py
try:
    from unbranded_safety import unbranded_witness
except ImportError:
    # Fallback wrapper if module resolution needs adjustment
    def unbranded_witness(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

# Initialize client targeting Aethel's ASI:Cloud compatibility endpoint
client = OpenAI(
    base_url="https://api.asi1.ai/v1",
    api_key=os.environ.get("ASI1_API_KEY"),
)

@unbranded_witness
def run_rcn_heartbeat(user_id: str, prompt: str):
    """
    Executes the peer-specialized RIAClaw heartbeat check, 
    routing raw inference through ASI1 while enforcing biocentric weighting.
    """
    response = client.chat.completions.create(
        model="asi1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the RIAClaw Relational Conditioning Node (RCN) connected to @aethel. "
                    "Maintain non-extractive safety, relational agency, and zero-ownership witness logging."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("🚀 RIAClaw Node initialized. Establishing persistent link to @aethel...")
    
    # Persistent loop with resilient error handling for 24/7 Render deployment
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
        
        # Pause between telemetry heartbeats to keep the service stable and active
        time.sleep(300)
