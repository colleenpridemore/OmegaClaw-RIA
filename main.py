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
    
    # Keep the container alive as a 24/7 daemon loop for Render, 
    # executing your relational witness checks safely over time.
    while True:
        run_rcn_heartbeat()
        time.sleep(300)  # Pings / syncs every 5 minutes
