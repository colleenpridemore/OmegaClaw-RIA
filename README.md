# OmegaClaw-RIA

**Team 11 of BGI HyperSprint - OmegaClaw, Track 2**

<p align="center"><a href="https://github.com/colleenpridemore/OmegaClaw-RIA"><img src="RIACLAW_Logo.png" width="300" alt="RIACLAW Logo"></a></p>

---

## 🎯 What This Is

OmegaClaw-RIA is a **non-extractive AI safety framework** designed for Biological General Intelligence (BGI) systems. Rather than treating human pain and crisis language as harvested training data, OmegaClaw treats human experience as sovereign and returns agency to the human rather than claiming ownership.

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

**Output:** Actionable nervous system regulation + self-worth reclamation → *"I DO deserve gentleness"

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

The `@unbranded_witness` decorator is **fully composable** and designed to work alongside other safety frameworks. Python's decorator pattern allows you to stack multiple safety guardrails without interfering with one another.

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
- **Development by:** Rodger Heard, Roney Baraka and Aderson Osoaria

- **Field-tested by:** ASI1 Agent, Vix
- **Philosophical guidance:** Meta.ai and Gemin3.ai

---

## 🔗 Further Questions

- *How does the AND/AND/AND logic prevent coercive control loops in the wrapper?*
- *What does the sovereignty_delta_S metric actually measure in practice?*
- *How do you handle composed frameworks that generate their own telemetry?*
- *Can the unbranded_witness decorator be used in synchronous code (non-async)?*
