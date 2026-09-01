#!/usr/bin/env python3
import datetime
import json
import os
import re
import sys
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "161seconds")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


def fetch_days():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(URL, headers=headers, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        cells = soup.find_all("td", attrs={"data-date": True})
    if not cells:
        print("[ERR] No calendar cells found -- github markup may have changed", file=sys.stderr)
        sys.exit(1)

    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        td_id = td.get("id", "")
        tooltip_el = soup.find("tool-tip", attrs={"for": td_id}) if td_id else None
        text = tooltip_el.get_text(strip=True) if tooltip_el else ""
        
        if re.search(r"no contributions", text, re.I):
            count = 0
        else:
            m = re.match(r"(\d+)", text)
            count = int(m.group(1)) if m else (1 if int(td.get("data-level", 0)) > 0 else 0)
        days.append({"date": date, "count": count})

    # Deduplicate and sort chronologically by date
    unique_days = {}
    for d in days:
        unique_days[d["date"]] = d["count"]
    
    sorted_days = [{"date": k, "count": v} for k, v in sorted(unique_days.items())]
    return sorted_days


def compute_stats(days):
    total = sum(d["count"] for d in days)
    best_day = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}

    # Longest streak & Current streak
    longest = 0
    cur_streak = 0
    temp_streak = 0
    for d in days:
        if d["count"] > 0:
            temp_streak += 1
            if temp_streak > longest:
                longest = temp_streak
        else:
            temp_streak = 0

    for d in reversed(days):
        if d["count"] > 0:
            cur_streak += 1
        else:
            if cur_streak == 0:
                continue
            break

    daily_avg = round(total / max(len(days), 1), 2)

    return {
        "username": USERNAME,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total": total,
        "daily_avg": daily_avg,
        "current_streak": cur_streak,
        "longest_streak": longest,
        "best_day": best_day,
        "days": days
    }


def main():
    days = fetch_days()
    stats = compute_stats(days)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"[OK] Fetched {len(days)} days. Total: {stats['total']}, Current Streak: {stats['current_streak']}, Longest: {stats['longest_streak']}")


if __name__ == "__main__":
    main()
