# YouTube コメント分析サイト開発ガイドライン

## プロジェクト概要
YouTube動画のコメントを分析し、感情分析と頻出キーワードを可視化するWebアプリケーション

## 技術スタック
- **バックエンド**: Python 3.9+ / FastAPI
- **フロントエンド**: React 18+ / TypeScript
- **分析ライブラリ**: 
  - 形態素解析: janome
  - 感情分析: oseti（日本語感情極性辞書）
- **可視化**: Chart.js, react-wordcloud
- **API**: YouTube Data API v3

## コーディング規約

### Python (バックエンド)
- **PEP 8** に準拠
- 型ヒントを必須とする
- 関数・クラスには適切なdocstringを記述
- 非同期処理には `async/await` を使用
- エラーハンドリングを適切に実装

### TypeScript/React (フロントエンド)
- **厳密な型指定**を行う
- Functional Componentを使用
- React Hooksを活用
- CSSはモジュール形式またはstyled-componentsを使用
- propsには適切な型定義を行う

### 共通規約
- **日本語コメント**を使用（コード説明時）
- 変数・関数名は英語で記述
- コミットメッセージは日本語で記述
- APIレスポンスはJSONで統一

## ディレクトリ構造
```
youtube-comment-analyzer/
├── backend/
│   ├── main.py                 # FastAPIアプリケーション
│   ├── api/
│   │   ├── __init__.py
│   │   └── youtube.py          # YouTube API連携
│   ├── analyzer/
│   │   ├── __init__.py
│   │   ├── sentiment.py        # 感情分析
│   │   └── keywords.py         # キーワード抽出
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── InputForm.tsx    # URL入力フォーム
│   │   │   ├── SentimentChart.tsx # 感情分析グラフ
│   │   │   └── WordCloud.tsx    # ワードクラウド
│   │   └── api/
│   │       └── client.ts        # API通信
│   ├── package.json
│   └── tsconfig.json
├── .env.example
├── README.md
└── CLAUDE.md
```

## API設計

### エンドポイント
- `POST /api/analyze`
  - リクエスト: `{ "video_url": "https://youtube.com/watch?v=..." }`
  - レスポンス:
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

## セキュリティガイドライン
- APIキーは必ず環境変数で管理
- YouTube API呼び出し回数制限に注意
- エラー情報は適切に隠蔽
- CORS設定を適切に行う

## 開発フロー
1. 機能実装前にissueで仕様確認
2. ブランチ作成 (`feature/機能名`)
3. 実装・テスト
4. プルリクエスト作成
5. レビュー後マージ

## パフォーマンス指針
- YouTube API呼び出しは最大100件に制限（MVP版）
- レスポンシブデザインでモバイル対応
- ローディング状態の適切な表示
- エラーハンドリングの充実

## テスト方針
- バックエンド: pytest使用
- フロントエンド: Jest + React Testing Library
- 外部API依存部分はモック化

## デプロイメント
- バックエンド: uvicorn使用
- フロントエンド: npm run build
- 環境変数の適切な設定確認

## 制約事項
- 日本語コメントに特化（MVP版）
- 外部APIへの過度な依存を避ける
- シンプルで理解しやすいコード重視