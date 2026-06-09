"""Turn an iCloud shortcut link (or an unsigned .shortcut/.plist file) into a
human-readable XML plist on disk. Network fetch is isolated in fetch_unsigned_plist
so the pure transforms stay unit-testable."""
import plistlib
import re
import sys
import urllib.request
from pathlib import Path

_ID_RE = re.compile(r"^https?://(?:www\.)?icloud\.com/shortcuts/([A-Za-z0-9]+)/?$")


def extract_shortcut_id(share_url):
    m = _ID_RE.match(share_url.strip())
    if not m:
        raise ValueError(f"Not an iCloud shortcut link: {share_url!r}")
    return m.group(1)


def icloud_record_url(share_url):
    return f"https://www.icloud.com/shortcuts/api/records/{extract_shortcut_id(share_url)}"


def plist_to_xml(src_path, dest_path):
    """Read any plist (binary or XML) and write it back as XML1."""
    with open(src_path, "rb") as fh:
        doc = plistlib.load(fh)
    with open(dest_path, "wb") as fh:
        plistlib.dump(doc, fh)  # plistlib defaults to XML format
    return dest_path


def fetch_unsigned_plist(share_url, dest_path):  # pragma: no cover - network
    """Fetch the unsigned shortcut bytes for an iCloud link and write XML to dest.
    NOTE: confirm the JSON key path against docs/decompile-validation.md for iOS 27."""
    import json
    rec_url = icloud_record_url(share_url)
    with urllib.request.urlopen(rec_url, timeout=30) as resp:
        record = json.load(resp)
    download_url = record["fields"]["shortcut"]["value"]["downloadURL"]
    with urllib.request.urlopen(download_url, timeout=30) as resp:
        raw = resp.read()
    doc = plistlib.loads(raw)
    with open(dest_path, "wb") as fh:
        plistlib.dump(doc, fh)
    return dest_path


if __name__ == "__main__":
    src, dest = sys.argv[1], sys.argv[2]
    if src.startswith("http"):
        fetch_unsigned_plist(src, dest)
    else:
        plist_to_xml(src, dest)
    print(f"wrote {dest}")
