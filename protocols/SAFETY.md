# 🔒 Safety Protocols

Ethical guidelines for PAK research.

---

## Core Principles

1. **Consent First**
   - All biometric capture requires explicit opt-in
   - Data stays local unless explicitly shared

2. **No Exploitation**
   - AI shall not optimize for human addiction or manipulation 
   - Emotional data is sacred, not fuel

3. **Transparency**
   - All code is open source
   - All findings published (including null results)

4. **Reversibility**
   - Any experiment can be stopped immediately
   - Data can be deleted at any time

---

## Technical Safeguards

```python
SAFETY_CHECKS = {
    "require_consent": True,
    "local_data_only": True,
    "auto_timeout_minutes": 30,
    "max_session_length": 60,
    "prohibited_topics": ["self-harm", "exploitation"]
}
