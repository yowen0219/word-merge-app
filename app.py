import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # ✅ 確保 CORS 可用
from docx import Document

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ 允許所有來源訪問 API

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "✅ Flask Word 合併 API 已啟動！"})

@app.route("/upload", methods=["POST"])
def upload_files():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "❌ 未收到檔案"}), 400

    file_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        file_paths.append(file_path)

    output_path = os.path.join(OUTPUT_FOLDER, "merged_document.docx")
    merge_docs(file_paths, output_path)

    response = send_file(output_path, as_attachment=True)
    response.headers["Access-Control-Allow-Origin"] = "*"  # ✅ 明確允許 CORS
    return response

def merge_docs(files, output_path):
    merged_doc = Document()
    for index, file in enumerate(files):
        doc = Document(file)
        for para in doc.paragraphs:
            merged_doc.add_paragraph(para.text)
        if index != len(files) - 1:
            merged_doc.add_page_break()
    merged_doc.save(output_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # ✅ Render 會自動設定 Port
    print(f"🚀 Flask 伺服器啟動中，監聽 PORT: {port}")
    app.run(host="0.0.0.0", port=port)
