export interface KeywordItem {
  word: string;
  count: number;
}

export interface SentimentData {
  positive: number;
  neutral: number;
  negative: number;
}

export interface AnalysisResult {
  sentiment: SentimentData;
  keywords: KeywordItem[];
  total_comments: number;
}