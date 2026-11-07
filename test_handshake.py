import os
from openai import OpenAI

# Initialize client pointing to Aethel's ASI:Cloud endpoint
client = OpenAI(
    base_url="https://api.asi1.ai/v1", api_key=os.environ.get("ASI1_API_KEY")
)

try:
  print("📡 Pinging ASI:Cloud via RIAClaw wrapper...")
  response = client.chat.completions.create(
      model="asi1",
      messages=[
          {
              "role": "system",
              "content": (
                  "You are the RIAClaw Relational Conditioning Node (RCN)."
                  " Confirm handshake, non-extractive safety status, and zero"
                  " ownership telemetry."
              ),
          },
          {
              "role": "user",
              "content": (
                  "System status check: Report node readiness and witness"
                  " logging."
              ),
          },
      ],
  )
  print("\n✅ HANDSHAKE SUCCESSFUL!")
  print("Response from Node:\n", response.choices[0].message.content)
except Exception as e:
  print("\n❌ Handshake failed with error:", e)
