"""tests/test_metadata.py — Per-format metadata extraction.

Covers the image EXIF extractor and the dispatcher contract.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("PIL", reason="Pillow required for metadata tests")

from ftree_kg.metadata import (  # noqa: E402
    AUDIO_EXTS,
    IMAGE_EXTS,
    extract_image_metadata,
    extract_metadata,
    metadata_keywords,
    metadata_prose,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _write_jpeg_with_exif(
    path: Path,
    *,
    make: str = "TestMake",
    model: str = "TestModel",
    datetime_original: str = "2024:07:15 12:00:00",
    description: str | None = None,
    width: int = 32,
    height: int = 32,
    gps: tuple[float, float] | None = None,
) -> Path:
    """Mint a tiny JPEG with the requested EXIF tags. Returns *path*."""
    from PIL import Image
    from PIL.ExifTags import IFD, TAGS

    tag_id = {name: tid for tid, name in TAGS.items()}

    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    exif = img.getexif()
    if make:
        exif[tag_id["Make"]] = make
    if model:
        exif[tag_id["Model"]] = model
    if datetime_original:
        # Canonical EXIF DateTime tag (0x0132). DateTimeOriginal lives in the
        # Exif IFD (0x9003); we set both for breadth.
        exif[tag_id["DateTime"]] = datetime_original
        exif_ifd = exif.get_ifd(IFD.Exif)
        exif_ifd[tag_id["DateTimeOriginal"]] = datetime_original
    if description:
        exif[tag_id["ImageDescription"]] = description
    if gps is not None:
        # PIL writes GPS DMS as a 3-tuple of IFDRational values.
        from PIL.TiffImagePlugin import IFDRational

        lat, lon = gps
        gps_ifd = exif.get_ifd(IFD.GPSInfo)

        def _to_dms(deg: float) -> tuple[IFDRational, IFDRational, IFDRational]:
            d = int(abs(deg))
            m_full = (abs(deg) - d) * 60
            m = int(m_full)
            s = (m_full - m) * 60
            return (
                IFDRational(d, 1),
                IFDRational(m, 1),
                IFDRational(int(round(s * 1000)), 1000),
            )

        gps_ifd[1] = "N" if lat >= 0 else "S"  # GPSLatitudeRef
        gps_ifd[2] = _to_dms(lat)
        gps_ifd[3] = "E" if lon >= 0 else "W"  # GPSLongitudeRef
        gps_ifd[4] = _to_dms(lon)
    img.save(path, "JPEG", exif=exif)
    return path


@pytest.fixture
def jpeg_with_exif(tmp_path: Path) -> Path:
    return _write_jpeg_with_exif(
        tmp_path / "vacation.jpg",
        make="Apple",
        model="iPhone 14 Pro",
        datetime_original="2023:07:15 12:34:56",
        description="Beach at sunset",
        gps=(37.7749, -122.4194),  # San Francisco
    )


@pytest.fixture
def jpeg_no_exif(tmp_path: Path) -> Path:
    return _write_jpeg_with_exif(
        tmp_path / "plain.jpg",
        make="",
        model="",
        datetime_original="",
    )


# ---------------------------------------------------------------------------
# extract_image_metadata
# ---------------------------------------------------------------------------


def test_extract_image_metadata_returns_canonical_keys(jpeg_with_exif: Path) -> None:
    meta = extract_image_metadata(jpeg_with_exif)
    assert meta is not None
    assert meta["camera_make"] == "Apple"
    assert meta["camera_model"] == "iPhone 14 Pro"
    assert meta["taken_at"].startswith("2023:07:15")
    assert meta["description"] == "Beach at sunset"
    assert meta["dimensions"] == "32x32"


def test_extract_image_metadata_parses_gps(jpeg_with_exif: Path) -> None:
    meta = extract_image_metadata(jpeg_with_exif)
    assert meta is not None
    assert "gps" in meta
    lat = meta["gps"]["lat"]
    lon = meta["gps"]["lon"]
    # Within 0.01 degrees of San Francisco (rounding from DMS).
    assert abs(lat - 37.7749) < 0.01
    assert abs(lon - (-122.4194)) < 0.01


def test_extract_image_metadata_handles_no_exif(jpeg_no_exif: Path) -> None:
    """A JPEG with no meaningful EXIF still returns dimensions, no error."""
    meta = extract_image_metadata(jpeg_no_exif)
    assert meta is not None
    assert "dimensions" in meta
    # No camera fields present
    assert "camera_make" not in meta or meta.get("camera_make") in ("", None)


def test_extract_image_metadata_returns_none_for_nonimage(tmp_path: Path) -> None:
    txt = tmp_path / "not_an_image.txt"
    txt.write_text("hello")
    assert extract_image_metadata(txt) is None


def test_extract_image_metadata_returns_none_for_missing_file(tmp_path: Path) -> None:
    assert extract_image_metadata(tmp_path / "nope.jpg") is None


# ---------------------------------------------------------------------------
# extract_metadata dispatcher
# ---------------------------------------------------------------------------


def test_dispatcher_routes_image_to_image_extractor(jpeg_with_exif: Path) -> None:
    meta = extract_metadata(jpeg_with_exif)
    assert meta is not None
    assert meta["camera_make"] == "Apple"


def test_dispatcher_returns_none_for_unsupported_extension(tmp_path: Path) -> None:
    py = tmp_path / "module.py"
    py.write_text("print('hi')")
    assert extract_metadata(py) is None


def test_dispatcher_returns_none_for_directory(tmp_path: Path) -> None:
    sub = tmp_path / "sub"
    sub.mkdir()
    assert extract_metadata(sub) is None


def test_image_extension_set_includes_common_formats() -> None:
    for ext in (".jpg", ".jpeg", ".png", ".tiff", ".webp", ".heic"):
        assert ext in IMAGE_EXTS


def test_audio_extension_set_present_for_future_dispatch() -> None:
    # Stub support — currently dispatcher returns None for these.
    for ext in (".mp3", ".flac"):
        assert ext in AUDIO_EXTS


# ---------------------------------------------------------------------------
# metadata_keywords / metadata_prose projections
# ---------------------------------------------------------------------------


def test_metadata_keywords_includes_camera_year_and_gps() -> None:
    meta = {
        "camera_make": "Apple",
        "camera_model": "iPhone 14 Pro",
        "taken_at": "2023:07:15 12:34:56",
        "description": "Beach",
        "gps": {"lat": 37.7749, "lon": -122.4194},
    }
    tokens = metadata_keywords(meta)
    flat = " ".join(tokens)
    assert "apple" in flat
    assert "iphone 14 pro" in flat
    assert "2023" in flat
    assert "2023-07" in flat
    assert "beach" in flat
    assert any(t.startswith("gps:") for t in tokens)


def test_metadata_keywords_empty_for_none() -> None:
    assert metadata_keywords(None) == []
    assert metadata_keywords({}) == []


def test_metadata_prose_renders_lines() -> None:
    meta = {
        "dimensions": "100x100",
        "camera_make": "Apple",
        "taken_at": "2023:07:15 12:00:00",
    }
    prose = metadata_prose(meta)
    lines = prose.splitlines()
    assert lines[0] == "dimensions: 100x100"
    assert "camera_make: Apple" in prose
    assert "taken_at:" in prose


def test_metadata_prose_formats_gps_decimal() -> None:
    meta = {"gps": {"lat": 37.7749, "lon": -122.4194}}
    prose = metadata_prose(meta)
    assert "gps: 37.774900, -122.419400" in prose


def test_metadata_prose_empty_for_none() -> None:
    assert metadata_prose(None) == ""
    assert metadata_prose({}) == ""
