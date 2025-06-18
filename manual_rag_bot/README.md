# manual_rag_bot

`manual_rag_bot` は社内マニュアルをアップロードして検索・回答に活用する簡易RAG (Retrieval Augmented Generation) アプリケーションです。PDF から抽出したテキストを ChromaDB に登録し、質問時には関連する文書を参照して OpenAI モデルにコンテキストとして渡します。ユーザーごとにアップロードしたマニュアルを管理でき、他のユーザーの文書は参照されません。

## 主な機能
- **ユーザー登録・ログイン**
- **PDFアップロード**: `/pdf_upload/` で PDF をアップロードすると、内容が `Document` モデルに保存され、ユーザーごとの ChromaDB コレクションに追加されます。
- **チャットインターフェース**: `/chat/` では非同期チャット、トップページでは同期チャットが利用できます。アップロードした文書のみを参照して回答を生成します。
- **マニュアル管理**: `/documents/` で自分のアップロード済みマニュアルを一覧・削除できます。

## セットアップ
1. Python 3.12 をインストールしてください。
2. `.env.example` をコピーして `.env` を作成し、必要な環境変数を設定します。
   OpenAI API キーは `OPENAI_API_KEY` に指定してください。ChromaDB への接続先を
   変更したい場合は `CHROMA_HOST` と `CHROMA_PORT` を指定します (デフォルトは
   `chromadb:8000`)。
3. 依存パッケージをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
   `requirements.txt` では OpenAI クライアントと互換性のある
   `httpx==0.26.0` を指定しています。`httpx` 0.27 以降では
   `proxies` 引数が削除されているため、これより新しいバージョンを
   インストールすると起動時に `Client.__init__()` エラーが発生します。
4. マイグレーションを適用します。
   ```bash
   python manage.py migrate
   ```
5. ChromaDB を起動します。Docker を利用する場合は次のコマンドで Django と合わせて起動できます。Docker イメージは Python クライアントと互換性のある `chromadb/chroma:0.4.24` を使用します。
   本リポジトリでは OpenAI の埋め込み API を直接呼び出す実装に変更しているため、
   ChromaDB サーバー側のバージョン差異によるエラーは発生しません。
   ```bash
   docker-compose up --build
   ```
   もしくは `chromadb` サービスだけを起動してから `python manage.py runserver` で開発サーバーを起動してください。

## 使い方
- `http://localhost:8000/` にアクセスするとログイン画面が表示されます。登録後にチャットを利用できます。
- `http://localhost:8000/pdf_upload/` で PDF をアップロードすると、内容が自身の検索対象に追加されます。
- `http://localhost:8000/documents/` でアップロード済みマニュアルを一覧・削除できます。
- `http://localhost:8000/chat/` は非同期チャット用のエンドポイントです。

## テスト
Django のテストランナーを利用できます。
```bash
python manage.py test
```

## ライセンス
このリポジトリは学習目的のサンプルであり、特別なライセンスは付与されていません。
