# Draws a static dark contribution grid from the GitHub GraphQL API.
import json, os, sys, urllib.request
user = sys.argv[1]
q = '{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date weekday}}}}}}' % user
req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": q}).encode(),
                             {"Authorization": "bearer " + os.environ["GITHUB_TOKEN"]})
cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]  # github-dark palette
def level(n):  # ponytail: fixed buckets, switch to quartiles if counts get large
    return 0 if n == 0 else 1 if n < 3 else 2 if n < 6 else 3 if n < 10 else 4
S, G, L, T = 11, 3, 28, 22
weeks = cal["weeks"]
w, h = L + len(weeks) * (S + G), T + 7 * (S + G) + 20
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="ui-monospace,monospace" font-size="10">',
       f'<rect width="100%" height="100%" rx="6" fill="#0d1117"/>',
       f'<text x="{L}" y="14" fill="#c9d1d9">{cal["totalContributions"]} contributions in the last year</text>']
for i, d in enumerate(["Mon", "Wed", "Fri"]):
    out.append(f'<text x="2" y="{T + (2*i+1)*(S+G) + 9}" fill="#8b949e">{d}</text>')
for x, wk in enumerate(weeks):
    for d in wk["contributionDays"]:
        out.append(f'<rect x="{L + x*(S+G)}" y="{T + d["weekday"]*(S+G)}" width="{S}" height="{S}" rx="2" '
                   f'fill="{colors[level(d["contributionCount"])]}"><title>{d["contributionCount"]} on {d["date"]}</title></rect>')
out.append("</svg>")
os.makedirs("dist", exist_ok=True)
open("dist/grid-dark.svg", "w").write("\n".join(out))
