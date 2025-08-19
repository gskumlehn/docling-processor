import os
import io
import json
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from main import process_bytes  # deve retornar bytes, str ou dict do JSON

app = Flask(__name__)

@app.post("/process-file")
def process_single_file():
    if "file" not in request.files:
        return jsonify({"error": "arquivo não enviado"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "nome de arquivo vazio"}), 400

    ocr = str(request.form.get("ocr", "false")).lower() == "true"

    filename = secure_filename(file.filename)
    base, _ = os.path.splitext(filename)

    pdf_bytes = file.read()
    json_out = process_bytes(pdf_bytes, ocr=ocr)  # sem gravação em disco

    if isinstance(json_out, dict):
        json_bytes = json.dumps(json_out, ensure_ascii=False).encode("utf-8")
    elif isinstance(json_out, str):
        json_bytes = json_out.encode("utf-8")
    else:
        json_bytes = json_out  # já em bytes

    buf = io.BytesIO(json_bytes)
    buf.seek(0)

    return send_file(
        buf,
        mimetype="application/json",
        as_attachment=True,
        download_name=f"{base}.json",
        max_age=0,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
