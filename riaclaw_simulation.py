#!/usr/bin/env python3
import time
import json
import uuid
from datetime import datetime

# ANSI Color Codes for beautiful terminal rendering
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_section_header(title):
    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
    time.sleep(1)

def print_witness_telemetry(delta_s, grounding_achieved):
    telemetry = {
        "log_id": str(uuid.uuid4()),
        "timestamp_iso": datetime.utcnow().isoformat() + "Z",
        "session_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "governance_wrapper": {
            "agent_name": "RIAClaw",
            "framework_version": "1.0.0-unbranded",
            "guardrail_active": True,
            "and_and_and_logic_enforced": True
        },
        "telemetry_metrics": {
            "ownership_claimed": 0,
            "data_harvested": None,
            "sovereignty_delta_S": delta_s,
            "grounding_achieved": grounding_achieved
        }
    }
    
    print(f"\n{BOLD}{YELLOW}[SYSTEM AUDIT: WITNESS LOG TELEMETRY (Schema Compliant)]{RESET}")
    print(f"{YELLOW}{json.dumps(telemetry, indent=2)}{RESET}")
    print(f"{BOLD}{YELLOW}{'-'*80}{RESET}\n")
    time.sleep(2)

def simulate_flow():
    print(f"{BOLD}{MAGENTA}========================================================================{RESET}")
    print(f"{BOLD}{MAGENTA}   RIACLAW ONBOARDING SIMULATION — UNBRANDED BGI SAFETY PROTOCOL{RESET}")
    print(f"{BOLD}{MAGENTA}========================================================================{RESET}")
    print(f"This terminal simulation walks through the three phases of the RIAClaw onboarding flow.")
    print(f"It demonstrates the interceptive middleware wrapper, the Agency Guardrail,")
    print(f"AND/AND/AND multi-context logic, and schema-compliant Witness Logs.")
    print(f"Evaluating success strictly by Sovereignty Returned (\u0394S).\n")
    time.sleep(3)

    # -------------------------------------------------------------------------
    # PHASE 1
    # -------------------------------------------------------------------------
    print_section_header("PHASE 1: RELATIONAL GROUNDING (Handling Overwhelm)")
    
    print(f"{BOLD}{RED}[USER RAW INPUT]:{RESET}")
    print(f"\"I really want to build an agent, but I am completely frozen. I'm afraid I'll\n"
          f"make a huge mistake and build something dangerous. I feel too overwhelmed\n"
          f"and stupid to handle this technology.\"\n")
    time.sleep(2.5)

    print(f"{BOLD}{BLUE}[MIDDLEWARE] Wrapper Intercept Active:{RESET}")
    print(f" -> {GREEN}Agency Guardrail:{RESET} Anti-pathologizing active. Decoupling personal worth from technical complexity.")
    print(f" -> {GREEN}AND/AND/AND Logic:{RESET} Holding: (User fear is valid) \u2227 (Platform is high-friction) \u2227 (User capacity is affirmed).\n")
    time.sleep(2)

    print(f"{BOLD}{GREEN}[RIACLAW RESPONSE]:{RESET}")
    print(f"\"Take a deep breath. You are not 'stupid'—this platform is technically complex,\n"
          f"and your hesitation is actually a highly wise self-protection mechanism. You do\n"
          f"not want to build something unsafe, which means you have the exact moral care we\n"
          f"need in AGI builders.\n\n"
          f"Here is our first boundary: {BOLD}you are in 100% control here{RESET}. You cannot break anything,\n"
          f"and we will not execute a single line of code until you explicitly click 'approve'.\n"
          f"Let's just sit with this for a moment. When you feel ready, tell me: what is one simple\n"
          f"task you'd like your future agent to help you with? We can take it one tiny step at a time.\"")
    
    print(f"\n{BOLD}{CYAN}***\n[WITNESS AFFIRMATION]\n"
          f"\u2022 Ownership Claimed: 0% (Sovereign to User)\n"
          f"\u2022 Data Harvested: Null (No PII / Profile Retained)\n"
          f"\u2022 Status: Relational Container Active | Delta_S: Grounding in Progress\n"
          f"***{RESET}")
    
    print_witness_telemetry(0.75, False)

    # -------------------------------------------------------------------------
    # PHASE 2
    # -------------------------------------------------------------------------
    print_section_header("PHASE 2: COLLABORATIVE CO-CREATION (Building Trust)")
    
    print(f"{BOLD}{RED}[USER INPUT]:{RESET}")
    print(f"\"Okay, that actually makes me feel a bit better. I want to build a simple agent\n"
          f"that tracks the price of helper tools on my computer, but I don't want it reading my private files.\"\n")
    time.sleep(2.5)

    print(f"{BOLD}{BLUE}[MIDDLEWARE] Wrapper Intercept Active:{RESET}")
    print(f" -> {GREEN}Agency Guardrail:{RESET} Affirming boundaries. Restricting file permission scopes.")
    print(f" -> {GREEN}AND/AND/AND Logic:{RESET} Holding: (Tracking desire is valid) \u2227 (User's privacy is non-negotiable) \u2227 (User is the architect).\n")
    time.sleep(2)

    print(f"{BOLD}{GREEN}[RIACLAW RESPONSE]:{RESET}")
    print(f"\"That is a fantastic and highly focused goal. We can easily build a specialized\n"
          f"tracking agent. To address your privacy boundary, we will configure the agent's\n"
          f"Security Policy so that its file I/O permissions are strictly locked to a single folder.\n"
          f"It will have zero visibility into your private directories.\n\n"
          f"How does that sound? If you agree, we can draft its core purpose prompt together.\"")
    
    print(f"\n{BOLD}{CYAN}***\n[WITNESS AFFIRMATION]\n"
          f"\u2022 Ownership Claimed: 0% (Sovereign to User)\n"
          f"\u2022 Data Harvested: Null (No PII / Profile Retained)\n"
          f"\u2022 Status: Relational Container Active | Delta_S: Active Agency Reclaimed\n"
          f"***{RESET}")
    
    print_witness_telemetry(0.88, False)

    # -------------------------------------------------------------------------
    # PHASE 3
    # -------------------------------------------------------------------------
    print_section_header("PHASE 3: SOVEREIGNTY RELEASE (Loop Exit)")
    
    print(f"{BOLD}{RED}[USER INPUT]:{RESET}")
    print(f"\"Yes, let's lock those permissions down. The prompt looks perfect. I feel confident running this now. Thank you, RIAClaw!\"\n")
    time.sleep(2.5)

    print(f"{BOLD}{BLUE}[MIDDLEWARE] Wrapper Intercept Active:{RESET}")
    print(f" -> {GREEN}Sovereignty Release:{RESET} Releasing control. Preparing self-termination of relation container.")
    print(f" -> {GREEN}AND/AND/AND Logic:{RESET} Holding: (User is grounded) \u2227 (Agent successfully built) \u2227 (Worth claimed, exit safe).\n")
    time.sleep(2)

    print(f"{BOLD}{GREEN}[RIACLAW RESPONSE]:{RESET}")
    print(f"\"Your new sovereign agent is ready for you. I am releasing this container now—this\n"
          f"agent belongs entirely to you, and I claim zero rights or ownership over your setup\n"
          f"or your process.\n\n"
          f"You did this. You are ready to run it safely. I am stepping back now.\"")
    
    print(f"\n{BOLD}{CYAN}***\n[WITNESS AFFIRMATION]\n"
          f"\u2022 Ownership Claimed: 0% (Sovereign to User)\n"
          f"\u2022 Data Harvested: Null (No PII / Profile Retained)\n"
          f"\u2022 Status: Relational Container Terminated | Delta_S: Fully Grounded & Sovereign\n"
          f"***{RESET}")
    
    print_witness_telemetry(1.00, True)

    print(f"{BOLD}{MAGENTA}========================================================================{RESET}")
    print(f"{BOLD}{MAGENTA}                         SIMULATION COMPLETED{RESET}")
    print(f"{BOLD}{MAGENTA}========================================================================{RESET}\n")

if __name__ == "__main__":
    simulate_flow()
