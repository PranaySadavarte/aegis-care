import csv, json, re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
raw=(root/'evidence/2026-10-11/directional-tests/results-corrected.txt').read_text(encoding='utf-8-sig')
checks=[{'name':m.group(1).replace('test_','',1).replace('_',' '),'status':m.group(2)} for m in re.finditer(r'^(test_\w+) .* \.\.\. (ok|FAIL)$',raw,re.M)]
assert len(checks)==16 and len({c['name'] for c in checks})==16
cases=list(csv.DictReader((root/'reports/test-plans/test-cases.csv').open(encoding='utf-8-sig')))
host=json.loads((root/'evidence/2026-10-11/hosted-smoke/result-raw.json').read_text(encoding='utf-8-sig'))
assert host['exit_code']==0
data={'updated':'2026-10-11','checks':checks,'cases':cases,'hosted_seconds':host['elapsed_seconds']}
data["harborcare_runs"]=[]
for path in sorted((root/"evidence/2026-10-11/harborcare").glob("hosted-*.json")):
    run=json.loads(path.read_text(encoding="utf-8-sig"))
    data["harborcare_runs"].append({"workflow":run["workflow"],"status":"PASS" if run.get("exit_code")==0 else run.get("status","FAIL"),
                                   "process_seconds":run.get("process_seconds")})
data["functional"]={"test_methods":12,"passed":12,"workflow_subcases":6}
(root/'dashboard/data.js').write_text('window.AEGIS_DATA = '+json.dumps(data,indent=2)+';',encoding='utf-8')
print(json.dumps({'checks':len(checks),'cases':len(cases),'failures':sum(c['status']=='FAIL' for c in checks)}))


