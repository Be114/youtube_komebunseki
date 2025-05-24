"""エラーメッセージとレスポンスメッセージの定義"""

class Messages:
    # エラーメッセージ
    INVALID_URL = "無効なYouTube URLです。正しい形式: https://www.youtube.com/watch?v=VIDEO_ID"
    VIDEO_NOT_FOUND = "指定された動画が見つかりません"
    API_LIMIT_EXCEEDED = "YouTube APIの利用制限に達しました"
    COMMENTS_NOT_FOUND = "コメントが見つかりませんでした"
    ANALYSIS_ERROR = "分析処理中にエラーが発生しました"
    
    # 成功メッセージ
    EXTRACTION_COMPLETE = "動画ID抽出完了: {}"
    COMMENTS_RETRIEVED = "コメント取得完了: {}件"
    SENTIMENT_COMPLETE = "感情分析完了: {}"
    KEYWORDS_COMPLETE = "キーワード抽出完了: {}件"