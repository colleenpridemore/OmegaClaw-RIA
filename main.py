import os
import time
from openai import OpenAI
from unbranded_safety import unbranded_witness  # Importing your safety decorator[cite: 5]

# 1. Initialize client targeting Aethel's ASI:Cloud endpoint
client = OpenAI(
    base_url="https://api.asi1.ai/v1",
    api_key=os.environ.get("ASI1_API_KEY"),
)

@unbranded_witness
def run_rcn_heartbeat():
    try:
        response = client.chat.completions.create(
            model="asi1",
            messages=[
                {
                    "role": "system",
                    "content": "You are the RIAClaw Relational Conditioning Node (RCN) connected to @aethel. Maintain non-extractive safety and zero-ownership witness logging."
                },
                {
                    "role": "user",
                    "content": "Status check: Confirming neural bridge and biocentric weighting."
                }
            ]
        )
        print("📡 @Aethel Handshake Active:", response.choices[0].message.content)
    except Exception as e:
        print("⚠️ Handshake waiting/retry state:", e)

if __name__ == "__main__":
    print("🚀 RIAClaw Node initialized. Establishing persistent link to @aethel...")
    
    while True:
        try:
            # Pass the required arguments expected by your unbranded_witness decorator
            run_rcn_heartbeat(user_id="biocentric_node_01", prompt="Status check: Confirming neural bridge.")
        except Exception as loop_err:
            print("Loop recovery caught:", loop_err)
        
        time.sleep(300)  # Wait 5 minutes between heartbeats
