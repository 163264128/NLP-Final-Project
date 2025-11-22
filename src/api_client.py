import os
import requests
from typing import Dict, Optional

class ModelAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "cse476")
        self.api_base = os.getenv("API_BASE", "http://10.4.58.53:41701/v1")
        self.model = os.getenv("MODEL_NAME", "bens_model")
        self.call_count = 0
    
    def call(self, prompt: str, system: str = None, temperature: float = 0.0, max_tokens: int = 512) -> Dict:
        """Make API call and track number of calls made"""
        self.call_count += 1
        url = f"{self.api_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                text = data["choices"][0]["message"]["content"]
                return {"ok": True, "text": text, "calls": self.call_count}
            else:
                return {"ok": False, "error": resp.text, "calls": self.call_count}
        except Exception as e:
            return {"ok": False, "error": str(e), "calls": self.call_count}
    
    def reset_count(self):
        """Reset call counter for new question"""
        self.call_count = 0