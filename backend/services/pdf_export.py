import io

from PyPDF2 import PdfReader, PdfWriter

_WEASYPRINT_ERROR = None
try:
    from weasyprint import HTML
except (ImportError, OSError) as exc:
    HTML = None
    _WEASYPRINT_ERROR = exc

def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    if HTML is None:
        raise RuntimeError(
            "WeasyPrint is unavailable. On Windows, install the GTK/Pango "
            "runtime and ensure its bin directory is on PATH."
        ) from _WEASYPRINT_ERROR
    if not html_docs:
        raise ValueError("At least one HTML document is required to generate a PDF.")

    writer = PdfWriter()
    for html_str in html_docs.values():
        pdf_bytes = HTML(string=html_str).write_pdf()
        if pdf_bytes is None:
            raise RuntimeError("WeasyPrint did not return PDF data.")
        writer.append(PdfReader(io.BytesIO(pdf_bytes)))

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()