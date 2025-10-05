import {
  Trophy,
  CheckCircle,
  XCircle,
  Clock,
  RotateCcw,
  Home,
} from "lucide-react";
import "./ResultsView.css";

function ResultsView({ results, quizTitle, onRetake, deployLink }) {
  const {
    score,
    total,
    percentage,
    results: detailedResults,
    timeTaken,
  } = results;

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  const getPerformanceMessage = () => {
    if (percentage >= 90)
      return { text: "Outstanding! 🎉", color: "excellent" };
    if (percentage >= 75) return { text: "Great Job! 👏", color: "great" };
    if (percentage >= 60) return { text: "Good Effort! 👍", color: "good" };
    if (percentage >= 40) return { text: "Keep Practicing! 💪", color: "fair" };
    return { text: "Don't Give Up! 📚", color: "needs-improvement" };
  };

  const performance = getPerformanceMessage();

  return (
    <div className="results-view fade-in">
      {/* Results Header */}
      <div className="results-header">
        <div className={`trophy-icon ${performance.color}`}>
          <Trophy size={64} />
        </div>
        <h2 className="results-title">Quiz Completed!</h2>
        <p className="results-subtitle">{quizTitle}</p>
      </div>

      {/* Score Card */}
      <div className="score-card slide-in">
        <div className="score-main">
          <div className="score-circle">
            <svg className="score-ring" viewBox="0 0 120 120">
              <circle
                className="score-ring-bg"
                cx="60"
                cy="60"
                r="54"
                fill="none"
                stroke="var(--bg-tertiary)"
                strokeWidth="8"
              />
              <circle
                className="score-ring-progress"
                cx="60"
                cy="60"
                r="54"
                fill="none"
                stroke="url(#gradient)"
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray={`${(percentage / 100) * 339.292} 339.292`}
                transform="rotate(-90 60 60)"
              />
              <defs>
                <linearGradient
                  id="gradient"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="100%"
                >
                  <stop offset="0%" stopColor="var(--primary-color)" />
                  <stop offset="100%" stopColor="var(--secondary-color)" />
                </linearGradient>
              </defs>
            </svg>
            <div className="score-text">
              <div className="score-percentage">{percentage}%</div>
              <div className="score-fraction">
                {score}/{total}
              </div>
            </div>
          </div>
          <div className={`performance-message ${performance.color}`}>
            {performance.text}
          </div>
        </div>

        <div className="score-stats">
          <div className="stat-item">
            <CheckCircle className="stat-icon success" size={24} />
            <div className="stat-content">
              <div className="stat-label">Correct</div>
              <div className="stat-value">{score}</div>
            </div>
          </div>
          <div className="stat-item">
            <XCircle className="stat-icon error" size={24} />
            <div className="stat-content">
              <div className="stat-label">Incorrect</div>
              <div className="stat-value">{total - score}</div>
            </div>
          </div>
          <div className="stat-item">
            <Clock className="stat-icon" size={24} />
            <div className="stat-content">
              <div className="stat-label">Time Taken</div>
              <div className="stat-value">{formatTime(timeTaken)}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Results */}
      <div className="detailed-results">
        <h3 className="detailed-title">Question Breakdown</h3>
        <div className="results-list">
          {detailedResults.map((result, index) => (
            <div
              key={result.questionId}
              className={`result-item ${
                result.isCorrect ? "correct" : "incorrect"
              } slide-in`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="result-header">
                <span className="result-number">Question {index + 1}</span>
                <span
                  className={`result-badge ${
                    result.isCorrect ? "correct" : "incorrect"
                  }`}
                >
                  {result.isCorrect ? (
                    <>
                      <CheckCircle size={16} />
                      Correct
                    </>
                  ) : (
                    <>
                      <XCircle size={16} />
                      Incorrect
                    </>
                  )}
                </span>
              </div>
              <p className="result-question">{result.questionText}</p>
              <div className="result-answers">
                <div className="answer-row">
                  <span className="answer-label">Your Answer:</span>
                  <span
                    className={`answer-value ${
                      result.isCorrect ? "correct" : "incorrect"
                    }`}
                  >
                    {result.userAnswer}
                  </span>
                </div>
                {!result.isCorrect && (
                  <div className="answer-row">
                    <span className="answer-label">Correct Answer:</span>
                    <span className="answer-value correct">
                      {result.correctAnswer}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="results-actions">
        <button className="action-button secondary" onClick={onRetake}>
          <Home size={20} />
          Back to Quizzes
        </button>
        <button className="action-button primary" onClick={onRetake}>
          <RotateCcw size={20} />
          Try Another Quiz
        </button>
        {deployLink && (
          <a
            className="deploy-link"
            href={deployLink}
            target="_blank"
            rel="noopener noreferrer"
            style={{ marginLeft: "12px", alignSelf: "center" }}
          >
            View Live (Single Deploy)
          </a>
        )}
      </div>
    </div>
  );
}

export default ResultsView;
