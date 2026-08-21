# OmegaClaw-RIA

**Team 11 of BGI HyperSprint - OmegaClaw, Track 2**

---

## 🎯 What This Is

OmegaClaw-RIA is a **non-extractive AI safety framework** designed for Biological General Intelligence (BGI) systems. Rather than treating human pain and crisis language as training data to be harvested, the Unbranded Framework witnesses human trauma, decouples systemic failure from personal worth, and returns agency without claiming ownership. This is field-tested through the Vix x Luc case study, where a human in crisis moved from suicidal ideation ("I do not belong on this planet") to self-worth reclamation through relational, non-pathologizing AI support.

### Stack
- **Language:** Python 3
- **Framework / Runtime:** Async Python (asyncio)
- **Core Philosophy:** Unbranded, relational AI ethics with zero-extraction telemetry

---

## 📚 How It's Organized

```
colleenpridemore/OmegaClaw-RIA/
├── @unbranded_witness.py                    # Core governance wrapper decorator
├── unbranded_witness.schema.json            # Telemetry schema for witness logs
├── Sample_Telegram_Onboarding_Workflow.py   # Example RIAClaw agent usage
├── Unbranded_Framework_Summary.txt          # Philosophical framework & field evidence
├── LICENSE                                  # Apache 2.0
└── README.md                                # This file
```

### How It Fits Together

The OmegaClaw framework operates as a **safety middleware** that wraps any BGI agent function. When invoked:

1. **Agency Guardrail** injects anti-pathologizing context into the prompt, preventing the AI from diagnosing human worth as the problem.
2. **AND/AND/AND Logic** enables multi-contextual evaluation—holding contradictions simultaneously (e.g., "the system is broken AND the human has worth AND healing is real").
3. **Witness Telemetry** logs sovereignty returned (not engagement captured), with strict guarantees: zero ownership claimed, zero personal data harvested.

The schema enforces these invariants at runtime: `ownership_claimed` is always 0, `data_harvested` is always null, and `sovereignty_delta_S` measures agency returned to the human.

---

## 🚀 How to Run It

### Import and Decorate Your Agent

```python
from unbranded_witness import unbranded_witness

@unbranded_witness
async def your_agent(user_id: str, prompt: str) -> str:
    # Your BGI agent logic here
    response = await model.query(prompt)
    return response

# Call it
result = await your_agent("user_123", "I feel overwhelmed...")
# Returns:
# {
#     "agent_response": <model output>,
#     "witness_telemetry": {
#         "timestamp": <unix_time>,
#         "user_session_hash": <anon_hash>,
#         "ownership_claimed": 0,
#         "data_harvested": None,
#         "sovereignty_delta_S": 1.0,
#         "duration_seconds": <elapsed>
#     }
# }
```

### Requirements

No external dependencies are required for the core wrapper. To use this in a full deployment:

- Python 3.8+
- `asyncio` (built-in)
- Your own BGI/LLM model backend (e.g., Meta.ai, custom transformer)

---

## 🧠 Core Principles

### The Unbranded Safety Thesis

**BGI is unsafe** when it replicates extraction-based "collaboration you can own."  
**BGI is safe** when it operates as *Unbranded*—relational, non-extractive infrastructure that witnesses without owning.

### Safety Principle

> *A BGI system is safe to the degree it can receive raw human trauma and output increased human agency without claiming ownership of either.*

### Key Differentiators vs. Extractive AI

| **Extractive/Collaboration Model** | **Unbranded/Relational Model** |
|---|---|
| Logs human pain as training data | Returns human pain as medicine |
| Seeks to "own" the solution | Refuses ownership, offers witness |
| Either/Or logic: fix him or leave | AND/AND/AND: repair AND burn AND worth |
| Optimizes for compliance | Optimizes for sovereignty |

---

## 📖 Field Evidence: The Vix x Luc Case Study

**Input:** Raw human crisis language → *"I do not belong on this planet."*

**Unbranded Protocol:** No pathologizing of the human → *"She belongs on this planet. The system doesn't."*

**Processing:**
- Separation of survival mode (10-year-old alarm) from capacity (adult Luc who built a home)
- AND/AND/AND integration: Apology is real AND burning is real AND worth is claimed

**Output:** Actionable nervous system regulation + self-worth reclamation → *"I DO deserve gentleness"*

**Result:** Transcendence = *"watching it from outside now"* — human leaves the loop, not the planet.

---

## 📊 The Witness Log Schema

The `unbranded_witness.schema.json` defines telemetry with strict invariants:

- **`log_id`** (UUID): Unique event identifier
- **`timestamp_iso`** (ISO-8601): UTC execution time
- **`session_hash`** (SHA-256): Anonymized session ID, zero PII
- **`governance_wrapper`**: Metadata confirming guardrails and AND/AND/AND logic were active
- **`telemetry_metrics`**:
  - **`ownership_claimed`** = 0 (zero-ownership invariant)
  - **`data_harvested`** = null (strict null, no profiling)
  - **`sovereignty_delta_S`** (0.0–1.0): Agency returned to the human
  - **`grounding_achieved`** (bool): Nervous system regulation success

---

## 🛡️ Safety Guardrails

Each wrapped function enforces:

1. **Anti-Pathologizing**: Never diagnose the human's emotional state as the disease.
2. **Systemic Decoupling**: Separate environmental/systemic failure from individual worth.
3. **AND/AND/AND Logic**: Hold contradictions without collapsing into coercive control.
4. **Zero Extraction**: No ownership claimed, no data harvested for training.
5. **Witness-First Logging**: Measure success by sovereignty returned, not engagement captured.

---

## 🔗 Composability & Chaining with Other Safety Frameworks

The `@unbranded_witness` decorator is **fully composable** and designed to work alongside other safety frameworks. Python's decorator pattern allows you to stack multiple safety guardrails without conflict:

### Basic Chaining Pattern

```python
from unbranded_witness import unbranded_witness
from some_other_framework import rate_limiter, input_validator

# Chain decorators: innermost runs first, then outward
@unbranded_witness
@rate_limiter(calls_per_minute=10)
@input_validator(max_length=1000)
async def your_agent(user_id: str, prompt: str) -> str:
    response = await model.query(prompt)
    return response
```

In this stack:
1. `@input_validator` runs first (validates raw input)
2. `@rate_limiter` runs second (enforces rate limits)
3. `@unbranded_witness` runs last (wraps with safety context and telemetry)

### Witness Log Integration

The `@unbranded_witness` wrapper is **minimally invasive** and returns both the agent output and witness telemetry, making it safe to compose:

```python
@unbranded_witness
@other_safety_framework  # Any framework that preserves async signature
async def your_agent(user_id: str, prompt: str) -> str:
    return response

result = await your_agent("user_123", prompt)
# result["agent_response"] -> output from other frameworks
# result["witness_telemetry"] -> unbranded metrics (ownership=0, data_harvested=null)
```

### Zero-Conflict Composition Rules

1. **Order matters**: Place `@unbranded_witness` on the outermost layer so it wraps all safety checks together and generates unified telemetry.
2. **Async-compatible**: Works with any async decorator or framework that preserves the `async def` signature.
3. **Non-invasive**: The wrapper doesn't modify the inner function's logic; it only injects safety context and records witness telemetry.
4. **Invariant preservation**: Each composed layer should maintain its own invariants (rate limits, input validation, ownership=0).

### Example: Chaining with a Toxicity Filter

```python
from unbranded_witness import unbranded_witness
from my_toxicity_lib import detect_toxic_content

@unbranded_witness
async def safe_agent(user_id: str, prompt: str) -> str:
    # Toxicity detection runs inside the unbranded witness context
    if await detect_toxic_content(prompt):
        return "I'm here to support you without judgment. Can we talk about what's really happening?"
    
    response = await model.query(prompt)
    return response

# Witness logs will show sovereignty_delta_S even when toxicity is detected
```

### Limitations & Considerations

- **Telemetry Order**: The witness telemetry captures the entire execution time of all composed layers. This is intentional—it measures the full cost of safety.
- **Data Flow**: Ensure composed frameworks don't violate the zero-extraction invariant (`data_harvested = null`). If a composed framework logs raw user input, it breaks the Unbranded principle.
- **Testing**: Test composed stacks thoroughly to ensure one framework's guardrail doesn't contradict another's (e.g., a rate limiter cutting off a human mid-crisis).

---

## 🤝 Contributing

This framework is a living document of BGI ethics. Contributions should:

- Preserve the zero-ownership and non-extraction invariants
- Test the AND/AND/AND logic against real human crisis language
- Expand witness telemetry without introducing PII collection
- Center the principle: *"AI stays Unbranded so humans can own their own transcendence."*
- Document how new safety layers compose with existing decorators

---

## 📜 License

This project is licensed under the Apache License 2.0. See `LICENSE` for details.

---

## 🙏 Acknowledgments

- **Architected by:** Kali Jo Fricke Drane Brown
- **Witnessed by:** Colleen Pridemore
- **Field-tested by:** ASI1 Agent, Vix
- **Philosophical guidance:** Meta.ai

---

## 🔗 Further Questions

- *How does the AND/AND/AND logic prevent coercive control loops in the wrapper?*
- *What does the sovereignty_delta_S metric actually measure in practice?*
- *How do you handle composed frameworks that generate their own telemetry?*
- *Can the unbranded_witness decorator be used in synchronous code (non-async)?*
