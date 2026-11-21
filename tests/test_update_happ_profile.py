"""Unit and integration checks for the published Happ artifacts."""

import base64
import json
import re
import shutil
from pathlib import Path

import pytest

from scripts import update_happ_profile as mod


@pytest.fixture
def project(tmp_path):
    source = Path(__file__).resolve().parents[1]
    (tmp_path / "happ").mkdir()
    shutil.copy2(source / mod.TEMPLATE, tmp_path / mod.TEMPLATE)
    (tmp_path / "README.md").write_text(
        "# Keep this heading\n\n"
        f"{mod.BEGIN}\n{mod.END}\n\nThis paragraph must survive.\n",
        encoding="utf-8",
    )
    return tmp_path


def test_four_timestamp_fields_and_canonical_base64():
    template = (mod.ROOT / mod.TEMPLATE).read_text(encoding="utf-8")
    ts = 1795181278
    profile = mod.render_profile(template, ts)
    assert profile["Geoipurl"].endswith(f"?v={ts}")
    assert profile["Geositeurl"].endswith(f"?v={ts}")
    assert profile["LastUpdated"] == str(ts)
    assert profile["lastUpdatedDate"] == str(ts)
    link = mod.create_deeplink(profile)
    encoded = link.removeprefix("happ://routing/add/")
    raw = base64.b64decode(encoded, validate=True).decode("utf-8")
    assert raw == json.dumps(profile, ensure_ascii=False, separators=(",", ":"))
    assert "\n" not in encoded


def test_generation_check_and_readme_preservation(project):
    mod.generate(project, 1795181278)
    mod.check(project)
    assert mod.main(["--check", "--root", str(project)]) == 0
    assert (project / mod.PROFILE).is_file()
    assert not (project / mod.LEGACY_PROFILE).exists()
    readme = (project / "README.md").read_text(encoding="utf-8")
    assert readme.startswith("# Keep this heading")
    assert readme.endswith("This paragraph must survive.\n")
    assert readme.count(mod.BEGIN) == 1
    assert "1795181278" in readme


@pytest.mark.parametrize("changed", [
    "Geoipurl", "Geositeurl", "LastUpdated", "lastUpdatedDate",
    "other-rule", "legacy-duplicate", "deeplink", "README",
])
def test_check_rejects_out_of_sync_artifacts(project, changed):
    mod.generate(project, 1795181278)
    if changed in {"Geoipurl", "Geositeurl", "LastUpdated", "lastUpdatedDate", "other-rule"}:
        path = project / mod.PROFILE
        obj = json.loads(path.read_text(encoding="utf-8"))
        key = changed if changed != "other-rule" else "RouteOrder"
        obj[key] = "unexpected"
        path.write_text(json.dumps(obj), encoding="utf-8")
    elif changed == "legacy-duplicate":
        path = project / mod.LEGACY_PROFILE
        path.write_text("{}", encoding="utf-8")
    elif changed == "deeplink":
        path = project / mod.DEEPLINK
        path.write_text("happ://routing/add/WRONG\n", encoding="utf-8")
    else:
        path = project / mod.README
        path.write_text(path.read_text(encoding="utf-8").replace("1795181278", "0000000000"), encoding="utf-8")
    with pytest.raises(mod.ProfileError):
        mod.check(project)
    assert mod.main(["--check", "--root", str(project)]) == 1


def test_template_requires_exactly_four_tokens():
    with pytest.raises(mod.ProfileError, match="four"):
        mod.render_profile('{"LastUpdated":"{TIMESTAMP}"}', 1234)


def test_cli_generation_and_check_uses_single_clock_value(project, monkeypatch):
    monkeypatch.setattr(mod.time, "time", lambda: 1795181278.9)
    assert mod.main(["--root", str(project)]) == 0
    assert mod.main(["--check", "--root", str(project)]) == 0
    assert re.fullmatch(r"happ://routing/add/[A-Za-z0-9+/]+=*\n", (project / mod.DEEPLINK).read_text())


def test_regeneration_removes_legacy_duplicate(project):
    (project / mod.LEGACY_PROFILE).write_text("{}", encoding="utf-8")
    mod.generate(project, 1795181278)
    assert not (project / mod.LEGACY_PROFILE).exists()
    mod.check(project)
