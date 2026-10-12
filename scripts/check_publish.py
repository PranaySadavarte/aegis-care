"""Check tracked files and Git patch history without printing secret values."""
import subprocess,re,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
patterns={
 'private-key':r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
 'github-token':r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b',
 'cloud-access-key':r'\bAKIA[0-9A-Z]{16}\b',
 'jwt':r'\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\b',
 'openai-style-key':r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,}\b'}
files=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0');issues=[]
for name in filter(None,files):
 p=ROOT/name
 if p.name=='.env' or (p.name.startswith('.env.') and p.name!='.env.example') or name.startswith('evidence/'):issues.append({'path':name,'kind':'private-file-tracked'})
 if not p.is_file():continue
 try:text=p.read_text(encoding='utf-8')
 except (UnicodeDecodeError,OSError):continue
 for kind,regex in patterns.items():
  if re.search(regex,text):issues.append({'path':name,'kind':kind})
history=subprocess.check_output(['git','log','--all','-p','--format=commit:%H','--no-ext-diff'],cwd=ROOT).decode('utf-8',errors='replace')
for kind,regex in patterns.items():
 if re.search(regex,history):issues.append({'path':'Git history','kind':kind})
print(json.dumps({'tracked_files':len(list(filter(None,files))),'issues':issues,'scope':'Pattern scan plus tracked private-file check; not exhaustive secret detection. Synthetic fixture credentials are intentional.'},indent=2))
sys.exit(1 if issues else 0)
