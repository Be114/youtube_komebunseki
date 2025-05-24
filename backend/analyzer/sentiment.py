from typing import List, Dict
import logging

try:
    import oseti
except ImportError:
    oseti = None

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """日本語テキストの感情分析を行うクラス"""
    
    def __init__(self):
        """感情分析器の初期化"""
        if oseti is None:
            logger.warning("osetiライブラリが見つかりません。簡易な感情分析を使用します。")
            self.analyzer = None
        else:
            try:
                self.analyzer = oseti.Analyzer()
                logger.info("oseti感情分析器を初期化しました")
            except Exception as e:
                logger.error(f"oseti初期化エラー: {e}")
                self.analyzer = None
    
    def analyze_text(self, text: str) -> str:
        """
        単一テキストの感情分析
        
        Args:
            text: 分析対象のテキスト
            
        Returns:
            感情ラベル ('positive', 'neutral', 'negative')
        """
        if self.analyzer:
            try:
                scores = self.analyzer.analyze(text)
                
                # osetiは複数の感情スコアを返すので、合計で判定
                total_score = sum(scores)
                
                if total_score > 0.1:
                    return 'positive'
                elif total_score < -0.1:
                    return 'negative'
                else:
                    return 'neutral'
                    
            except Exception as e:
                logger.error(f"感情分析エラー: {e}")
                return self._simple_sentiment_analysis(text)
        else:
            return self._simple_sentiment_analysis(text)
    
    def analyze_batch(self, texts: List[str]) -> Dict[str, int]:
        """
        複数テキストの感情分析
        
        Args:
            texts: 分析対象のテキストリスト
            
        Returns:
            感情別の件数辞書
        """
        sentiment_counts = {
            'positive': 0,
            'neutral': 0,
            'negative': 0
        }
        
        for text in texts:
            sentiment = self.analyze_text(text)
            sentiment_counts[sentiment] += 1
        
        logger.info(f"感情分析結果: {sentiment_counts}")
        return sentiment_counts
    
    def _simple_sentiment_analysis(self, text: str) -> str:
        """
        簡易的な感情分析（osetiが利用できない場合）
        感情表現キーワードに基づく分類
        """
        # ポジティブキーワード
        positive_words = [
            '素晴らしい', '最高', '面白い', 'いいね', '良い', 'よい', 'よかった',
            'ありがとう', '感動', '楽しい', '嬉しい', 'すごい', 'かっこいい',
            'きれい', '美しい', '感謝', '好き', '愛', '幸せ', '喜び'
        ]
        
        # ネガティブキーワード
        negative_words = [
            'つまらない', '嫌い', 'ひどい', '最悪', '悪い', 'だめ', 'ダメ',
            '残念', '微妙', '納得いかない', '腹立つ', '怒', '悲しい',
            '失望', 'がっかり', '不満', '問題', '困る'
        ]
        
        # 日本語は大文字小文字の区別がないため、元のテキストを使用
        text_lower = text
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'