import os
import io
from flask import Flask, request, send_file, jsonify, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from main import process_bytes

ORIGIN = "https://brand-to-json-converter.lovable.app"

app = Flask(__name__)
CORS(
    app,
    resources={r"/process-file": {"origins": [ORIGIN]}},
    methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
    expose_headers=["Content-Disposition", "Content-Type"],
    supports_credentials=False,
    max_age=86400,
)

@app.route("/process-file", methods=["OPTIONS"])
def process_file_options():
    resp = make_response("", 204)
    resp.headers["Access-Control-Allow-Origin"] = ORIGIN
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
    resp.headers["Access-Control-Max-Age"] = "86400"
    return resp

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
    json_bytes = process_bytes(pdf_bytes, ocr=ocr, filename=filename)

    buf = io.BytesIO(json_bytes); buf.seek(0)

    resp = send_file(
        buf,
        mimetype="application/json",
        as_attachment=True,
        download_name=f"{base}.json",
        max_age=0,
        etag=False,
        last_modified=None,
        conditional=False,
    )
    resp.headers["Access-Control-Allow-Origin"] = ORIGIN
    resp.headers["Access-Control-Expose-Headers"] = "Content-Disposition, Content-Type"
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
