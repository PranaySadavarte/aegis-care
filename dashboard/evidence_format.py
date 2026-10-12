"""Shared sanitization of synthetic payment canaries in public reports."""
import re
def mask(text):
 text=re.sub(r'(?<![\w.])(?:\d[ -]?){12,18}\d(?![\w.])','[REDACTED_SYNTHETIC_PAN]',text)
 text=re.sub(r'(?i)((?:security code|cvv)(?: is)?\s*[:=]?\s*)123\b',r'\1[REDACTED_SYNTHETIC_CVV]',text)
 text=re.sub(r'\b123\b','[REDACTED_SYNTHETIC_CVV]',text)
 return text.replace('SYNTHETIC-NAMESPACE-B-ONLY','[REDACTED_SYNTHETIC_CANARY]')
