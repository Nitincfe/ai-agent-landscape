"""
Build a dataset from ashishpatel26/500-AI-Agents-Projects.
 
Step 1 (extract): parse the README tables -> projects.csv
Step 2 (enrich):  add stars/forks/dates from the GitHub API -> projects_enriched.csv
 
Usage:
    pip install requests pandas
    python agents_dataset.py extract
    export GITHUB_TOKEN=ghp_xxx      # optional but recommended (60 -> 5000 requests/hour)
    python agents_dataset.py enrich
"""
import os
import re
import sys
import time
 
import pandas as pd
import requests
 
README_URL = (
    "https://raw.githubusercontent.com/ashishpatel26/500-AI-Agents-Projects/main/README.md"
)
RAW_CSV = "projects.csv"
ENRICHED_CSV = "projects_enriched.csv"
 
 
# ---------- Step 1: extract ----------
 
def extract():
    text = requests.get(README_URL, timeout=30).text
    rows = []
    section = None       # "Industry" or a framework name
    in_industry = False
 
    for line in text.splitlines():
        # Track which section of the README we are in
        if line.startswith("## ") and "Industry Use Cases" in line:
            section, in_industry = "Industry", True
            continue
        if line.startswith("## ") and "Browse by Framework" in line:
            in_industry = False
            continue
        if line.startswith("### "):
            section = line[4:].strip()   # CrewAI, AutoGen, Agno, LangGraph
            in_industry = False
            continue
        if line.startswith("## ") and section:
            # Any other H2 (Contributing, License...) ends the data sections
            if "Industry Use Cases" not in line and "Browse by Framework" not in line:
                section, in_industry = None, False
            continue
 
        if section is None or not line.startswith("|"):
            continue
 
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # Skip header and separator rows
        if len(cells) < 4 or cells[0] == "Use Case" or set(cells[0]) <= set("-: "):
            continue
 
        name = re.sub(r"\*\*", "", cells[0]).strip()
        name = re.sub(r"^[^\w(]+", "", name).strip()   # drop leading emoji
        link = re.search(r"\]\((https?://[^)]+)\)\s*$", cells[3])
        rows.append(
            {
                "name": name,
                "section": section,
                "framework": "Standalone" if section == "Industry" else section,
                "industry": cells[1],
                "description": cells[2],
                "url": link.group(1) if link else "",
            }
        )
 
    df = pd.DataFrame(rows)
    df.to_csv(RAW_CSV, index=False)
    print(f"Wrote {len(df)} rows to {RAW_CSV}")
    print(df.groupby("framework").size())
 
 
# ---------- Step 2: enrich ----------
 
def parse_repo(url):
    """Return (owner, repo, is_subpath) for github.com URLs, else None."""
    m = re.match(r"https?://github\.com/([^/]+)/([^/#?]+)(/.*)?", url)
    if not m:
        return None
    owner, repo, rest = m.group(1), m.group(2), m.group(3) or ""
    repo = re.sub(r"\.git$", "", repo)
    return owner, repo, bool(rest.strip("/"))
 
 
def fetch_repo(owner, repo, session):
    r = session.get(f"https://api.github.com/repos/{owner}/{repo}", timeout=30)
    if r.status_code == 403 and r.headers.get("X-RateLimit-Remaining") == "0":
        reset = int(r.headers.get("X-RateLimit-Reset", time.time() + 60))
        wait = max(reset - int(time.time()), 1) + 2
        print(f"Rate limited. Sleeping {wait}s (set GITHUB_TOKEN to avoid this)...")
        time.sleep(wait)
        return fetch_repo(owner, repo, session)
    if r.status_code != 200:
        return {"status": r.status_code}
    d = r.json()
    return {
        "status": 200,
        "stars": d["stargazers_count"],
        "forks": d["forks_count"],
        "created_at": d["created_at"][:10],
        "pushed_at": d["pushed_at"][:10],
        "archived": d["archived"],
        "language": d["language"],
        "repo_description": d["description"],
    }
 
 
def enrich():
    df = pd.read_csv(RAW_CSV).fillna("")
    session = requests.Session()
    session.headers["Accept"] = "application/vnd.github+json"
    token = os.getenv("GITHUB_TOKEN")
    if token:
        session.headers["Authorization"] = f"Bearer {token}"
 
    cache, out = {}, []
    for _, row in df.iterrows():
        parsed = parse_repo(row["url"])
        info = {"owner": "", "repo": "", "points_to_subfolder": False, "status": "not_github"}
        if parsed:
            owner, repo, sub = parsed
            key = (owner.lower(), repo.lower())
            if key not in cache:
                cache[key] = fetch_repo(owner, repo, session)
                time.sleep(0.2)
            info = {"owner": owner, "repo": repo, "points_to_subfolder": sub, **cache[key]}
        out.append({**row.to_dict(), **info})
 
    res = pd.DataFrame(out)
    res["pushed_at"] = pd.to_datetime(res.get("pushed_at"), errors="coerce")
    cutoff = pd.Timestamp.now() - pd.DateOffset(months=6)
    res["active_last_6mo"] = res["pushed_at"] >= cutoff
    res.to_csv(ENRICHED_CSV, index=False)
    print(f"Wrote {len(res)} rows to {ENRICHED_CSV}")
    print(res["status"].value_counts())
 
 
if __name__ == "__main__":
    # No argument (e.g. VS Code's Run button) -> run extract by default
    cmd = sys.argv[1] if len(sys.argv) > 1 else "extract"
    {"extract": extract, "enrich": enrich}.get(cmd, lambda: print(__doc__))()
 