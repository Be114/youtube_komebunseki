from typing import List, Tuple, Dict
from collections import Counter
import re
import logging

try:
    from janome.tokenizer import Tokenizer
except ImportError:
    Tokenizer = None

logger = logging.getLogger(__name__)

class KeywordExtractor:
    """日本語テキストからキーワードを抽出するクラス"""
    
    def __init__(self):
        """キーワード抽出器の初期化"""
        if Tokenizer is None:
            logger.warning("janomeライブラリが見つかりません。簡易な単語分割を使用します。")
            self.tokenizer = None
        else:
            try:
                self.tokenizer = Tokenizer()
                logger.info("janome形態素解析器を初期化しました")
            except Exception as e:
                logger.error(f"janome初期化エラー: {e}")
                self.tokenizer = None
        
        # 除外する品詞
        self.exclude_pos = {
            '助詞', '助動詞', '記号', '補助記号', 'フィラー'
        }
        
        # 除外する単語（ストップワード）
        self.stopwords = {
            'の', 'は', 'が', 'を', 'に', 'で', 'と', 'から', 'まで', 'より',
            'て', 'だ', 'である', 'です', 'ます', 'する', 'した', 'される',
            'これ', 'それ', 'あれ', 'この', 'その', 'あの', 'ここ', 'そこ', 'あそこ',
            'こと', 'もの', 'ため', 'とき', '時', '人', '方', 'さん', 'やつ',
            'やっぱり', 'やはり', 'でも', 'しかし', 'ただ', 'ちょっと', 'すごく',
            'とても', 'かなり', 'なんか', 'なんて', 'みたい', 'ような', 'という',
            'w', 'ww', 'www', '笑', 'lol', 'lmao'
        }
    
    def extract_keywords(self, texts: List[str], top_n: int = 20) -> List[Tuple[str, int]]:
        """
        テキストリストからキーワードを抽出
        
        Args:
            texts: 分析対象のテキストリスト
            top_n: 上位何件のキーワードを返すか
            
        Returns:
            (キーワード, 出現回数)のタプルリスト
        """
        all_words = []
        
        for text in texts:
            words = self._extract_words_from_text(text)
            all_words.extend(words)
        
        # 単語カウント
        word_counts = Counter(all_words)
        
        # 上位キーワード取得
        top_keywords = word_counts.most_common(top_n)
        
        logger.info(f"キーワード抽出完了: {len(top_keywords)}件")
        return top_keywords
    
    def _extract_words_from_text(self, text: str) -> List[str]:
        """単一テキストから意味のある単語を抽出"""
        if self.tokenizer:
            return self._extract_with_janome(text)
        else:
            return self._extract_simple(text)
    
    def _extract_with_janome(self, text: str) -> List[str]:
        """janomeを使用した形態素解析による単語抽出"""
        words = []
        
        try:
            for token in self.tokenizer.tokenize(text, wakati=False):
                # 品詞情報を取得
                pos = token.part_of_speech.split(',')[0]
                word = token.surface
                
                # フィルタリング条件
                if (len(word) >= 2 and  # 2文字以上
                    pos not in self.exclude_pos and  # 除外品詞でない
                    word not in self.stopwords and  # ストップワードでない
                    not word.isdigit() and  # 数字でない
                    self._is_meaningful_word(word)):  # 意味のある単語
                    
                    words.append(word)
                    
        except Exception as e:
            logger.error(f"形態素解析エラー: {e}")
            return self._extract_simple(text)
        
        return words
    
    def _extract_simple(self, text: str) -> List[str]:
        """簡易的な単語抽出（janomeが利用できない場合）"""
        # 基本的な前処理
        text = re.sub(r'[!-/:-@\\[-`{-~]', ' ', text)  # 記号除去
        text = re.sub(r'[0-9]+', '', text)  # 数字除去
        text = re.sub(r'\s+', ' ', text)  # 連続する空白を1つに
        
        # 空白で分割（簡易的）
        words = [word.strip() for word in text.split() if word.strip()]
        
        # フィルタリング
        filtered_words = []
        for word in words:
            if (len(word) >= 2 and 
                word not in self.stopwords and
                self._is_meaningful_word(word)):
                filtered_words.append(word)
        
        return filtered_words
    
    def _is_meaningful_word(self, word: str) -> bool:
        """単語が意味のあるものかどうかチェック"""
        # URLやメール等を除外
        if 'http' in word or '@' in word or '.com' in word:
            return False
        
        # 全角・半角の記号のみの場合を除外
        if re.match(r'^[!-/:-@\\[-`{-~\s　]+$', word):
            return False
        
        # 連続する同じ文字（笑笑笑等）を除外
        if len(set(word)) == 1 and len(word) > 2:
            return False
        
        return True
    
    def get_word_frequency(self, texts: List[str]) -> Dict[str, int]:
        """全単語の出現頻度辞書を取得"""
        all_words = []
        for text in texts:
            words = self._extract_words_from_text(text)
            all_words.extend(words)
        
        return dict(Counter(all_words))