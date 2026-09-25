"""Write the README's weekly links from verified release records.

This does not publish an article or assert that a URL is live. Add a record to
releases.json only after checking the public article and that week's examples.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- RELEASES_START -->"
END = "<!-- RELEASES_END -->"
ARTICLE_START = "<!-- ARTICLE_START -->"
ARTICLE_END = "<!-- ARTICLE_END -->"


def between(text: str, start: str, end: str, replacement: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if len(pattern.findall(text)) != 1:
        raise ValueError(f"Expected one {start} ... {end} block")
    return pattern.sub(lambda _: f"{start}\n{replacement}\n{end}", text)


def validated_records() -> list[dict]:
    records = json.loads((ROOT / "releases.json").read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("releases.json must contain a list")
    weeks = set()
    for row in records:
        week = row["week"]
        if not isinstance(week, int) or week < 1 or week in weeks:
            raise ValueError(f"Invalid or duplicate week: {week}")
        weeks.add(week)
        date.fromisoformat(row["released_at_pt"])
        verified_at = datetime.fromisoformat(row["article_public_verified_at"].replace("Z", "+00:00"))
        if verified_at.tzinfo is None or verified_at > datetime.now(timezone.utc):
            raise ValueError(f"Missing or future public readback: week {week}")
        url = urlparse(row["article_url"])
        if url.scheme != "https" or url.hostname != "ericmacdougall.com" or not url.path.startswith("/journal/"):
            raise ValueError(f"Unexpected article URL: week {week}")
        if not (ROOT / "weeks" / f"{week:02d}" / "README.md").is_file():
            raise ValueError(f"Missing companion folder: week {week}")
        if not row["title"].strip() or not row["added"].strip():
            raise ValueError(f"Missing release copy: week {week}")
    return sorted(records, key=lambda row: row["week"], reverse=True)


def main() -> None:
    records = validated_records()
    readme = ROOT / "README.md"
    body = readme.read_text(encoding="utf-8")
    entries = [
        f"- **{row['released_at_pt']} · Week {row['week']:02d}: "
        f"[{row['title']}]({row['article_url']})** — "
        f"[{row['added']}](weeks/{row['week']:02d}/README.md)"
        for row in records
    ]
    body = between(body, START, END, "\n".join(entries) if entries else "No journal article has a verified public readback yet. Approved Week 01 and Week 02 companion materials are available below.")
    readme.write_text(body, encoding="utf-8")
    for row in records:
        path = ROOT / "weeks" / f"{row['week']:02d}" / "README.md"
        content = path.read_text(encoding="utf-8")
        article = f"**Article:** [{row['title']}]({row['article_url']}) · released {row['released_at_pt']} Pacific time."
        path.write_text(between(content, ARTICLE_START, ARTICLE_END, article), encoding="utf-8")
    print(f"Updated root README and {len(records)} released week folders")


if __name__ == "__main__":
    main()
