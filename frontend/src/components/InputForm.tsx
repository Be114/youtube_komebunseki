import { useState } from 'react';
import { analyzeVideo } from '../api/client';
import { AnalysisResult } from '../types';
import './InputForm.css';

interface InputFormProps {
  onResult: (result: AnalysisResult) => void;
  onError: (error: string) => void;
  onLoadingChange: (loading: boolean) => void;
}

const InputForm: React.FC<InputFormProps> = ({ onResult, onError, onLoadingChange }) => {
  const [videoUrl, setVideoUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateYouTubeUrl = (url: string): boolean => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)[\w-]+/;
    return youtubeRegex.test(url);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!videoUrl.trim()) {
      onError('YouTube URLを入力してください');
      return;
    }

    if (!validateYouTubeUrl(videoUrl)) {
      onError('有効なYouTube URLを入力してください');
      return;
    }

    setIsSubmitting(true);
    onLoadingChange(true);
    
    try {
      const result = await analyzeVideo(videoUrl);
      onResult(result);
    } catch (error) {
      if (error instanceof Error) {
        onError(error.message);
      } else {
        onError('分析中にエラーが発生しました');
      }
    } finally {
      setIsSubmitting(false);
      onLoadingChange(false);
    }
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setVideoUrl(e.target.value);
    // 入力中はエラーをクリア
    onError('');
  };

  return (
    <div className="input-form-container">
      <form onSubmit={handleSubmit} className="input-form">
        <div className="form-group">
          <label htmlFor="videoUrl">
            YouTube動画URL
          </label>
          <input
            type="url"
            id="videoUrl"
            value={videoUrl}
            onChange={handleUrlChange}
            placeholder="https://www.youtube.com/watch?v=..."
            disabled={isSubmitting}
            className="url-input"
            aria-label="YouTube動画URL入力欄"
            aria-describedby="url-help"
            required
          />
        </div>
        
        <button 
          type="submit" 
          disabled={isSubmitting || !videoUrl.trim()}
          className="analyze-button"
        >
          {isSubmitting ? '分析中...' : 'コメントを分析'}
        </button>
      </form>
      
      <div className="form-info" id="url-help">
        <p>
          <strong>使用方法:</strong>
        </p>
        <ol>
          <li>YouTube動画のURLをコピーして上記に貼り付けてください</li>
          <li>「コメントを分析」ボタンをクリックします</li>
          <li>しばらくお待ちください（最大100件のコメントを分析します）</li>
        </ol>
      </div>
    </div>
  );
};

export default InputForm;