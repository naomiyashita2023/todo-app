# 🌸 やることリスト（Todoアプリ）

Python（Flask）で作った、シンプルでかわいいTodoリストのWebアプリです。
データは **Googleスプレッドシート** に保存されます。

## ✨ できること

- やることを **登録** する（タイトル・内容・期日）
- やることを **編集** する
- やることを **削除** する
- やることを **一覧** で見る（期日が近い順に並びます）
- 期日まで **あと何日か** を色分けして表示

| 期日の様子 | 表示の色 |
|---|---|
| まだ先 | 水色 |
| 3日以内・今日まで | 黄色 |
| すぎている | ピンク |

## 🧩 しくみ

```
📱💻 ブラウザ
      ↓
🏠 Flaskアプリ（Renderで公開）
      ↓ サービスアカウントのカギで読み書き
📒 Googleスプレッドシート
```

## 🛠️ 使っているもの

| 道具 | 役わり |
|---|---|
| [Flask](https://flask.palletsprojects.com/) | Webアプリの骨組み |
| [gspread](https://docs.gspread.org/) | Googleスプレッドシートとやりとりする |
| [gunicorn](https://gunicorn.org/) | サーバーでFlaskを動かす |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | `.env` の設定を読みこむ |
| [Render](https://render.com/) | アプリを公開するサーバー（無料プラン） |

## 📁 ファイルの説明

```
.
├── app.py              … アプリの頭脳（ページの動き・スプレッドシートとのやりとり）
├── templates/
│   ├── base.html       … 全ページ共通のデザイン
│   ├── index.html      … 一覧ページ
│   └── form.html       … 登録・編集ページ
├── requirements.txt    … 使っている道具のリスト
└── .env.example        … 設定ファイルのお手本
```

## 🚀 自分のパソコンで動かす方法

### 1. Googleの準備
1. [Google Cloud](https://console.cloud.google.com) でプロジェクトを作り、**Google Sheets API** を有効にする
2. **サービスアカウント** を作り、**JSON形式のキー** をダウンロードする
3. ダウンロードしたファイルの名前を `credentials.json` にして、このフォルダに置く
4. Googleスプレッドシートを新しく作り、サービスアカウントのメールアドレスに **編集者** として共有する

### 2. 設定ファイルを作る
`.env.example` をコピーして `.env` という名前にし、スプレッドシートのIDを書きます。

```
SPREADSHEET_ID=ここにスプレッドシートのID
```

スプレッドシートのIDは、URLの `/d/` と `/edit` のあいだの文字です。

### 3. 動かす
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python app.py
```

ブラウザで http://127.0.0.1:5000 を開きます。

## 🌍 Renderで公開する方法

Renderで **Web Service** を作り、次のように設定します。

| 項目 | 設定 |
|---|---|
| Language | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Instance Type | Free |

**Environment Variables**（環境変数）に、次の2つを入れます。

| Key | Value |
|---|---|
| `SPREADSHEET_ID` | スプレッドシートのID |
| `GOOGLE_CREDENTIALS_JSON` | `credentials.json` の中身ぜんぶ |

## ⚠️ 注意

- `credentials.json`（カギ）と `.env` は **ひみつのファイル** です。GitHubにはアップロードされないように `.gitignore` で設定しています。
- このアプリにはログイン機能がありません。URLを知っている人はだれでも見たり書きかえたりできます。
