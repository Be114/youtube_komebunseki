import { useMemo } from 'react';
import { KeywordItem } from '../types';
import './WordCloud.css';

interface WordCloudProps {
  keywords: KeywordItem[];
}

const WordCloud: React.FC<WordCloudProps> = ({ keywords }) => {
  const maxCount = useMemo(() => {
    return Math.max(...keywords.map(item => item.count), 1);
  }, [keywords]);

  const getWordSize = (count: number): number => {
    // 最小14px、最大40pxの範囲でサイズを計算
    const minSize = 14;
    const maxSize = 40;
    const ratio = count / maxCount;
    return Math.round(minSize + (maxSize - minSize) * ratio);
  };

  const getWordColor = (count: number): string => {
    // カウントに基づいて色を変更
    const colors = [
      '#667eea', '#764ba2', '#f093fb', '#f5576c',
      '#4facfe', '#00f2fe', '#43e97b', '#38f9d7',
      '#ffecd2', '#fcb69f', '#a8edea', '#fed6e3'
    ];
    
    const ratio = count / maxCount;
    const colorIndex = Math.floor(ratio * (colors.length - 1));
    return colors[colorIndex] || colors[0];
  };

  if (keywords.length === 0) {
    return (
      <div className="wordcloud-container">
        <div className="no-keywords">
          キーワードが見つかりませんでした
        </div>
      </div>
    );
  }

  return (
    <div className="wordcloud-container">
      <div className="wordcloud-grid">
        {keywords.map((keyword, index) => (
          <div
            key={`${keyword.word}-${index}`}
            className="keyword-item"
            style={{
              fontSize: `${getWordSize(keyword.count)}px`,
              color: getWordColor(keyword.count),
            }}
            title={`${keyword.word}: ${keyword.count}回`}
          >
            {keyword.word}
          </div>
        ))}
      </div>
      
      <div className="keyword-list">
        <h4>キーワード一覧</h4>
        <div className="keyword-table">
          {keywords.slice(0, 10).map((keyword, index) => (
            <div key={`list-${keyword.word}-${index}`} className="keyword-row">
              <span className="keyword-rank">{index + 1}</span>
              <span className="keyword-word">{keyword.word}</span>
              <span className="keyword-count">{keyword.count}回</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default WordCloud;