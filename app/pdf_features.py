"""Safe static feature extraction for PDFShield AI.

This extractor is designed to produce the same 31 feature names
used by the PDFMalware2022 training dataset.

Safety:
- PDF files are read as bytes and parsed as documents.
- Embedded JavaScript is never executed.
- Embedded files are never extracted or executed.
- No shell commands are executed against the PDF.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict

from pypdf import PdfReader


# ============================================================
# Helper
# ============================================================

def _count(raw: bytes, token: str | bytes) -> int:
    """Count occurrences of a PDF token without executing anything."""
    if isinstance(token, str):
        token = token.encode("latin-1")

    return len(
        re.findall(
            re.escape(token),
            raw,
            flags=re.IGNORECASE,
        )
    )


def _count_keyword(raw: bytes, keyword: str) -> int:
    """Count PDF names such as /JS or /OpenAction."""
    return _count(raw, f"/{keyword}")


def _header(raw: bytes) -> str:
    """Return the PDF header, e.g. %PDF-1.7."""
    match = re.search(
        rb"%PDF-\d+\.\d+",
        raw[:1024],
    )

    if match:
        return match.group(0).decode(
            "latin-1",
            errors="replace",
        )

    return "Unknown"


def _xref_length(raw: bytes) -> int:
    """Estimate the classic xref table entry count.

    Example:
        xref
        0 11

    gives an xref length of 11.

    If no classic xref subsection can be detected, return 0.
    """

    total = 0

    # Match classic PDF xref subsections:
    #
    # xref
    # 0 11
    #
    # or:
    #
    # xref
    # 0 1
    # 12 4
    pattern = re.compile(
        rb"\bxref\b\s+((?:\d+\s+\d+\s*)+)",
        flags=re.IGNORECASE,
    )

    match = pattern.search(raw)

    if not match:
        return 0

    numbers = re.findall(
        rb"\d+",
        match.group(1),
    )

    values = [int(x) for x in numbers]

    # Values occur as start,count pairs.
    for i in range(0, len(values) - 1, 2):
        total += values[i + 1]

    return total


def _page_number_tokens(raw: bytes) -> int:
    """Count /Page tokens while excluding /Pages."""
    return len(
        re.findall(
            rb"/Page\b",
            raw,
            flags=re.IGNORECASE,
        )
    )


def _metadata_size(reader: PdfReader) -> int:
    """Approximate metadata size using the serialized metadata."""
    try:
        metadata = reader.metadata or {}

        if not metadata:
            return 0

        return len(
            str(metadata).encode("utf-8")
        )

    except Exception:
        return 0


def _title_characters(reader: PdfReader) -> int:
    """Return the number of characters in PDF title metadata."""
    try:
        metadata = reader.metadata or {}

        title = metadata.get("/Title", "")

        if title is None:
            return 0

        return len(str(title))

    except Exception:
        return 0


def _image_count(reader: PdfReader) -> int:
    """Count image XObjects without executing content."""
    count = 0

    try:
        for page in reader.pages:
            try:
                resources = page.get("/Resources")

                if not resources:
                    continue

                resources = resources.get_object()

                xobjects = resources.get("/XObject")

                if not xobjects:
                    continue

                xobjects = xobjects.get_object()

                for obj in xobjects.values():
                    try:
                        obj = obj.get_object()

                        if obj.get("/Subtype") == "/Image":
                            count += 1

                    except Exception:
                        continue

            except Exception:
                continue

    except Exception:
        pass

    return count


def _text_present(reader: PdfReader) -> str:
    """Return Yes/No depending on whether text can be extracted."""
    try:
        for page in reader.pages:
            try:
                text = page.extract_text() or ""

                if text.strip():
                    return "Yes"

            except Exception:
                continue

    except Exception:
        pass

    return "No"


def _page_count(reader: PdfReader) -> int:
    try:
        return len(reader.pages)
    except Exception:
        return 0


def _encrypted(reader: PdfReader) -> str:
    try:
        return "1" if reader.is_encrypted else "0"
    except Exception:
        return "0"


# ============================================================
# Main extractor
# ============================================================

def extract_features(
    file_path: str | Path,
) -> Dict[str, Any]:
    """Extract the 31 PDFMalware2022 model features."""

    path = Path(file_path)

    raw = path.read_bytes()

    try:
        reader = PdfReader(
            str(path),
            strict=False,
        )
    except Exception:
        reader = None

    # --------------------------------------------------------
    # Basic PDF properties
    # --------------------------------------------------------

    if reader is not None:
        pages = _page_count(reader)
        metadata_size = _metadata_size(reader)
        title_characters = _title_characters(reader)
        encrypted = _encrypted(reader)
        images = _image_count(reader)
        text = _text_present(reader)
    else:
        pages = 0
        metadata_size = 0
        title_characters = 0
        encrypted = "0"
        images = 0
        text = "No"

    # --------------------------------------------------------
    # Structural features
    # --------------------------------------------------------

    obj = _count(raw, b"obj")
    endobj = _count(raw, b"endobj")
    stream = _count(raw, b"stream")
    endstream = _count(raw, b"endstream")

    xref = _count_keyword(raw, "xref")
    trailer = _count_keyword(raw, "trailer")
    startxref = _count_keyword(raw, "startxref")

    page_no = _page_number_tokens(raw)

    encrypt = _count_keyword(raw, "Encrypt")
    objstm = _count_keyword(raw, "ObjStm")

    js = _count_keyword(raw, "JS")
    javascript = _count_keyword(raw, "JavaScript")

    aa = _count_keyword(raw, "AA")
    open_action = _count_keyword(raw, "OpenAction")

    acroform = _count_keyword(raw, "AcroForm")
    jbig2 = _count_keyword(raw, "JBIG2Decode")

    rich_media = _count_keyword(raw, "RichMedia")
    launch = _count_keyword(raw, "Launch")
    embedded_file = _count_keyword(raw, "EmbeddedFile")

    xfa = _count_keyword(raw, "XFA")

    # Colors is represented by the /Colors PDF keyword.
    colors = _count_keyword(raw, "Colors")

    embedded_files = embedded_file

    # --------------------------------------------------------
    # Dataset-compatible categorical values
    # --------------------------------------------------------

    # The original dataset stores several structural columns
    # as categorical values even when their contents look numeric.
    #
    # We therefore return those values as strings.

    features: Dict[str, Any] = {
        "PdfSize": len(raw) / 1000.0,
        "MetadataSize": float(metadata_size),
        "Pages": float(pages),
        "XrefLength": float(_xref_length(raw)),
        "TitleCharacters": float(title_characters),

        "isEncrypted": str(encrypted),
        "EmbeddedFiles": float(embedded_files),

        "Images": str(images),
        "Text": str(text),

        "Header": _header(raw),

        "Obj": str(obj),
        "Endobj": str(endobj),
        "Stream": float(stream),
        "Endstream": str(endstream),

        "Xref": str(xref),
        "Trailer": float(trailer),
        "StartXref": str(startxref),
        "PageNo": str(page_no),

        "Encrypt": float(encrypt),
        "ObjStm": float(objstm),

        "JS": str(js),
        "Javascript": str(javascript),
        "AA": str(aa),
        "OpenAction": str(open_action),
        "Acroform": str(acroform),
        "JBIG2Decode": str(jbig2),
        "RichMedia": str(rich_media),
        "Launch": str(launch),
        "EmbeddedFile": str(embedded_file),
        "XFA": str(xfa),

        "Colors": float(colors),
    }

    return features