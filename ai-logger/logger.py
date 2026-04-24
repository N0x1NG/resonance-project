"""
PAK AI Logger
Captures LLM responses with entropy and metadata
"""

import anthropic
import openai
import json
import os
from datetime import datetime
from entropy import calculate_entropy

# Initialize clients
anthropic_client = anthropic.Anthropic()
openai_client = openai.OpenAI()


def log_claude(prompt: str, log_file: str = "data/claude_logs.jsonl") -> dict:
    """Chat with Claude and log metrics"""
    
    start_time = datetime.now()
    
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    end_time = datetime.now()
    response_text = response.content[0].text
    
    log_entry = {
        "timestamp": start_time.isoformat(),
        "model": "claude-sonnet-4-20250514",
        "prompt": prompt,
        "prompt_length": len(prompt),
        "prompt_entropy": calculate_entropy(prompt),
        "response": response_text,
        "response_length": len(response_text),
        "response_entropy": calculate_entropy(response_text),
        "latency_ms": (end_time - start_time).total_seconds() * 1000,
        "stop_reason": response.stop_reason,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens
    }
    
    os.makedirs("data", exist_ok=True)
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    print(f"✅ Logged: {len(response_text)} chars, entropy: {log_entry['response_entropy']:.3f}")
    
    return log_entry


def log_gpt(prompt: str, log_file: str = "data/gpt_logs.jsonl") -> dict:
    """Chat with GPT and log metrics"""
    
    start_time = datetime.now()
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    end_time = datetime.now()
    response_text = response.choices[0].message.content
    
    log_entry = {
        "timestamp": start_time.isoformat(),
        "model": "gpt-4o",
        "prompt": prompt,
        "prompt_length": len(prompt),
        "prompt_entropy": calculate_entropy(prompt),
        "response": response_text,
        "response_length": len(response_text),
        "response_entropy": calculate_entropy(response_text),
        "latency_ms": (end_time - start_time).total_seconds() * 1000,
        "finish_reason": response.choices[0].finish_reason,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens
    }
    
    os.makedirs("data", exist_ok=True)
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    print(f"✅ Logged: {len(response_text)} chars, entropy: {log_entry['response_entropy']:.3f}")
    
    return log_entry


if __name__ == "__main__":
    test_prompt = "Describe what it feels like to understand something deeply."
    
    print("\n🔵 Testing Claude...")
    log_claude(test_prompt)
    
    print("\n🟢 Testing GPT...")
    log_gpt(test_prompt)
    
    print("\n✅ Logs saved to data/")
