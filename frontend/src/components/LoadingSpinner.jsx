import './LoadingSpinner.css'

function LoadingSpinner() {
  return (
    <div className="loading-container fade-in">
      <div className="spinner"></div>
      <p className="loading-text">Loading...</p>
    </div>
  )
}

export default LoadingSpinner
