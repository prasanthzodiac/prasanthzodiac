import os
import sys
import json
import re
import datetime
import urllib.request
from html.parser import HTMLParser

USERNAME = os.environ.get("GH_PROFILE_USER", "prasanthzodiac")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")

class ContribParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []
        self.tooltips = {}
        self.current_td_id = None
        self.current_tooltip_for = None
        self.tooltip_text = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "td" and "data-date" in attr_dict:
            date = attr_dict.get("data-date")
            level = int(attr_dict.get("data-level", 0))
            td_id = attr_dict.get("id")
            self.days.append({"date": date, "level": level, "id": td_id, "count": 0})
        elif tag == "tool-tip" and "for" in attr_dict:
            self.current_tooltip_for = attr_dict.get("for")
            self.tooltip_text = ""

    def handle_data(self, data):
        if self.current_tooltip_for:
            self.tooltip_text += data

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.current_tooltip_for:
            self.tooltips[self.current_tooltip_for] = self.tooltip_text.strip()
            self.current_tooltip_for = None

def fetch_days():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode('utf-8')

    parser = ContribParser()
    parser.feed(html)

    for d in parser.days:
        td_id = d.get("id")
        text = parser.tooltips.get(td_id, "")
        if "no contribution" in text.lower() or not text:
            d["count"] = 0
        else:
            m = re.search(r"(\d+)\s+contribution", text)
            if m:
                d["count"] = int(m.group(1))
            else:
                d["count"] = d["level"] if d["level"] > 0 else 0
        d.pop("id", None)

    parser.days.sort(key=lambda x: x["date"])
    return parser.days

def compute_current_streak(days):
    idx = len(days) - 1
    if idx >= 0 and days[idx]["count"] == 0:
        idx -= 1
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]

def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end

def build_data(days):
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]} if days else {},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly_list,
        "days": days,
    }

if __name__ == "__main__":
    days = fetch_days()
    data = build_data(days)
    out_dir = os.path.dirname(os.path.abspath(OUT_PATH))
    os.makedirs(out_dir, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {OUT_PATH}: {data['total_contributions']} contributions, active {data['active_days']} days, streak {data['current_streak']['length']}.")
