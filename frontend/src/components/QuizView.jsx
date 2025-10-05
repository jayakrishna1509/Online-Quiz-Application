import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight, Clock, CheckCircle, AlertCircle } from 'lucide-react'
import './QuizView.css'

function QuizView({ quiz, questions, onSubmit, onBack }) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [timeRemaining, setTimeRemaining] = useState(300) // 5 minutes in seconds
  const [startTime] = useState(Date.now())
  const [showSubmitWarning, setShowSubmitWarning] = useState(false)

  const currentQuestion = questions[currentQuestionIndex]
  const totalQuestions = questions.length
  const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100

  // Timer effect
  useEffect(() => {
    if (timeRemaining <= 0) {
      handleSubmit()
      return
    }

    const timer = setInterval(() => {
      setTimeRemaining(prev => prev - 1)
    }, 1000)

    return () => clearInterval(timer)
  }, [timeRemaining])

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const handleOptionSelect = (optionId) => {
    setAnswers({
      ...answers,
      [currentQuestion.id]: optionId
    })
  }

  const handleNext = () => {
    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  const handleSubmit = () => {
    const unansweredCount = totalQuestions - Object.keys(answers).length
    
    if (unansweredCount > 0 && timeRemaining > 0) {
      setShowSubmitWarning(true)
      return
    }

    const formattedAnswers = Object.entries(answers).map(([questionId, selectedOptionId]) => ({
      questionId: parseInt(questionId),
      selectedOptionId: selectedOptionId
    }))

    const timeTaken = Math.floor((Date.now() - startTime) / 1000)
    onSubmit(formattedAnswers, timeTaken)
  }

  const getTimerClass = () => {
    if (timeRemaining <= 30) return 'timer-critical'
    if (timeRemaining <= 60) return 'timer-warning'
    return ''
  }

  const answeredCount = Object.keys(answers).length

  return (
    <div className="quiz-view fade-in">
      {/* Quiz Header */}
      <div className="quiz-header">
        <button className="back-button" onClick={onBack}>
          <ChevronLeft size={20} />
          Back to Quizzes
        </button>
        <h2 className="quiz-title">{quiz.title}</h2>
      </div>

      {/* Timer and Progress */}
      <div className="quiz-info">
        <div className={`timer ${getTimerClass()}`}>
          <Clock size={20} />
          <span>{formatTime(timeRemaining)}</span>
        </div>
        <div className="question-counter">
          Question {currentQuestionIndex + 1} of {totalQuestions}
        </div>
        <div className="answered-counter">
          <CheckCircle size={20} />
          {answeredCount}/{totalQuestions} Answered
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-bar-container">
        <div className="progress-bar" style={{ width: `${progress}%` }}></div>
      </div>

      {/* Question Card */}
      <div className="question-card slide-in" key={currentQuestion.id}>
        <div className="question-header">
          <span className="question-number">Question {currentQuestionIndex + 1}</span>
          {answers[currentQuestion.id] && (
            <span className="answered-badge">
              <CheckCircle size={16} />
              Answered
            </span>
          )}
        </div>
        <h3 className="question-text">{currentQuestion.text}</h3>

        <div className="options-container">
          {currentQuestion.options.map((option, index) => (
            <button
              key={option.id}
              className={`option-button ${
                answers[currentQuestion.id] === option.id ? 'selected' : ''
              }`}
              onClick={() => handleOptionSelect(option.id)}
            >
              <span className="option-letter">
                {String.fromCharCode(65 + index)}
              </span>
              <span className="option-text">{option.text}</span>
              {answers[currentQuestion.id] === option.id && (
                <span className="option-check">
                  <CheckCircle size={20} />
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Navigation */}
      <div className="quiz-navigation">
        <button
          className="nav-button secondary"
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
        >
          <ChevronLeft size={20} />
          Previous
        </button>

        {currentQuestionIndex === totalQuestions - 1 ? (
          <button className="nav-button primary submit-button" onClick={handleSubmit}>
            Submit Quiz
            <CheckCircle size={20} />
          </button>
        ) : (
          <button className="nav-button primary" onClick={handleNext}>
            Next
            <ChevronRight size={20} />
          </button>
        )}
      </div>

      {/* Submit Warning Modal */}
      {showSubmitWarning && (
        <div className="modal-overlay" onClick={() => setShowSubmitWarning(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-icon warning">
              <AlertCircle size={48} />
            </div>
            <h3 className="modal-title">Incomplete Quiz</h3>
            <p className="modal-text">
              You have {totalQuestions - answeredCount} unanswered question(s).
              Are you sure you want to submit?
            </p>
            <div className="modal-actions">
              <button
                className="modal-button secondary"
                onClick={() => setShowSubmitWarning(false)}
              >
                Continue Quiz
              </button>
              <button
                className="modal-button primary"
                onClick={() => {
                  setShowSubmitWarning(false)
                  const formattedAnswers = Object.entries(answers).map(([questionId, selectedOptionId]) => ({
                    questionId: parseInt(questionId),
                    selectedOptionId: selectedOptionId
                  }))
                  const timeTaken = Math.floor((Date.now() - startTime) / 1000)
                  onSubmit(formattedAnswers, timeTaken)
                }}
              >
                Submit Anyway
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default QuizView
