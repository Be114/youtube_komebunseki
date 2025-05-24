import { AnalysisResult } from '../types';

declare const process: {
  env: {
    REACT_APP_API_URL?: string;
  }
};

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const MAX_RETRY_ATTEMPTS = 3;
const RETRY_DELAY = 1000; // 1秒

export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public code?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const analyzeVideo = async (videoUrl: string): Promise<AnalysisResult> => {
  let lastError: Error | null = null;
  
  for (let attempt = 1; attempt <= MAX_RETRY_ATTEMPTS; attempt++) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_url: videoUrl,
        }),
      });

      if (!response.ok) {
        let errorMessage = 'サーバーエラーが発生しました';
        
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch {
          // JSONパースに失敗した場合は、ステータスに基づいてメッセージを設定
          switch (response.status) {
            case 400:
              errorMessage = '無効なリクエストです。YouTube URLを確認してください。';
              break;
            case 403:
              errorMessage = 'YouTube APIの利用制限に達しました。しばらく待ってから再試行してください。';
              break;
            case 404:
              errorMessage = '動画が見つかりません。URLを確認してください。';
              break;
            case 429:
              errorMessage = 'リクエスト数が多すぎます。しばらく待ってから再試行してください。';
              break;
            case 500:
              errorMessage = 'サーバー内部エラーが発生しました。';
              break;
            default:
              errorMessage = `エラーが発生しました (${response.status})`;
          }
        }

        // 403や429の場合は再試行しない
        if (response.status === 403 || response.status === 429) {
          throw new ApiError(errorMessage, response.status);
        }

        throw new ApiError(errorMessage, response.status);
      }

      const data = await response.json();
      
      // レスポンスデータの検証
      if (!data.sentiment || !data.keywords || typeof data.total_comments !== 'number') {
        throw new ApiError('サーバーから無効なデータが返されました');
      }

      return data;
    } catch (error) {
      lastError = error as Error;
      
      if (error instanceof ApiError) {
        // APIエラーの場合、特定のステータスコードでは再試行しない
        if (error.status && [400, 403, 404, 429].indexOf(error.status) !== -1) {
          throw error;
        }
      }

      // ネットワークエラーまたはその他のエラー
      if (error instanceof TypeError && error.message.includes('fetch')) {
        lastError = new ApiError(
          'サーバーに接続できません。ネットワーク接続を確認してください。'
        );
      }

      // 最後の試行でない場合は、遅延後に再試行
      if (attempt < MAX_RETRY_ATTEMPTS) {
        await sleep(RETRY_DELAY * attempt); // 指数バックオフ
        continue;
      }
    }
  }

  // すべての再試行が失敗した場合
  throw lastError || new ApiError('予期しないエラーが発生しました');
};
