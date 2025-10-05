import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import QuizSelection from "./components/QuizSelection";
import QuizView from "./components/QuizView";
import ResultsView from "./components/ResultsView";
import LoadingSpinner from "./components/LoadingSpinner";

const API_BASE_URL = "http://localhost:5000/api";

function App() {
  const [currentView, setCurrentView] = useState("selection"); // selection, quiz, results
  const [quizzes, setQuizzes] = useState([]);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all quizzes on mount
  useEffect(() => {
    fetchQuizzes();
  }, []);

  const fetchQuizzes = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/quizzes`);
      setQuizzes(response.data);
    } catch (err) {
      setError(
        "Failed to Load Quizzes. Please Make Sure the backend is Running."
      );
      console.error("Error fetching quizzes:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuizSelect = async (quizId) => {
    setLoading(true);
    setError(null);
    try {
      const quiz = quizzes.find((q) => q.id === quizId);
      setSelectedQuiz(quiz);

      const response = await axios.get(
        `${API_BASE_URL}/quizzes/${quizId}/questions`
      );
      setQuestions(response.data);
      setCurrentView("quiz");
    } catch (err) {
      setError("Failed to load quiz questions.");
      console.error("Error fetching questions:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuizSubmit = async (answers, timeTaken) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(
        `${API_BASE_URL}/quizzes/${selectedQuiz.id}/submit`,
        { answers }
      );
      setResults({ ...response.data, timeTaken });
      setCurrentView("results");
    } catch (err) {
      setError("Failed to submit quiz. Please try again.");
      console.error("Error submitting quiz:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRetakeQuiz = () => {
    setCurrentView("selection");
    setSelectedQuiz(null);
    setQuestions([]);
    setResults(null);
    setError(null);
  };

  const handleBackToSelection = () => {
    setCurrentView("selection");
    setSelectedQuiz(null);
    setQuestions([]);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="container">
          <h1 className="app-title">
            Online Quiz Application
            <span className="title-icon">📋</span>
          </h1>
          <p className="app-subtitle">Write Quiz and Test Your Knowledge</p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {error && (
            <div className="error-banner fade-in">
              <span className="error-icon">⚠️</span>
              {error}
              <button className="error-close" onClick={() => setError(null)}>
                ×
              </button>
            </div>
          )}

          {loading && <LoadingSpinner />}

          {!loading && currentView === "selection" && (
            <QuizSelection quizzes={quizzes} onSelectQuiz={handleQuizSelect} />
          )}

          {!loading && currentView === "quiz" && (
            <QuizView
              quiz={selectedQuiz}
              questions={questions}
              onSubmit={handleQuizSubmit}
              onBack={handleBackToSelection}
            />
          )}

          {!loading && currentView === "results" && (
            <ResultsView
              results={results}
              quizTitle={selectedQuiz?.title}
              onRetake={handleRetakeQuiz}
            />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>
            &copy; 2025 Online Quiz Application. Built With Full Stack
            Application.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
