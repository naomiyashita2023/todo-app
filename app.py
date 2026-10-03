"""
Todoリストアプリ（データは Google スプレッドシートに保存）

スプレッドシートの1行目は見出しで、こうなっています:
    A列: id   B列: タイトル   C列: 内容   D列: 期日
"""
import json
import os
import uuid

import gspread
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

# .env ファイルに書いた設定を読みこむ
load_dotenv()

app = Flask(__name__)

HEADER = ["id", "タイトル", "内容", "期日"]


def get_sheet():
    """Googleスプレッドシートの1枚目のシートを取り出す"""
    # サーバー(Render)では環境変数に鍵の中身を入れる。パソコンでは credentials.json を使う
    creds_text = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if creds_text:
        client = gspread.service_account_from_dict(json.loads(creds_text))
    else:
        client = gspread.service_account(filename="credentials.json")

    sheet = client.open_by_key(os.environ["SPREADSHEET_ID"]).sheet1

    # 見出しがなければ自動で書く
    if sheet.row_values(1) != HEADER:
        sheet.update(range_name="A1:D1", values=[HEADER])
    return sheet


def find_row(sheet, todo_id):
    """idを見て、そのやることが何行目にあるか探す（見つからなければ None）"""
    ids = sheet.col_values(1)
    for row_number, value in enumerate(ids, start=1):
        if row_number > 1 and value == todo_id:
            return row_number
    return None


# ---------- ページ ----------

@app.route("/")
def index():
    """一覧ページ"""
    records = get_sheet().get_all_values()[1:]  # 1行目(見出し)はとばす
    todos = [
        {"id": r[0], "title": r[1], "content": r[2], "due": r[3]}
        for r in records
        if r and r[0]
    ]
    todos.sort(key=lambda t: t["due"] or "9999-99-99")  # 期日が近い順
    return render_template("index.html", todos=todos)


@app.route("/new", methods=["GET", "POST"])
def new():
    """登録ページ"""
    if request.method == "POST":
        get_sheet().append_row(
            [
                uuid.uuid4().hex[:8],
                request.form["title"],
                request.form["content"],
                request.form["due"],
            ],
            value_input_option="RAW",
        )
        return redirect(url_for("index"))
    return render_template("form.html", todo=None)


@app.route("/edit/<todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    """編集ページ"""
    sheet = get_sheet()
    row = find_row(sheet, todo_id)
    if row is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        sheet.update(
            range_name=f"B{row}:D{row}",
            values=[[request.form["title"], request.form["content"], request.form["due"]]],
            value_input_option="RAW",
        )
        return redirect(url_for("index"))

    r = sheet.row_values(row) + ["", "", "", ""]
    todo = {"id": r[0], "title": r[1], "content": r[2], "due": r[3]}
    return render_template("form.html", todo=todo)


@app.route("/delete/<todo_id>", methods=["POST"])
def delete(todo_id):
    """削除"""
    sheet = get_sheet()
    row = find_row(sheet, todo_id)
    if row:
        sheet.delete_rows(row)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
