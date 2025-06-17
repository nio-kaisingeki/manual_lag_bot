# manual_rag_bot

`manual_rag_bot` は社内マニュアルをアップロードして検索・回答に活用する簡易RAG (Retrieval Augmented Generation) アプリケーションです。PDF から抽出したテキストを ChromaDB に登録し、質問時には関連する文書を参照して OpenAI モデルにコンテキストとして渡します。

## 主な機能
- **PDFアップロード**: `/pdf_upload/` で PDF をアップロードすると、内容が `Document` モデルに保存され、ChromaDB コレクションに追加されます。
- **チャットインターフェース**: `/chat/` では非同期チャット、トップページでは同期チャットが利用できます。入力された質問に対し、保存済み文書を検索して得たテキストをコンテキストに含めて回答を生成します。

## セットアップ
1. Python 3.12 をインストールしてください。
2. OpenAI API キーを環境変数 `OPENAI_API_KEY` で設定するか、`.env` ファイルに
   `OPENAI_API_KEY=...` と記述します。ChromaDB への接続先を変更したい場合は
   `CHROMA_HOST` と `CHROMA_PORT` を指定してください (デフォルトは
   `chromadb:8000`)。
3. 依存パッケージをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
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
- `http://localhost:8000/` にアクセスするとチャット画面が表示されます。
- `http://localhost:8000/pdf_upload/` で PDF をアップロードすると、内容が検索対象に追加されます。
- `http://localhost:8000/chat/` は非同期チャット用のエンドポイントです。

## テスト
Django のテストランナーを利用できます。
```bash
python manage.py test
```

## ライセンス
このリポジトリは学習目的のサンプルであり、特別なライセンスは付与されていません。
