import os
from flask import Flask, request, send_file
from docx import Document

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 測試首頁
@app.route("/")
def home():
    return "✅ Flask Word 合併 API 已啟動！"

# 合併 DOCX 檔案
def merge_docs(files, output_path):
    merged_doc = Document()
    for index, file in enumerate(files):
        doc = Document(file)
        for para in doc.paragraphs:
            merged_doc.add_paragraph(para.text)
        if index != len(files) - 1:
            merged_doc.add_page_break()  # 插入分頁符號
    merged_doc.save(output_path)

# API 端點: 接收檔案並合併
@app.route("/upload", methods=["POST"])
def upload_files():
    files = request.files.getlist("files")
    if not files:
        return "❌ 未收到檔案", 400

    file_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        file_paths.append(file_path)

    output_path = os.path.join(OUTPUT_FOLDER, "merged_document.docx")
    merge_docs(file_paths, output_path)
    
    return send_file(output_path, as_attachment=True)

# 啟動 Flask 應用
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # 讓 Render 自動設定 Port
    print(f"🚀 Flask 伺服器啟動中，監聽 PORT: {port}")
    app.run(host="0.0.0.0", port=port)
