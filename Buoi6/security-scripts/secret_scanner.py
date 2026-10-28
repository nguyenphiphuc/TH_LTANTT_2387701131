import os
import re
import sys

PATTERNS = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Generic Private Key": re.compile(r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----"),
    "Hardcoded Password": re.compile(r"(?i)(password|secret|passwd|api_key)\s*[:=]\s*['\"][A-Za-z0-9!@#$%^&*()_+=-]{6,}['\"]"),
    "Slack Token": re.compile(r"xox[baprs]-[0-9]{10,12}-[0-9]{10,12}-[a-zA-Z0-9]{24,32}"),
    "GitHub Token": re.compile(r"gh[pous]_[A-Za-z0-9_]{36,255}")
}

EXCLUDE_DIRS = {".git", "node_modules", "build", "dist", ".docusaurus", "__pycache__"}

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f, start=1):
                for rule_name, regex in PATTERNS.items():
                    if regex.search(line):
                        findings.append({
                            "file": filepath,
                            "line": idx,
                            "rule": rule_name,
                            "snippet": line.strip()[:80]
                        })
    except Exception as e:
        pass
    return findings

def scan_directory(target_dir):
    all_findings = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            path = os.path.join(root, f)
            all_findings.extend(scan_file(path))
    return all_findings

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"[*] DevSecOps Secret Scanner: Scanning '{target}'...")
    findings = scan_directory(target)
    if not findings:
        print("[+] PASS: Khong phat hien khoa bi mat hoac token bi ro ri.")
        sys.exit(0)
    else:
        print(f"[-] FAIL: Phat hien {len(findings)} nguy co ro ri thong tin bi mat!")
        for item in findings:
            print(f"    - [Line {item['line']}] {item['file']}: {item['rule']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
