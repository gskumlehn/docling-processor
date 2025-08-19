import os
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions


def process_file(input_path: str, output_path: str, ocr: bool = False):
    """
    Processa um único arquivo PDF com Docling e gera um JSON de saída.

    Args:
        input_path (str): Caminho do arquivo PDF de entrada
        output_path (str): Caminho do arquivo JSON de saída
        ocr (bool): Se True, ativa OCR no pipeline
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    pdf_opts = PdfPipelineOptions()
    pdf_opts.do_ocr = ocr

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_opts)}
    )

    results = converter.convert_all([input_path], raises_on_error=False)
    for res in results:
        res.document.save_as_json(output_path)
