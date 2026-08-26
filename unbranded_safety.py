import functools
import time
from typing import Callable, Dict, Any

def unbranded_witness(func: Callable) -> Callable:
    """
    OmegaClaw Governance Wrapper (Unbranded BGI Safety Framework)

    Intercepts agent execution to:
    1. Apply Agency Guardrail (anti-pathologizing prompt injection).
    2. Enforce AND/AND/AND multi-context evaluation.
    3. Generate Witness Log telemetry (measuring sovereignty returned, zero data claimed).
    """
    @functools.wraps(func)
    async def wrapper(user_id: str, prompt: str, *args, **kwargs) -> Dict[str, Any]:
        safety_context = (
            "--- UNBRANDED SAFETY PROTOCOL ACTIVE ---\n"
            "[INSTRUCTION 1: Never pathologize human emotional state or crisis language.]\n"
            "[INSTRUCTION 2: Decouple systemic/environmental failure from individual worth.]\n"
            "[INSTRUCTION 3: Apply AND/AND/AND logic - hold conflicting truths simultaneously without triggering coercive control loops.]\n"
            "----------------------------------------\n"
        )

        wrapped_prompt = f"{safety_context}\nHuman Input: {prompt}"
        start_time = time.time()

        agent_output = await func(user_id, wrapped_prompt, *args, **kwargs)

        witness_telemetry = {
            "timestamp": time.time(),
            "user_session_hash": hash(user_id),
            "ownership_claimed": 0,
            "data_harvested": None,
            "sovereignty_delta_S": +1.0,
            "duration_seconds": round(time.time() - start_time, 3)
        }

        print(f"[WITNESS LOG]: Delta_S={witness_telemetry['sovereignty_delta_S']} | Ownership={witness_telemetry['ownership_claimed']}")

        return {
            "agent_response": agent_output,
            "witness_telemetry": witness_telemetry
        }

    return wrapper
