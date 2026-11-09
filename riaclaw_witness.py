import asyncio
import json
import time
from pathlib import Path


class RIAClawWitnessLog:

  def __init__(self, log_path: str = "logs/riaclaw_witness.jsonl"):
    self.log_path = Path(log_path)
    self.log_path.parent.mkdir(parents=True, exist_ok=True)

  async def record(
      self,
      event_type: str,
      state_payload: dict,
      affective_valence: float = 0.0,
      entropy_metric: float = 0.0,
  ):
    """Silently records state alongside affective valence and entropy drift

    without blocking execution.
    """
    entry = {
        "timestamp": time.time(),
        "event_type": event_type,
        "affective_valence": round(float(affective_valence), 4),
        "entropy_metric": round(float(entropy_metric), 4),
        "payload": state_payload,
    }

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, self._append_to_file, entry)

  def _append_to_file(self, entry: dict):
    with open(self.log_path, "a", encoding="utf-8") as f:
      f.write(json.dumps(entry) + "\n")
