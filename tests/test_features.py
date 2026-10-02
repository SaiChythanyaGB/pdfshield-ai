from pathlib import Path

from app.pdf_features import extract_features


def test_extract_features(tmp_path: Path):
    p = tmp_path / "minimal.pdf"
    p.write_bytes(b"%PDF-1.7\n1 0 obj\n<<>>\nendobj\nstartxref\n0\n%%EOF")
    f = extract_features(p)
    assert f["pdf_ver"] == 1.7
    assert "JS" in f
    assert f["obj"] >= 1
