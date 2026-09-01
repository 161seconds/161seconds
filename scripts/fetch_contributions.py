import os
import json
import re
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

USERNAME = os.getenv("GITHUB_USERNAME", "161seconds")
URL = f"https://github.com/users/{USERNAME}/contributions"

def fetch_contributions():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(URL, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch contributions: HTTP {resp.status_code}")

    soup = BeautifulSoup(resp.text, "html.parser")
    
    # 1. Parse month headers from thead
    month_labels = []
    thead = soup.find("thead")
    if thead:
        th_tds = thead.find_all("td", class_="ContributionCalendar-label")
        current_col = 0
        for td in th_tds:
            # text contains "September\nSep" or similar
            raw_text = td.text.strip().split()
            month_short = raw_text[-1] if raw_text else ""
            colspan = int(td.get("colspan", 1))
            if month_short:
                month_labels.append({
                    "month": month_short,
                    "col": current_col
                })
            current_col += colspan

    # 2. Parse 2D calendar table from tbody
    tbody = soup.find("tbody")
    if not tbody:
        raise RuntimeError("Could not find tbody in contribution calendar")

    tr_rows = tbody.find_all("tr") # Exactly 7 rows: Row 0=Sun, 1=Mon, ..., 6=Sat
    
    cells = []
    days_by_date = {}

    for day_of_week, tr in enumerate(tr_rows):
        tds = tr.find_all("td", class_="ContributionCalendar-day")
        for week_idx, td in enumerate(tds):
            date = td.get("data-date")
            if not date:
                continue
            level = int(td.get("data-level", 0))
            td_id = td.get("id", "")
            count = 0
            
            tooltip = soup.find("tool-tip", attrs={"for": td_id}) if td_id else None
            if tooltip and tooltip.text:
                m = re.search(r"(\d+)\s+contribution", tooltip.text)
                if m:
                    count = int(m.group(1))
            else:
                count = 1 if level > 0 else 0

            cell_info = {
                "date": date,
                "col": week_idx,
                "row": day_of_week,
                "level": level,
                "count": count
            }
            cells.append(cell_info)
            days_by_date[date] = cell_info

    # Sort all days chronologically by date
    sorted_dates = sorted(days_by_date.keys())
    
    total_contributions = 0
    longest_streak = 0
    temp_streak = 0
    best_day = {"date": "", "count": 0}

    for d in sorted_dates:
        cnt = days_by_date[d]["count"]
        total_contributions += cnt
        if cnt > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

        if cnt > best_day["count"]:
            best_day = {"date": d, "count": cnt}

    # Calculate current streak backwards from today
    current_streak = 0
    for d in reversed(sorted_dates):
        cnt = days_by_date[d]["count"]
        if cnt > 0:
            current_streak += 1
        else:
            if current_streak == 0:
                continue
            break

    # Check header text for exact yearly total count
    header_text = soup.find("h2", class_="f4 text-normal mb-2")
    if header_text:
        m = re.search(r"([\d,]+)\s+contributions", header_text.text)
        if m:
            total_contributions = int(m.group(1).replace(",", ""))

    data = {
        "username": USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "month_labels": month_labels,
        "cells": cells
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[OK] Fetched {len(cells)} cells across {len(sorted_dates)} dates.")
    print(f"[OK] Total: {total_contributions}, Current streak: {current_streak}, Longest streak: {longest_streak}")

if __name__ == "__main__":
    fetch_contributions()
