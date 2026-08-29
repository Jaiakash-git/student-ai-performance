import { useState } from "react";

import "./App.css";


/* ==========================================
   MESSAGE
   ========================================== */

interface Message {
  sender: "user" | "ai";
  text: string;
}


/* ==========================================
   AGENT MEMORY
   ========================================== */

interface AgentContext {
  student_name?: string;
  last_intent?: string | null;
  last_subject?: string | null;
  requested_subject?: string | null;
  last_result?: Record<string, unknown> | null;
}


/* ==========================================
   DASHBOARD DATA
   ========================================== */

interface DashboardData {
  student_name: string;

  average: number;
  attendance: number;

  performance_status: string;

  risk_level: string;
  risk_probability: number;

  highest_subject: string;
  highest_mark: number;

  lowest_subject: string;
  lowest_mark: number;

  overall_trend: string;
  average_improvement: number;

  recommendation: string;
  priority_subject: string;
  priority_mark: number;
}


function App() {

  /* ========================================
     STUDENT
     ======================================== */

  const [studentName, setStudentName] = useState("");

  const [nameInput, setNameInput] = useState("");


  /* ========================================
     DASHBOARD
     ======================================== */

  const [dashboard, setDashboard] =
    useState<DashboardData | null>(null);

  const [dashboardLoading, setDashboardLoading] =
    useState(false);

  const [dashboardError, setDashboardError] =
    useState("");


  /* ========================================
     CHAT
     ======================================== */

  const [isChatOpen, setIsChatOpen] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [messages, setMessages] =
    useState<Message[]>([]);

  const [loading, setLoading] =
    useState(false);


  /* ========================================
     AGENT MEMORY
     ======================================== */

  const [context, setContext] =
    useState<AgentContext | null>(null);


  /* ========================================
     LOAD DASHBOARD
     ======================================== */

  const loadDashboard = async (
    name: string
  ) => {

    setDashboardLoading(true);
    setDashboardError("");

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/student/${encodeURIComponent(name)}/dashboard`
      );

      if (!response.ok) {

        let errorMessage =
          "Unable to load student data.";

        try {

          const errorData =
            await response.json();

          if (errorData.detail) {
            errorMessage = errorData.detail;
          }

        } catch {
          // Ignore JSON parsing error
        }

        throw new Error(errorMessage);
      }

      const data: DashboardData =
        await response.json();

      setDashboard(data);

    } catch (error) {

      console.error(error);

      setDashboardError(
        error instanceof Error
          ? error.message
          : "Unable to connect to the AI server."
      );

    } finally {

      setDashboardLoading(false);

    }
  };


  /* ========================================
     START
     ======================================== */

  const startDashboard = async () => {

    const name = nameInput.trim();

    if (!name || dashboardLoading) {
      return;
    }

    setStudentName(name);

    setContext(null);

    setMessages([
      {
        sender: "ai",
        text: `Hello ${name}! 👋 How can I help you today?`,
      },
    ]);

    await loadDashboard(name);
  };


  /* ========================================
     SEND CHAT MESSAGE
     ======================================== */

  const sendMessage = async () => {

    if (!message.trim() || loading) {
      return;
    }

    const userMessage = message.trim();

    /* Add user message immediately */

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userMessage,
      },
    ]);

    setMessage("");

    setLoading(true);


    try {

      /* ====================================
         CALL FASTAPI AGENT
         ==================================== */

      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            student_name: studentName,
            message: userMessage,
            context: context,
          }),
        }
      );


      /* ====================================
         CHECK RESPONSE
         ==================================== */

      if (!response.ok) {
        throw new Error(
          "API request failed"
        );
      }


      const data = await response.json();


      /* ====================================
         UPDATE MEMORY
         ==================================== */

      setContext(data.context);


      /* ====================================
         ADD AI RESPONSE
         ==================================== */

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: data.response,
        },
      ]);

    } catch (error) {

      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text:
            "Sorry, I couldn't connect to the AI server.",
        },
      ]);

    } finally {

      setLoading(false);

    }
  };


  /* ========================================
     ENTER KEY
     ======================================== */

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {

    if (event.key === "Enter") {
      sendMessage();
    }
  };


  /* ========================================
     NAME SCREEN
     ======================================== */

  if (!studentName) {

    return (

      <div className="welcome-container">

        <div className="welcome-card">

          <div className="welcome-logo">
            🤖
          </div>

          <h1>
            Student AI Assistant
          </h1>

          <p className="welcome-text">
            Your intelligent academic companion
          </p>

          <label>
            Enter your student name
          </label>

          <input
            type="text"
            placeholder="Enter your name"
            value={nameInput}
            onChange={(event) =>
              setNameInput(event.target.value)
            }
            onKeyDown={(event) => {

              if (event.key === "Enter") {
                startDashboard();
              }

            }}
            disabled={dashboardLoading}
          />

          <button
            onClick={startDashboard}
            disabled={
              dashboardLoading ||
              !nameInput.trim()
            }
          >

            {dashboardLoading
              ? "Loading..."
              : "Continue →"}

          </button>

        </div>

      </div>
    );
  }


  /* ========================================
     DASHBOARD LOADING
     ======================================== */

  if (dashboardLoading && !dashboard) {

    return (

      <div className="loading-screen">

        <div className="loading-card">

          <div className="loading-icon">
            🤖
          </div>

          <h2>
            Preparing your dashboard...
          </h2>

          <p>
            Loading your academic information
          </p>

          <div className="loading-spinner"></div>

        </div>

      </div>
    );
  }


  /* ========================================
     DASHBOARD ERROR
     ======================================== */

  if (dashboardError && !dashboard) {

    return (

      <div className="error-screen">

        <div className="error-card">

          <div className="error-icon">
            ⚠️
          </div>

          <h2>
            Unable to load dashboard
          </h2>

          <p>
            {dashboardError}
          </p>

          <button
            onClick={() => {

              setStudentName("");
              setDashboard(null);
              setDashboardError("");

            }}
          >
            Try Again
          </button>

        </div>

      </div>
    );
  }


  /* ========================================
     MAIN DASHBOARD
     ======================================== */

  return (

    <div className="app-container">

      {/* ====================================
          SIDEBAR
          ==================================== */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            🤖
          </div>

          <div>

            <h2>
              Student AI
            </h2>

            <span>
              Academic Assistant
            </span>

          </div>

        </div>


        <nav className="sidebar-nav">

          <div className="nav-item active">
            <span>📊</span>
            Dashboard
          </div>

          <div className="nav-item">
            <span>📈</span>
            Performance
          </div>

          <div className="nav-item">
            <span>🎯</span>
            Analytics
          </div>

          <div className="nav-item">
            <span>💡</span>
            Insights
          </div>

        </nav>


        <div className="sidebar-bottom">

          <div className="student-mini">

            <div className="student-avatar">
              {studentName.charAt(0).toUpperCase()}
            </div>

            <div>

              <strong>
                {studentName}
              </strong>

              <span>
                Student
              </span>

            </div>

          </div>


          <button
            className="change-student"
            onClick={() => {

              setStudentName("");
              setDashboard(null);
              setMessages([]);
              setContext(null);
              setIsChatOpen(false);

            }}
          >
            ↩ Change Student
          </button>

        </div>

      </aside>


      {/* ====================================
          MAIN CONTENT
          ==================================== */}

      <main className="dashboard">

        {/* HEADER */}

        <header className="dashboard-header">

          <div>

            <p className="header-label">
              STUDENT DASHBOARD
            </p>

            <h1>
              Welcome back, {studentName} 👋
            </h1>

            <p className="header-subtitle">
              Here's your current academic overview.
            </p>

          </div>


          <div className="header-profile">

            <div className="profile-avatar">
              {studentName.charAt(0).toUpperCase()}
            </div>

            <div>

              <strong>
                {studentName}
              </strong>

              <span>
                Academic Profile
              </span>

            </div>

          </div>

        </header>


        {dashboard && (

          <>

            {/* ==================================
                STAT CARDS
                ================================== */}

            <section className="stats-grid">

              <div className="stat-card">

                <div className="stat-top">

                  <span>
                    Average Mark
                  </span>

                  <div className="stat-icon purple">
                    📊
                  </div>

                </div>

                <div className="stat-value">
                  {dashboard.average.toFixed(2)}
                </div>

                <div className="stat-description">
                  Overall academic average
                </div>

              </div>


              <div className="stat-card">

                <div className="stat-top">

                  <span>
                    Attendance
                  </span>

                  <div className="stat-icon blue">
                    📅
                  </div>

                </div>

                <div className="stat-value">
                  {dashboard.attendance.toFixed(2)}%
                </div>

                <div className="stat-description">
                  Overall attendance
                </div>

              </div>


              <div className="stat-card">

                <div className="stat-top">

                  <span>
                    Academic Risk
                  </span>

                  <div className="stat-icon green">
                    🛡️
                  </div>

                </div>

                <div className="stat-value risk-low">
                  {dashboard.risk_level}
                </div>

                <div className="stat-description">
                  Risk probability:{" "}
                  {dashboard.risk_probability.toFixed(2)}%
                </div>

              </div>


              <div className="stat-card">

                <div className="stat-top">

                  <span>
                    Performance
                  </span>

                  <div className="stat-icon orange">
                    ⭐
                  </div>

                </div>

                <div className="stat-value performance-value">
                  {dashboard.performance_status}
                </div>

                <div className="stat-description">
                  Current performance status
                </div>

              </div>

            </section>


            {/* ==================================
                MAIN GRID
                ================================== */}

            <section className="dashboard-grid">


              {/* PERFORMANCE OVERVIEW */}

              <div className="panel performance-panel">

                <div className="panel-header">

                  <div>

                    <h2>
                      Academic Overview
                    </h2>

                    <p>
                      Your current subject performance
                    </p>

                  </div>

                  <span className="panel-badge">
                    {dashboard.overall_trend}
                  </span>

                </div>


                <div className="subject-comparison">

                  <div className="subject-card highest">

                    <div className="subject-icon">
                      🏆
                    </div>

                    <div>

                      <span>
                        Highest Scoring
                      </span>

                      <h3>
                        {dashboard.highest_subject}
                      </h3>

                      <strong>
                        {dashboard.highest_mark.toFixed(2)}
                      </strong>

                    </div>

                  </div>


                  <div className="subject-card lowest">

                    <div className="subject-icon">
                      📚
                    </div>

                    <div>

                      <span>
                        Priority Subject
                      </span>

                      <h3>
                        {dashboard.lowest_subject}
                      </h3>

                      <strong>
                        {dashboard.lowest_mark.toFixed(2)}
                      </strong>

                    </div>

                  </div>

                </div>


                <div className="trend-section">

                  <div className="trend-header">

                    <div>

                      <span>
                        Overall Performance Trend
                      </span>

                      <h3>
                        {dashboard.overall_trend}
                      </h3>

                    </div>

                    <div className="trend-number">
                      {dashboard.average_improvement >= 0
                        ? "+"
                        : ""}
                      {dashboard.average_improvement.toFixed(2)}
                    </div>

                  </div>


                  <div className="trend-bar">

                    <div
                      className={
                        dashboard.average_improvement >= 0
                          ? "trend-progress improving"
                          : "trend-progress declining"
                      }
                      style={{
                        width: `${Math.min(
                          Math.max(
                            Math.abs(
                              dashboard.average_improvement
                            ) * 10,
                            5
                          ),
                          100
                        )}%`,
                      }}
                    />

                  </div>

                  <p>
                    Average improvement across subjects
                  </p>

                </div>

              </div>


              {/* AI INSIGHTS */}

              <div className="panel insight-panel">

                <div className="panel-header">

                  <div>

                    <h2>
                      AI Insight
                    </h2>

                    <p>
                      Personalized recommendation
                    </p>

                  </div>

                  <div className="ai-small-icon">
                    🤖
                  </div>

                </div>


                <div className="recommendation-box">

                  <div className="recommendation-icon">
                    💡
                  </div>

                  <p>
                    {dashboard.recommendation}
                  </p>

                </div>


                <div className="priority-box">

                  <span>
                    Priority Subject
                  </span>

                  <div>

                    <strong>
                      {dashboard.priority_subject}
                    </strong>

                    <span>
                      {dashboard.priority_mark.toFixed(2)} marks
                    </span>

                  </div>

                </div>


                <button
                  className="ask-ai-button"
                  onClick={() =>
                    setIsChatOpen(true)
                  }
                >
                  🤖 Ask AI Assistant
                </button>

              </div>

            </section>


            {/* ==================================
                QUICK SUMMARY
                ================================== */}

            <section className="summary-panel">

              <div>

                <span className="summary-label">
                  YOUR ACADEMIC SUMMARY
                </span>

                <h2>
                  {dashboard.overall_trend === "Improving"
                    ? "You're making good progress! 🚀"
                    : "Keep working on your academic goals! 💪"}
                </h2>

                <p>
                  Your average is{" "}
                  <strong>
                    {dashboard.average.toFixed(2)}
                  </strong>{" "}
                  with{" "}
                  <strong>
                    {dashboard.attendance.toFixed(2)}%
                  </strong>{" "}
                  attendance. Your current academic risk
                  level is{" "}
                  <strong>
                    {dashboard.risk_level}
                  </strong>
                  .
                </p>

              </div>


              <button
                className="summary-chat-button"
                onClick={() =>
                  setIsChatOpen(true)
                }
              >
                Chat with AI →
              </button>

            </section>

          </>

        )}

      </main>


      {/* ====================================
          FLOATING AI BUTTON
          ==================================== */}

      {!isChatOpen && (

        <button
          className="floating-ai-button"
          onClick={() =>
            setIsChatOpen(true)
          }
        >

          <span className="floating-ai-icon">
            🤖
          </span>

          <span>
            Ask AI
          </span>

        </button>

      )}


      {/* ====================================
          CHAT OVERLAY
          ==================================== */}

      {isChatOpen && (

        <>

          <div
            className="chat-overlay"
            onClick={() =>
              setIsChatOpen(false)
            }
          />


          <aside className="chat-panel">

            {/* CHAT HEADER */}

            <div className="chat-panel-header">

              <div className="chat-title">

                <div className="chat-avatar">
                  🤖
                </div>

                <div>

                  <h2>
                    Student AI
                  </h2>

                  <span>
                    Your academic assistant
                  </span>

                </div>

              </div>


              <button
                className="chat-close"
                onClick={() =>
                  setIsChatOpen(false)
                }
              >
                ✕
              </button>

            </div>


            {/* CHAT MESSAGES */}

            <div className="chat-messages">

              {messages.map(
                (msg, index) => (

                  <div
                    key={index}
                    className={`message-row ${msg.sender}`}
                  >

                    <div className="message-bubble">
                      {msg.text}
                    </div>

                  </div>

                )
              )}


              {loading && (

                <div className="message-row ai">

                  <div className="message-bubble typing">
                    <span />
                    <span />
                    <span />
                  </div>

                </div>

              )}

            </div>


            {/* CHAT INPUT */}

            <div className="chat-input-area">

              <input
                type="text"
                placeholder="Ask about your academics..."
                value={message}
                onChange={(event) =>
                  setMessage(event.target.value)
                }
                onKeyDown={handleKeyDown}
                disabled={loading}
              />

              <button
                onClick={sendMessage}
                disabled={
                  loading ||
                  !message.trim()
                }
              >
                ➤
              </button>

            </div>

          </aside>

        </>

      )}

    </div>
  );
}


export default App;

