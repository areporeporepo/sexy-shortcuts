import plistlib
from pathlib import Path

import pytest

from scripts.decompile import icloud_record_url, plist_to_xml, extract_shortcut_id

FIX = Path(__file__).parent / "fixtures"


def test_extract_shortcut_id_from_share_url():
    url = "https://www.icloud.com/shortcuts/abc123DEF456"
    assert extract_shortcut_id(url) == "abc123DEF456"


def test_extract_shortcut_id_with_trailing_slash():
    url = "https://www.icloud.com/shortcuts/abc123/"
    assert extract_shortcut_id(url) == "abc123"


def test_extract_shortcut_id_rejects_non_icloud():
    with pytest.raises(ValueError):
        extract_shortcut_id("https://example.com/foo")


def test_icloud_record_url():
    url = "https://www.icloud.com/shortcuts/abc123"
    assert icloud_record_url(url) == "https://www.icloud.com/shortcuts/api/records/abc123"


def test_plist_to_xml_roundtrips(tmp_path):
    out = tmp_path / "out.xml"
    plist_to_xml(FIX / "green_text.plist", out)
    text = out.read_text()
    assert "WFWorkflowActions" in text
    assert text.lstrip().startswith("<?xml")
    with open(out, "rb") as fh:
        doc = plistlib.load(fh)
    assert "WFWorkflowActions" in doc
