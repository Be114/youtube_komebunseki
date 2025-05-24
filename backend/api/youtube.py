import os
from typing import List, Optional
import httpx
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class YouTubeClient:
    """YouTube Data API v3を使用してコメントを取得するクライアント"""
    
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            logger.warning("YOUTUBE_API_KEYが設定されていません。環境変数を確認してください。")
        
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    async def get_comments(self, video_id: str, max_results: int = 100) -> List[str]:
        """
        指定されたYouTube動画のコメントを取得
        
        Args:
            video_id: YouTube動画ID
            max_results: 取得する最大コメント数（デフォルト: 100）
            
        Returns:
            コメントテキストのリスト
            
        Raises:
            HTTPException: APIキーが設定されていない場合や、API呼び出しに失敗した場合
        """
        if not self.api_key:
            logger.error("YOUTUBE_API_KEYが設定されていません")
            raise HTTPException(status_code=500, detail="YouTube APIキーが設定されていません。管理者に連絡してください。")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # 動画が存在するかチェック
                await self._check_video_exists(client, video_id)
                
                # コメントスレッド取得
                comments = await self._fetch_comment_threads(client, video_id, max_results)
                
                logger.info(f"取得完了: {len(comments)}件のコメント")
                return comments
                
        except httpx.HTTPStatusError as e:
            logger.error(f"YouTube API HTTPエラー: {e.response.status_code}")
            if e.response.status_code == 403:
                raise HTTPException(status_code=403, detail="YouTube APIの利用制限に達しました")
            elif e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="動画が見つかりません")
            else:
                raise HTTPException(status_code=500, detail="YouTube APIエラーが発生しました")
        except Exception as e:
            logger.error(f"コメント取得エラー: {e}")
            raise HTTPException(status_code=500, detail="コメントの取得に失敗しました")
    
    async def _check_video_exists(self, client: httpx.AsyncClient, video_id: str):
        """動画の存在確認"""
        url = f"{self.base_url}/videos"
        params = {
            'key': self.api_key,
            'id': video_id,
            'part': 'id'
        }
        
        response = await client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if not data.get('items'):
            raise HTTPException(status_code=404, detail="指定された動画が見つかりません")
    
    async def _fetch_comment_threads(self, client: httpx.AsyncClient, video_id: str, max_results: int) -> List[str]:
        """コメントスレッドを取得して平坦化"""
        url = f"{self.base_url}/commentThreads"
        params = {
            'key': self.api_key,
            'videoId': video_id,
            'part': 'snippet',
            'maxResults': min(max_results, 100),  # APIの制限
            'order': 'relevance'  # 関連度順
        }
        
        comments = []
        next_page_token = None
        
        while len(comments) < max_results:
            if next_page_token:
                params['pageToken'] = next_page_token
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # コメント抽出
            for item in data.get('items', []):
                comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment_text)
                
                if len(comments) >= max_results:
                    break
            
            # 次のページがあるかチェック
            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                break
        
        return comments[:max_results]
    
    def _get_dummy_comments(self) -> List[str]:
        """テスト用のダミーコメントデータ"""
        return [
            "とても面白い動画でした！",
            "最高の内容ですね",
            "素晴らしい説明ありがとうございます",
            "もう少し詳しく知りたいです",
            "参考になりました",
            "つまらない",
            "よくわからない",
            "いいね！",
            "また見たいです",
            "勉強になりました",
            "感動しました",
            "面白くない",
            "最高！",
            "ありがとうございます",
            "素晴らしい",
            "微妙ですね",
            "良い動画でした",
            "楽しかったです",
            "つまらなかった",
            "おもしろい！",
            "すごいですね",
            "よかった",
            "残念でした",
            "気に入りました",
            "納得いかない"
        ]
