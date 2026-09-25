# Release index maintenance

After an approved article is public and its live page has been checked, add a verified record to `releases.json` and run `python scripts/build_release_readme.py` from the repository root. The script updates the article links in the root README and the corresponding weekly README. It checks that the article URL uses `ericmacdougall.com`, the public readback has a valid timestamp, and the companion folder exists.

Do not enter a planned article or an unverified social/YouTube URL as a release. The script edits local files; it does not deploy the site or publish to GitHub.
