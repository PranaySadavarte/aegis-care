import subprocess, pathlib, json, time
root = pathlib.Path(__file__).resolve().parents[2]
started = time.monotonic()
try:
    result = subprocess.run([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),
                             str(root/"tests/integration/hosted_smoke.py")],
                            capture_output=True, text=True, timeout=60, cwd=root)
    record = {"exit_code":result.returncode, "stdout":result.stdout, "stderr":result.stderr,
              "elapsed_seconds":time.monotonic()-started}
except subprocess.TimeoutExpired:
    record = {"status":"TIMEOUT", "limit_seconds":60,
              "note":"Parent bounded process wait; hosted server cleanup not independently verified"}
(root/"evidence/2026-10-11/hosted-smoke/result-raw.json").write_text(json.dumps(record,indent=2))
print(json.dumps({"exit_code":record.get("exit_code"),"status":record.get("status"),
                  "elapsed_seconds":record.get("elapsed_seconds")}))
