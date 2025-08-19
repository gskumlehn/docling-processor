import json
from io import BytesIO
from typing import Optional

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat, DocumentStream, ConversionStatus
from docling.datamodel.pipeline_options import PdfPipelineOptions


def process_bytes(pdf_bytes: bytes, ocr: bool = False, filename: Optional[str] = None) -> bytes:
    """
    Converte um PDF em memória (bytes) para JSON (bytes) usando Docling.
    Não persiste nada em disco.

    :param pdf_bytes: conteúdo do PDF em bytes
    :param ocr: habilita OCR no pipeline
    :param filename: nome lógico do arquivo (usado só para metadados)
    :return: JSON serializado em bytes (UTF-8)
    :raises RuntimeError: quando a conversão falhar
    """
    pdf_opts = PdfPipelineOptions()
    pdf_opts.do_ocr = ocr

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_opts)}
    )

    source = DocumentStream(name=filename or "upload.pdf", stream=BytesIO(pdf_bytes))
    result = converter.convert(source)

    if result.status != ConversionStatus.SUCCESS:
        errs = "; ".join(getattr(e, "error_message", str(e)) for e in (result.errors or []))
        raise RuntimeError(f"Falha na conversão ({result.status}). {errs}")

    data = result.document.export_to_dict()
    return json.dumps(data, ensure_ascii=False).encode("utf-8")
