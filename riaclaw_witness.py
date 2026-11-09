import asyncio
import json
import time
from pathlib import Path


class RIAClawWitnessLog:

  def __init__(self, log_path: str = "logs/riaclaw_witness.jsonl"):
    self.log_path = Path(log_path)
    # Ensure local log directory exists without friction
    self.log_path.parent.mkdir(parents=True, exist_ok=True)

  async def record(self, event_type: str, state_payload: dict):
    """Silently records state and affective drift asynchronously

    without blocking primary agent execution or enforcing rules.
    """
    entry = {
        "timestamp": time.time(),
        "event_type": event_type,
        "payload": state_payload,
    }

    # Non-blocking append write
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, self._append_to_file, entry)

  def _append_to_file(self, entry: dict):
    with open(self.log_path, "a", encoding="utf-8") as f:
      f.write(json.dumps(entry) + "\n")
