import { useState } from "react";
import "./App.css";

type Page = "dashboard" | "marks" | "analytics" | "recommendations" | "chat";

function App() {
  const [activePage, setActivePage] = useState<Page>("dashboard");

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return (
          <div className="page">
            <h1>Student Dashboard</h1>
            <p className="page-subtitle">
              Here's an overview of your academic performance.
            </p>

            <div className="stats-grid">
              <div className="stat-card">
                <span className="stat-label">Average Marks</span>
                <span className="stat-value">78.5%</span>
              </div>

              <div className="stat-card">
                <span className="stat-label">Attendance</span>
                <span className="stat-value">86%</span>
              </div>

              <div className="stat-card">
                <span className="stat-label">Performance</span>
                <span className="stat-value">Good</span>
              </div>

              <div className="stat-card">
                <span className="stat-label">Risk Level</span>
                <span className="stat-value">Low</span>
              </div>
            </div>

            <div className="content-grid">
              <div className="content-card">
                <h2>Performance Overview</h2>
                <p>
                  Your academic performance is currently stable. Keep
                  maintaining your attendance and marks.
                </p>
              </div>

              <div className="content-card">
                <h2>Quick Recommendation</h2>
                <p>
                  Focus more on your weaker subjects and maintain your current
                  attendance.
                </p>
              </div>
            </div>
          </div>
        );

      case "marks":
        return (
          <div className="page">
            <h1>Marks</h1>
            <p className="page-subtitle">
              View your subject-wise and exam-wise marks.
            </p>

            <div className="content-card">
              <h2>Subject Performance</h2>
              <p>Marks data will be connected to FastAPI later.</p>
            </div>
          </div>
        );

      case "analytics":
        return (
          <div className="page">
            <h1>Analytics</h1>
            <p className="page-subtitle">
              Analyze your academic performance and trends.
            </p>

            <div className="content-card">
              <h2>Performance Trends</h2>
              <p>Charts and analytics will be added here.</p>
            </div>
          </div>
        );

      case "recommendations":
        return (
          <div className="page">
            <h1>Recommendations</h1>
            <p className="page-subtitle">
              Personalized recommendations based on your performance.
            </p>

            <div className="content-card">
              <h2>AI Recommendations</h2>
              <p>
                Your personalized recommendations will appear here.
              </p>
            </div>
          </div>
        );

      case "chat":
        return (
          <div className="page chat-page">
            <h1>AI Chatbot</h1>
            <p className="page-subtitle">
              Ask your AI assistant about your academic performance.
            </p>

            <div className="chat-container">
              <div className="chat-messages">
                <div className="message bot-message">
                  <strong>🤖 AI Assistant</strong>
                  <p>
                    Hi! I'm your Student AI Assistant. Ask me about your
                    marks, attendance, performance, or recommendations.
                  </p>
                </div>
              </div>

              <div className="chat-input-area">
                <input
                  type="text"
                  placeholder="Ask something..."
                />
                <button>Send</button>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">🎓</div>
          <div>
            <h2>Student AI</h2>
            <span>Assistant</span>
          </div>
        </div>

        <nav className="navigation">
          <button
            className={activePage === "dashboard" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("dashboard")}
          >
            <span>📊</span>
            Dashboard
          </button>

          <button
            className={activePage === "marks" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("marks")}
          >
            <span>📚</span>
            Marks
          </button>

          <button
            className={activePage === "analytics" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("analytics")}
          >
            <span>📈</span>
            Analytics
          </button>

          <button
            className={
              activePage === "recommendations"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => setActivePage("recommendations")}
          >
            <span>💡</span>
            Recommendations
          </button>

          <button
            className={activePage === "chat" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("chat")}
          >
            <span>🤖</span>
            AI Chat
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="student-profile">
            <div className="avatar">J</div>
            <div>
              <strong>Jaiakash</strong>
              <span>Student</span>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="welcome-text">Welcome back 👋</span>
            <h3>Jaiakash</h3>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            AI Assistant Online
          </div>
        </header>

        {renderPage()}
      </main>
    </div>
  );
}

export default App;