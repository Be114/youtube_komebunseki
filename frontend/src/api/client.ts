import { AnalysisResult } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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

export const analyzeVideo = async (videoUrl: string): Promise<AnalysisResult> => {
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

      throw new ApiError(errorMessage, response.status);
    }

    const data = await response.json();
    
    // レスポンスデータの検証
    if (!data.sentiment || !data.keywords || typeof data.total_comments !== 'number') {
      throw new ApiError('サーバーから無効なデータが返されました');
    }

    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    // ネットワークエラーまたはその他のエラー
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ApiError(
        'サーバーに接続できません。ネットワーク接続を確認してください。'
      );
    }

    throw new ApiError(
      error instanceof Error ? error.message : '予期しないエラーが発生しました'
    );
  }
};