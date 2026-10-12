from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'docs/agent-profile'
def load_profile():
 names=('persona','scope','safety','verification','payments','question-fallback')
 return {name:(ROOT/(name+'.md')).read_text(encoding='utf-8').strip() for name in names}
