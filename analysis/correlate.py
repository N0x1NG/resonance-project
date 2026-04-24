"""
Correlation analysis between human biometrics and AI responses
"""

import json
import math
from collections import Counter


def load_human_data(filepath: str) -> list:
    """Load human logger JSON export"""
    with open(filepath, 'r') as f:
        return json.load(f)


def load_ai_data(filepath: str) -> list:
    """Load AI logger JSONL"""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def pearson_correlation(x: list, y: list) -> float:
    """Calculate Pearson correlation coefficient"""
    n = len(x)
    if n != len(y) or n == 0:
        return 0.0
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    
    sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
    sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    
    if denominator == 0:
        return 0.0
    
    return round(numerator / denominator, 4)


def correlate_session(human_data: list, ai_data: list) -> dict:
    """
    Find correlations between human states and AI responses.
    """
    results = {
        "audio_vs_entropy": None,
        "tags": {},
        "summary": ""
    }
    
    # Extract ambient audio levels
    audio_levels = [
        entry['value']['audioLevel'] 
        for entry in human_data 
        if entry.get('event') == 'ambient' 
        and isinstance(entry.get('value'), dict)
        and 'audioLevel' in entry['value']
    ]
    
    # Extract AI entropy values
    ai_entropies = [entry['response_entropy'] for entry in ai_data]
    
    # Correlate if enough data
    if len(audio_levels) >= 3 and len(ai_entropies) >= 3:
        min_len = min(len(audio_levels), len(ai_entropies))
        r = pearson_correlation(audio_levels[:min_len], ai_entropies[:min_len])
        results["audio_vs_entropy"] = {
            "pearson_r": r,
            "sample_size": min_len,
            "significant": abs(r) > 0.3
        }
    
    # Analyze manual tags
    tags = [
        entry['value']['tag'] 
        for entry in human_data 
        if entry.get('event') == 'manual_tag'
        and isinstance(entry.get('value'), dict)
    ]
    results["tags"] = dict(Counter(tags)) if tags else {}
    
    # Summary
    if results["audio_vs_entropy"]:
        r = results["audio_vs_entropy"]["pearson_r"]
        if abs(r) > 0.7:
            strength = "STRONG"
        elif abs(r) > 0.4:
            strength = "MODERATE"
        else:
            strength = "WEAK"
        
        direction = "POSITIVE" if r > 0 else "NEGATIVE"
        results["summary"] = f"{strength} {direction} correlation (r={r})"
    else:
        results["summary"] = "Insufficient data for correlation"
    
    return results


if __name__ == "__main__":
    print("=" * 50)
    print("PAK CORRELATION ANALYZER")
    print("=" * 50)
    print("\nUsage:")
    print("  from correlate import load_human_data, load_ai_data, correlate_session")
    print("  human = load_human_data('path/to/human-log.json')")
    print("  ai = load_ai_data('path/to/claude_logs.jsonl')")
    print("  results = correlate_session(human, ai)")
    print("  print(results['summary'])")
    print("\n✅ Ready for analysis")
