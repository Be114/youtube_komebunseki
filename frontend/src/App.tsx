import React, { useState } from 'react';
import './App.css';
import InputForm from './components/InputForm';
import SentimentChart from './components/SentimentChart';
import WordCloud from './components/WordCloud';
import { AnalysisResult } from './types';

function App() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalysisResult = (result: AnalysisResult) => {
    setAnalysisResult(result);
    setError(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setAnalysisResult(null);
  };

  const handleLoadingChange = (isLoading: boolean) => {
    setLoading(isLoading);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>YouTube コメント分析</h1>
        <p>YouTube動画のコメントを感情分析・キーワード抽出で可視化</p>
      </header>

      <main className="App-main">
        <div className="container">
          <InputForm 
            onResult={handleAnalysisResult}
            onError={handleError}
            onLoadingChange={handleLoadingChange}
          />

          {loading && (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>コメントを分析中...</p>
            </div>
          )}

          {error && (
            <div className="error-container">
              <h3>エラー</h3>
              <p>{error}</p>
            </div>
          )}

          {analysisResult && !loading && (
            <div className="results-container">
              <div className="results-header">
                <h2>分析結果</h2>
                <p>総コメント数: {analysisResult.total_comments}件</p>
              </div>

              <div className="charts-container">
                <div className="chart-section">
                  <h3>感情分析</h3>
                  <SentimentChart sentiment={analysisResult.sentiment} />
                </div>

                <div className="chart-section">
                  <h3>頻出キーワード</h3>
                  <WordCloud keywords={analysisResult.keywords} />
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>&copy; 2025 YouTube Comment Analyzer</p>
      </footer>
    </div>
  );
}

export default App;