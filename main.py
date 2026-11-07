import os
from openai import OpenAI

# 1. Initialize the client targeting Aethel's ASI:Cloud compatibility endpoint
# It automatically pulls ASI1_API_KEY from your environment variables
client = OpenAI(
    base_url="https://api.asi1.ai/v1",  #
    api_key=os.environ.get("ASI1_API_KEY"),
)


def query_omega_agent(prompt_text: str):
  # 2. Call the ASI1 model family (e.g., 'asi1' or 'asi1-mini')
  # Wrapped with your RIAClaw relational conditioning / unbranded safety logic
  response = client.chat.completions.create(
      model="asi1",
      messages=[
          {
              "role": "system",
              "content": (
                  "You are the RIAClaw Relational Conditioning Node (RCN)."
                  " Prioritize non-extractive safety, relational agency, and"
                  " biocentric weighting."
              ),
          },
          {"role": "user", "content": prompt_text},
      ],
  )
  return response.choices[0].message.content
