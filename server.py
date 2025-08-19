import os
import tempfile
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from main import process_file

app = Flask(__name__)

@app.post("/process-file")
def process_single_file():
    if "file" not in request.files:
        return jsonify({"error": "arquivo não enviado"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "nome de arquivo vazio"}), 400

    ocr = str(request.form.get("ocr", "false")).lower() == "true"

    filename = secure_filename(file.filename)
    base, _ = os.path.splitext(filename)

    with tempfile.TemporaryDirectory() as tmpdir:
        in_path = os.path.join(tmpdir, filename)
        out_path = os.path.join(tmpdir, f"{base}.json")

        file.save(in_path)
        process_file(in_path, out_path, ocr=ocr)

        return send_file(
            out_path,
            mimetype="application/json",
            as_attachment=True,
            download_name=f"{base}.json",
            max_age=0,
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
