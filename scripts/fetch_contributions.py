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
    days = []

    # Find day elements: GitHub uses td.ContributionCalendar-day or td[data-date]
    day_elements = soup.find_all("td", class_="ContributionCalendar-day")
    if not day_elements:
        day_elements = soup.find_all("td", attrs={"data-date": True})

    total_contributions = 0
    longest_streak = 0
    temp_streak = 0
    best_day = {"date": "", "count": 0}

    for td in day_elements:
        date = td.get("data-date")
        if not date:
            continue
        level = int(td.get("data-level", 0))

        td_id = td.get("id", "")
        count = 0
        tooltip = soup.find("tool-tip", attrs={"for": td_id}) if td_id else None

        if tooltip and tooltip.text:
            match = re.search(r"(\d+)\s+contribution", tooltip.text)
            if match:
                count = int(match.group(1))
            elif "No contribution" in tooltip.text:
                count = 0
        else:
            count = 1 if level > 0 else 0

        total_contributions += count

        if count > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

        if count > best_day["count"]:
            best_day = {"date": date, "count": count}

        days.append({
            "date": date,
            "count": count,
            "level": level
        })

    # Calculate current streak
    current_streak = 0
    for day in reversed(days):
        if day["count"] > 0:
            current_streak += 1
        else:
            if current_streak == 0:
                continue
            break

    # Look for exact total in header text if present
    header_text = soup.find("h2", class_="f4 text-normal mb-2")
    if not header_text:
        header_text = soup.find(string=re.compile(r"contributions in the last year", re.I))
    if header_text:
        text_val = header_text.text if hasattr(header_text, 'text') else str(header_text)
        match = re.search(r"([\d,]+)\s+contributions", text_val)
        if match:
            total_contributions = int(match.group(1).replace(",", ""))

    data = {
        "username": USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[OK] Fetched {len(days)} days. Total contributions: {total_contributions}, Current streak: {current_streak}, Longest: {longest_streak}")

if __name__ == "__main__":
    fetch_contributions()
