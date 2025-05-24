from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Dict
import re
import logging
import os

from api.youtube import YouTubeClient
from analyzer.sentiment import SentimentAnalyzer
from analyzer.keywords import KeywordExtractor

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="YouTube Comment Analyzer",
    description="YouTube動画のコメントを分析し、感情分析と頻出キーワードを提供するAPI",
    version="1.0.0"
)

# CORS設定
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエスト・レスポンスモデル
class AnalyzeRequest(BaseModel):
    video_url: HttpUrl

class KeywordItem(BaseModel):
    word: str
    count: int

class SentimentData(BaseModel):
    positive: int
    neutral: int
    negative: int

class AnalyzeResponse(BaseModel):
    sentiment: SentimentData
    keywords: List[KeywordItem]
    total_comments: int

# 初期化
youtube_client = YouTubeClient()
sentiment_analyzer = SentimentAnalyzer()
keyword_extractor = KeywordExtractor()

def extract_video_id(url: str) -> str:
    """YouTube URLから動画IDを抽出"""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)'
    ]
    
    url_str = str(url).strip()
    
    for pattern in patterns:
        match = re.search(pattern, url_str)
        if match:
            video_id = match.group(1)
            # 動画IDの長さチェック（YouTubeの動画IDは通常11文字）
            if len(video_id) >= 10 and len(video_id) <= 12:
                return video_id
    
    raise ValueError("無効なYouTube URLです。正しい形式: https://www.youtube.com/watch?v=VIDEO_ID")

@app.get("/")
async def root():
    """ヘルスチェック用エンドポイント"""
    return {"message": "YouTube Comment Analyzer API"}

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_comments(request: AnalyzeRequest):
    """
    YouTube動画のコメントを分析して感情分析と頻出キーワードを返す
    """
    try:
        # YouTube URLから動画IDを抽出
        video_id = extract_video_id(str(request.video_url))
        logger.info(f"動画ID抽出完了: {video_id}")
        
        # YouTube APIからコメント取得
        comments = await youtube_client.get_comments(video_id)
        logger.info(f"コメント取得完了: {len(comments)}件")
        
        if not comments:
            raise HTTPException(status_code=404, detail="コメントが見つかりませんでした")
        
        # 感情分析
        sentiment_result = sentiment_analyzer.analyze_batch(comments)
        logger.info(f"感情分析完了: {sentiment_result}")
        
        # キーワード抽出
        keywords = keyword_extractor.extract_keywords(comments, top_n=20)
        logger.info(f"キーワード抽出完了: {len(keywords)}件")
        
        # レスポンス作成
        response = AnalyzeResponse(
            sentiment=SentimentData(
                positive=sentiment_result['positive'],
                neutral=sentiment_result['neutral'],
                negative=sentiment_result['negative']
            ),
            keywords=[
                KeywordItem(word=word, count=count)
                for word, count in keywords
            ],
            total_comments=len(comments)
        )
        
        return response
        
    except ValueError as e:
        logger.error(f"URL解析エラー: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"分析エラー: {e}")
        raise HTTPException(status_code=500, detail="分析処理中にエラーが発生しました")

if __name__ == "__main__":
    import uvicorn
    
    # 環境変数からポート番号を取得
    port = int(os.getenv("BACKEND_PORT", "8000"))
    
    # デバッグモードの設定
    debug_mode = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        reload=debug_mode
    )