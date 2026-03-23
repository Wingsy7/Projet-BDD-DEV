from pathlib import Path
import textwrap


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_PATH = BASE_DIR / "livrables" / "explication_projet.txt"
OUTPUT_PATH = BASE_DIR / "livrables" / "explication_projet.pdf"

PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT_MARGIN = 50
TOP_MARGIN = 60
BOTTOM_MARGIN = 60
FONT_SIZE = 11
LINE_HEIGHT = 15
WRAP_WIDTH = 88


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def normalize_lines(text: str) -> list[str]:
    wrapped_lines: list[str] = []
    for raw_line in text.splitlines():
        stripped = raw_line.rstrip()
        if not stripped:
            wrapped_lines.append("")
            continue
        if stripped.startswith("- "):
            prefix = "- "
            body = stripped[2:]
            wrapped = textwrap.wrap(
                body,
                width=WRAP_WIDTH - len(prefix),
                subsequent_indent="  ",
            )
            if not wrapped:
                wrapped_lines.append(prefix)
                continue
            wrapped_lines.append(prefix + wrapped[0])
            wrapped_lines.extend(wrapped[1:])
            continue
        wrapped = textwrap.wrap(stripped, width=WRAP_WIDTH)
        wrapped_lines.extend(wrapped or [""])
    return wrapped_lines


def paginate(lines: list[str]) -> list[list[str]]:
    usable_height = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    lines_per_page = usable_height // LINE_HEIGHT
    pages: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if len(current) >= lines_per_page:
            pages.append(current)
            current = []
        current.append(line)
    if current:
        pages.append(current)
    return pages


def build_content_stream(page_lines: list[str]) -> bytes:
    start_y = PAGE_HEIGHT - TOP_MARGIN
    parts = ["BT", f"/F1 {FONT_SIZE} Tf", f"{LEFT_MARGIN} {start_y} Td"]

    first_line = True
    for line in page_lines:
        if not first_line:
            parts.append(f"0 -{LINE_HEIGHT} Td")
        safe_line = pdf_escape(line)
        parts.append(f"({safe_line}) Tj")
        first_line = False

    parts.append("ET")
    return "\n".join(parts).encode("latin-1", errors="replace")


def build_pdf(pages: list[list[str]]) -> bytes:
    objects: list[bytes] = []

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")

    page_count = len(pages)
    first_page_object = 3
    kids = " ".join(f"{first_page_object + index * 2} 0 R" for index in range(page_count))
    objects.append(f"<< /Type /Pages /Count {page_count} /Kids [{kids}] >>".encode("ascii"))

    font_object_number = first_page_object + page_count * 2

    for index, page_lines in enumerate(pages):
        page_object_number = first_page_object + index * 2
        content_object_number = page_object_number + 1

        page_object = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_object_number} 0 R >> >> "
            f"/Contents {content_object_number} 0 R >>"
        ).encode("ascii")
        objects.append(page_object)

        stream = build_content_stream(page_lines)
        content_object = (
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"\nendstream"
        )
        objects.append(content_object)

    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]

    for object_number, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{object_number} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF"
        ).encode("ascii")
    )
    return bytes(pdf)


def main() -> None:
    source_text = SOURCE_PATH.read_text(encoding="utf-8")
    normalized_lines = normalize_lines(source_text)
    pages = paginate(normalized_lines)
    pdf_bytes = build_pdf(pages)
    OUTPUT_PATH.write_bytes(pdf_bytes)
    print(f"PDF cree : {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
