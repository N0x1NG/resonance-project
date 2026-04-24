# 📊 Analysis Tools

This folder contains tools for correlating human biometrics with AI responses.

---

## Files

| File | Purpose |
|------|---------|
| `correlate.py` | Pearson correlation between human/AI data |

---

## Usage

```python
from correlate import load_human_data, load_ai_data, correlate_session

# Load exported data
human = load_human_data('../data/pak-human-log-xxxxx.json')
ai = load_ai_data('../data/claude_logs.jsonl')

# Run correlation
results = correlate_session(human, ai)

# View results
print(results['summary'])
print(results['tags'])
print(results['audio_vs_entropy'])

Data is the bridge between poetry and proof.
