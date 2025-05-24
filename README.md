# YouTube コメント分析サイト

YouTube動画のコメントを分析し、感情分析と頻出キーワードを可視化するWebアプリケーションです。

## 機能

- YouTube動画URLからコメントを自動取得（最大100件）
- 日本語コメントの感情分析（ポジティブ/ニュートラル/ネガティブ）
- 頻出キーワードの抽出と可視化
- レスポンシブデザイン（PC・スマートフォン対応）

## 技術スタック

### バックエンド
- **Python 3.9+**
- **FastAPI** - 高速なWeb API フレームワーク
- **janome** - 日本語形態素解析
- **oseti** - 日本語感情極性辞書
- **httpx** - 非同期HTTPクライアント

### フロントエンド
- **React 18+**
- **TypeScript** - 型安全な開発
- **Chart.js** - グラフ描画ライブラリ
- **CSS3** - レスポンシブデザイン

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/Be114/youtube_komebunseki.git
cd youtube_komebunseki
```

### 2. YouTube Data API v3 キーの取得

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成または既存のプロジェクトを選択
3. YouTube Data API v3 を有効にする
4. 認証情報でAPIキーを作成
5. APIキーに適切な制限を設定（HTTPリファラーまたはIPアドレス制限推奨）

### 3. 環境変数の設定

```bash
cp .env.example .env
```

`.env`ファイルを編集して、YouTube APIキーを設定：

```
YOUTUBE_API_KEY=your_actual_api_key_here
REACT_APP_API_URL=http://localhost:8000
```

### 4. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 依存関係のインストール
pip install -r requirements.txt

# サーバー起動
python main.py
```

バックエンドサーバーが `http://localhost:8000` で起動します。

### 5. フロントエンドのセットアップ

新しいターミナルで：

```bash
cd frontend

# 依存関係のインストール
npm install

# 開発サーバー起動
npm start
```

フロントエンドが `http://localhost:3000` で起動します。

## 使用方法

1. ブラウザで `http://localhost:3000` にアクセス
2. YouTube動画のURLを入力フォームに貼り付け
3. 「コメントを分析」ボタンをクリック
4. 分析結果が表示されるまで待機（数秒〜数十秒）
5. 感情分析の円グラフとキーワードクラウドで結果を確認

### 対応するURL形式

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## API仕様

### POST /api/analyze

YouTube動画のコメント分析を実行

**リクエスト:**
```json
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**レスポンス:**
```json
{
  "sentiment": {
    "positive": 45,
    "neutral": 35,
    "negative": 20
  },
  "keywords": [
    {"word": "面白い", "count": 25},
    {"word": "最高", "count": 18}
  ],
  "total_comments": 100
}
```

## 開発

### バックエンドの開発

```bash
cd backend

# 開発サーバー起動（リロード有効）
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### フロントエンドの開発

```bash
cd frontend

# 開発サーバー起動
npm start

# TypeScriptの型チェック
npm run type-check

# ESLintによるコード品質チェック
npm run lint
```

### 開発前のチェック

開発を始める前に、以下のコマンドで型チェックとリントを実行することを推奨します：

```bash
# フロントエンドの型チェックとリント
cd frontend
npm run check-all

# 型チェックのみ
npm run type-check

# リントのみ
npm run lint

# リントの自動修正
npm run lint:fix
```

### よくある開発エラーと対処法

**「'React' is declared but its value is never read」エラー**
- React 17以降では、JSX使用時にReactのインポートは不要です
- このプロジェクトはReact 18を使用しているため、Reactの明示的なインポートは削除されています

**未使用のインポートエラー**
- TypeScriptのnoUnusedLocalsとnoUnusedParameters設定により検出されます
- `npm run lint:fix`で自動的に削除できます

### テスト

```bash
# バックエンドテスト
cd backend
python -m pytest

# フロントエンドテスト
cd frontend
npm test
```

## 制約・注意事項

- YouTube Data API v3の利用制限があります（1日あたり10,000クォータ）
- コメント取得は最大100件に制限されています（MVP版）
- 日本語コメントの分析に特化しています
- APIキーは環境変数で管理し、公開リポジトリにコミットしないでください
- 本番環境では`ALLOWED_ORIGINS`と`DEBUG`の設定を適切に変更してください

## デプロイメント準備

### 本番環境向けの設定

1. **環境変数の設定**
   ```bash
   # .envファイル（本番用）
   YOUTUBE_API_KEY=your_production_api_key
   ALLOWED_ORIGINS=https://yourdomain.com
   REACT_APP_API_URL=https://api.yourdomain.com
   DEBUG=False
   ```

2. **HTTPS対応**
   - フロントエンド・バックエンドともにHTTPS化を推奨
   - Let's Encryptなどで証明書を取得

3. **APIキーの制限**
   - Google Cloud ConsoleでAPIキーにHTTPリファラー制限を設定
   - 本番ドメインのみ許可するよう設定

## トラブルシューティング

### よくある問題

1. **「YouTube APIの利用制限に達しました」エラー**
   - API利用制限（クォータ）を超過しています
   - 翌日まで待つか、Google Cloud Consoleでクォータを確認してください

2. **「動画が見つかりません」エラー**
   - 無効なURLまたは非公開動画の可能性があります
   - 公開されているYouTube動画のURLを確認してください

3. **「サーバーに接続できません」エラー**
   - バックエンドサーバーが起動しているか確認してください
   - ポート8000が他のプロセスで使用されていないか確認してください

## ライセンス

MIT License

## 作成者

[Be114](https://github.com/Be114)

## 貢献

プルリクエストやIssueの作成を歓迎します。