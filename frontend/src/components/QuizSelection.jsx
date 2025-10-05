import { BookOpen, Code2, Database } from 'lucide-react'
import './QuizSelection.css'

function QuizSelection({ quizzes, onSelectQuiz }) {
  // Function to get icon based on quiz title
  const getQuizIcon = (title) => {
    if (title.includes('Programming')) {
      return <Code2 size={48} />
    } else if (title.includes('JavaScript')) {
      return (
        <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
          <path d="M0 0h24v24H0V0zm22.034 18.276c-.175-1.095-.888-2.015-3.003-2.873-.736-.345-1.554-.585-1.797-1.14-.091-.33-.105-.51-.046-.705.15-.646.915-.84 1.515-.66.39.12.75.42.976.9 1.034-.676 1.034-.676 1.755-1.125-.27-.42-.404-.601-.586-.78-.63-.705-1.469-1.065-2.834-1.034l-.705.089c-.676.165-1.32.525-1.71 1.005-1.14 1.291-.811 3.541.569 4.471 1.365 1.02 3.361 1.244 3.616 2.205.24 1.17-.87 1.545-1.966 1.41-.811-.18-1.26-.586-1.755-1.336l-1.83 1.051c.21.48.45.689.81 1.109 1.74 1.756 6.09 1.666 6.871-1.004.029-.09.24-.705.074-1.65l.046.067zm-8.983-7.245h-2.248c0 1.938-.009 3.864-.009 5.805 0 1.232.063 2.363-.138 2.711-.33.689-1.18.601-1.566.48-.396-.196-.597-.466-.83-.855-.063-.105-.11-.196-.127-.196l-1.825 1.125c.305.63.75 1.172 1.324 1.517.855.51 2.004.675 3.207.405.783-.226 1.458-.691 1.811-1.411.51-.93.402-2.07.397-3.346.012-2.054 0-4.109 0-6.179l.004-.056z"/>
        </svg>
      )
    } else if (title.includes('Database')) {
      return <Database size={48} />
    }
    return <BookOpen size={48} />
  }

  return (
    <div className="quiz-selection fade-in">
      <div className="selection-header">
        <h2 className="selection-title">Choose Your Quiz</h2>
        <p className="selection-subtitle">
          Select a Quiz to Test Your Knowledge and Challenge Yourself
        </p>
      </div>

      {quizzes.length === 0 ? (
        <div className="no-quizzes">
          <BookOpen size={64} className="no-quizzes-icon" />
          <h3>No Quizzes Available</h3>
          <p>Please check back later or contact the administrator.</p>
        </div>
      ) : (
        <div className="quiz-grid">
          {quizzes.map((quiz, index) => (
            <div
              key={quiz.id}
              className="quiz-card slide-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="quiz-card-icon">
                {getQuizIcon(quiz.title)}
              </div>
              <div className="quiz-card-content">
                <h3 className="quiz-card-title">{quiz.title}</h3>
                <p className="quiz-card-description">
                  Test Your Knowledge in This Category
                </p>
              </div>
              <button 
                className="start-quiz-button"
                onClick={() => onSelectQuiz(quiz.id)}
              >
                Start Quiz
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default QuizSelection
