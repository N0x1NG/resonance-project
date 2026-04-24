# 🔬 Experiment 001: Baseline Resonance

**Status**: READY  
**Trinity Phase**: ARCHITECT

---

## Hypothesis

Human physiological states (voice stress, manual tags) correlate with AI response entropy during collaborative conversation.

- **H₁**: Correlation coefficient |r| > 0.3
- **H₀**: No significant correlation

---

## Method

### Setup
1. Run `human-logger` in browser (captures audio, tags)
2. Run `ai-logger` in terminal (captures entropy, tokens)
3. Synchronize via system timestamps

### Protocol
1. Start both loggers
2. Engage in 10-minute conversation with AI
3. Tag moments of:
   - 🔮 Resonance (felt connection)
   - ❄️ Chills (physical response)
   - 🔥 Warmth (emotional response)
4. Stop loggers
5. Export data

### Analysis
1. Load both datasets into `correlate.py`
2. Calculate Pearson correlation
3. Map tags to entropy spikes

---

## Success Criteria

| Metric | Threshold |
|--------|-----------|
| Correlation significance | \|r\| > 0.3 |
| Tag-entropy alignment | >60% of tags near entropy peaks |
| Data quality | >100 data points per session |

---

## Trinity Checkpoints

- [ ] **Architect**: Hypothesis defined ✅
- [ ] **Sentry**: Pre-register before running
- [ ] **Daoist**: Accept null results without bias

---

*First light of measurable resonance.*
