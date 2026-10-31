#!/usr/bin/env python3
"""Pulls REAL GitHub numbers for one or more users and writes data.json.
Env: GH_TOKEN (token), GH_USERS (comma separated usernames, e.g. "nibrasnaourasdaboul,dana-username"),
     HIDE_LANGS (optional, e.g. "HTML,CSS")."""
import os, json, math, datetime as dt, urllib.request
Q = """query($login:String!){user(login:$login){followers{totalCount}
repositories(ownerAffiliations:OWNER,isFork:false,first:100){totalCount nodes{stargazerCount
languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
contributionsCollection{totalCommitContributions totalPullRequestContributions totalIssueContributions
contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
RANKS = ["C", "B", "A", "AA", "AAA", "S", "SS", "SSS"]
RCOL = ["#64748b", "#94a3b8", "#22d3ee", "#34d399", "#a78bfa", "#f472b6", "#fb923c", "#fbbf24"]
TH = {"Commits": [1, 50, 150, 300, 500, 800, 1200, 2000], "Stars": [1, 10, 30, 75, 150, 300, 600, 1000],
      "Followers": [1, 10, 30, 75, 150, 300, 600, 1000], "Repos": [1, 5, 10, 20, 35, 50, 80, 120],
      "PRs": [1, 10, 25, 50, 100, 200, 400, 800], "Streak": [1, 3, 7, 14, 30, 60, 100, 200]}

def gql(login, token):
    req = urllib.request.Request("https://api.github.com/graphql",
        json.dumps({"query": Q, "variables": {"login": login}}).encode(),
        {"Authorization": "bearer " + token, "Content-Type": "application/json", "User-Agent": "stats-bot"})
    r = json.load(urllib.request.urlopen(req, timeout=30))
    if r.get("errors") or not r["data"]["user"]: raise SystemExit("GitHub API error for %s: %s" % (login, r.get("errors")))
    return r["data"]["user"]

def rank(name, v):
    i = max(sum(v >= t for t in TH[name]) - 1, 0)
    return RANKS[i], RCOL[i]

def build(users, hide=()):
    cc = [u["contributionsCollection"] for u in users]
    stars = sum(n["stargazerCount"] for u in users for n in u["repositories"]["nodes"])
    repos = sum(u["repositories"]["totalCount"] for u in users)
    fol = sum(u["followers"]["totalCount"] for u in users)
    com = sum(c["totalCommitContributions"] for c in cc); prs = sum(c["totalPullRequestContributions"] for c in cc)
    iss = sum(c["totalIssueContributions"] for c in cc)
    days = {}
    for c in cc:
        for w in c["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]: days[d["date"]] = days.get(d["date"], 0) + d["contributionCount"]
    series = [v for _, v in sorted(days.items())]
    best = run = 0
    for v in series:
        run = run + 1 if v > 0 else 0; best = max(best, run)
    langs = {}
    for u in users:
        for n in u["repositories"]["nodes"]:
            for e in n["languages"]["edges"]:
                nm = e["node"]["name"]
                if nm in hide: continue
                o = langs.get(nm, [0, e["node"]["color"] or "#94a3b8"]); o[0] += e["size"]; langs[nm] = o
    tot = sum(v[0] for v in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    vals = [("Total Stars", stars, "#fbbf24"), ("Commits (1y)", com, "#a78bfa"), ("Pull Requests", prs, "#22d3ee"),
            ("Issues", iss, "#f472b6"), ("Repositories", repos, "#34d399")]
    mx = math.log1p(max(v for _, v, _ in vals)) or 1
    stats = [[l, f"{v:,}", round(math.log1p(v) / mx, 3), c] for l, v, c in vals]
    L = [[n, f"{v[0] * 100 / tot:.0f}%", round(v[0] / tot, 3), v[1]] for n, v in top]
    tro = [[n, *rank(n, v)] for n, v in (("Commits", com), ("Stars", stars), ("Followers", fol), ("Repos", repos), ("PRs", prs), ("Streak", best))]
    return {"stats": stats, "langs": L, "trophies": tro, "activity": series[-30:] or [0],
            "updated": dt.date.today().isoformat()}

if __name__ == "__main__":
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token: raise SystemExit("Set GH_TOKEN")
    names = [x.strip() for x in os.environ.get("GH_USERS", "").split(",") if x.strip()]
    if not names: raise SystemExit("Set GH_USERS")
    hide = [x.strip() for x in os.environ.get("HIDE_LANGS", "").split(",") if x.strip()]
    json.dump(build([gql(n, token) for n in names], hide), open("data.json", "w"), indent=1, ensure_ascii=False)
    print("data.json updated for", names)
