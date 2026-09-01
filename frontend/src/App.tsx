import { useEffect, useRef, useState } from "react";
import "./App.css";

interface Message {
  sender: "user" | "ai";
  text: string;
}

interface AgentContext {
  student_name?: string;
  last_intent?: string | null;
  last_subject?: string | null;
  requested_subject?: string | null;
  last_result?: Record<string, unknown> | null;
}

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

interface AuthResponse {
  message: string;
  access_token: string;
  token_type: string;
  student_id: number;
  username: string;
  student_name: string;
}

const API_URL = "http://127.0.0.1:8000";

function App() {
  // ========================================
  // AUTHENTICATION
  // ========================================

  const [authMode, setAuthMode] =
    useState<"login" | "register">("login");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [studentId, setStudentId] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState("");
  const [authSuccess, setAuthSuccess] = useState("");

  const [token, setToken] = useState<string | null>(
    localStorage.getItem("student_ai_token")
  );

  // ========================================
  // STUDENT
  // ========================================

  const [studentName, setStudentName] = useState(
    localStorage.getItem("student_ai_name") || ""
  );

  // ========================================
  // DASHBOARD
  // ========================================

  const [dashboard, setDashboard] =
    useState<DashboardData | null>(null);

  const [dashboardLoading, setDashboardLoading] =
    useState(false);

  const [dashboardError, setDashboardError] =
    useState("");

  // ========================================
  // CHAT
  // ========================================

  const [isChatOpen, setIsChatOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const [context, setContext] =
    useState<AgentContext | null>(null);

  const chatEndRef =
    useRef<HTMLDivElement | null>(null);

  // ========================================
  // AUTH INPUT REFS
  // ========================================

  const usernameRef =
    useRef<HTMLInputElement | null>(null);

  const passwordRef =
    useRef<HTMLInputElement | null>(null);

  const studentIdRef =
    useRef<HTMLInputElement | null>(null);

  // ========================================
  // AUTO SCROLL CHAT
  // ========================================

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading, isChatOpen]);

  // ========================================
  // LOGOUT
  // ========================================

  const logout = () => {
    localStorage.removeItem("student_ai_token");
    localStorage.removeItem("student_ai_name");

    setToken(null);
    setStudentName("");
    setDashboard(null);
    setMessages([]);
    setContext(null);
    setIsChatOpen(false);

    setUsername("");
    setPassword("");
    setStudentId("");

    setAuthError("");
    setAuthSuccess("");
    setShowPassword(false);
  };

  // ========================================
  // LOGIN
  // ========================================

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      setAuthError(
        "Please enter your username and password."
      );
      return;
    }

    setAuthLoading(true);
    setAuthError("");
    setAuthSuccess("");

    try {
      const response = await fetch(
        `${API_URL}/auth/login`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: username.trim(),
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Invalid username or password."
        );
      }

      const authData: AuthResponse = data;

      // Save authentication data
      localStorage.setItem(
        "student_ai_token",
        authData.access_token
      );

      localStorage.setItem(
        "student_ai_name",
        authData.student_name
      );

      setToken(authData.access_token);
      setStudentName(authData.student_name);

      setPassword("");
      setShowPassword(false);

      setMessages([
        {
          sender: "ai",
          text: `Hello ${authData.student_name}! 👋 How can I help you today?`,
        },
      ]);

      await loadDashboard(
        authData.student_name,
        authData.access_token
      );
    } catch (error) {
      console.error(error);

      setAuthError(
        error instanceof Error
          ? error.message
          : "Unable to connect to the AI server."
      );
    } finally {
      setAuthLoading(false);
    }
  };

  // ========================================
  // REGISTER
  // ========================================

  const handleRegister = async () => {
    if (
      !studentId.trim() ||
      !username.trim() ||
      !password.trim()
    ) {
      setAuthError(
        "Please fill in all fields."
      );
      return;
    }

    const numericStudentId =
      Number(studentId);

    if (
      !Number.isInteger(numericStudentId) ||
      numericStudentId <= 0
    ) {
      setAuthError(
        "Student ID must be a valid number."
      );
      return;
    }

    setAuthLoading(true);
    setAuthError("");
    setAuthSuccess("");

    try {
      const response = await fetch(
        `${API_URL}/auth/register`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            student_id: numericStudentId,
            username: username.trim(),
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Registration failed."
        );
      }

      setAuthSuccess(
        "Registration successful! You can now login."
      );

      setAuthMode("login");

      setStudentId("");
      setPassword("");
      setShowPassword(false);
    } catch (error) {
      console.error(error);

      setAuthError(
        error instanceof Error
          ? error.message
          : "Unable to register."
      );
    } finally {
      setAuthLoading(false);
    }
  };

  // ========================================
  // LOAD DASHBOARD
  // ========================================

  const loadDashboard = async (
    name: string,
    authToken: string
  ) => {
    setDashboardLoading(true);
    setDashboardError("");

    try {
      const response = await fetch(
        `${API_URL}/student/${encodeURIComponent(
          name
        )}/dashboard`,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to load student data."
        );
      }

      setDashboard(data);
    } catch (error) {
      console.error(error);

      if (
        error instanceof Error &&
        (
          error.message
            .toLowerCase()
            .includes("token") ||
          error.message
            .toLowerCase()
            .includes("authenticated") ||
          error.message
            .toLowerCase()
            .includes("not authorized")
        )
      ) {
        logout();
        return;
      }

      setDashboardError(
        error instanceof Error
          ? error.message
          : "Unable to connect to the AI server."
      );
    } finally {
      setDashboardLoading(false);
    }
  };

  // ========================================
  // SEND CHAT MESSAGE
  // ========================================

  const sendMessage = async () => {
    if (
      !message.trim() ||
      loading ||
      !token
    ) {
      return;
    }

    const userMessage = message.trim();

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
      const response = await fetch(
        `${API_URL}/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
            Authorization:
              `Bearer ${token}`,
          },
          body: JSON.stringify({
            student_name: studentName,
            message: userMessage,
            context: context,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to process your message."
        );
      }

      setContext(data.context);

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

  // ========================================
  // CHAT ENTER KEY
  // ========================================

  const handleChatKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      sendMessage();
    }
  };

  // ========================================
  // AUTH ENTER KEY
  // ========================================

  const handleUsernameKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      event.preventDefault();
      passwordRef.current?.focus();
    }
  };

  const handlePasswordKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      event.preventDefault();

      if (authMode === "login") {
        handleLogin();
      } else {
        handleRegister();
      }
    }
  };

  const handleStudentIdKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      event.preventDefault();
      usernameRef.current?.focus();
    }
  };

  // ========================================
  // AUTH SCREEN
  // ========================================

  if (!token || !studentName) {
    return (
      <div className="auth-container">
        <div className="auth-background-shape shape-one" />
        <div className="auth-background-shape shape-two" />

        <div className="auth-card">

          {/* BRAND */}
          <div className="auth-brand">
            <div className="auth-logo">
              🤖
            </div>

            <div>
              <h1>Student AI</h1>
              <span>
                Academic Assistant
              </span>
            </div>
          </div>

          {/* HEADING */}
          <div className="auth-heading">
            <h2>
              {authMode === "login"
                ? "Welcome back"
                : "Create your account"}
            </h2>

            <p>
              {authMode === "login"
                ? "Sign in to access your academic dashboard."
                : "Create your account to get started with Student AI."}
            </p>
          </div>

          {/* TABS */}
          <div className="auth-tabs">
            <button
              type="button"
              className={
                authMode === "login"
                  ? "auth-tab active"
                  : "auth-tab"
              }
              onClick={() => {
                setAuthMode("login");
                setAuthError("");
                setAuthSuccess("");
                setShowPassword(false);
              }}
            >
              Login
            </button>

            <button
              type="button"
              className={
                authMode === "register"
                  ? "auth-tab active"
                  : "auth-tab"
              }
              onClick={() => {
                setAuthMode("register");
                setAuthError("");
                setAuthSuccess("");
                setShowPassword(false);
              }}
            >
              Register
            </button>
          </div>

          {/* ERROR */}
          {authError && (
            <div className="auth-message error">
              <span>⚠️</span>
              {authError}
            </div>
          )}

          {/* SUCCESS */}
          {authSuccess && (
            <div className="auth-message success">
              <span>✓</span>
              {authSuccess}
            </div>
          )}

          {/* STUDENT ID */}
          {authMode === "register" && (
            <div className="form-group">
              <label htmlFor="student-id">
                Student ID
              </label>

              <div className="input-wrapper">
                <span>🎓</span>

                <input
                  id="student-id"
                  ref={studentIdRef}
                  type="number"
                  placeholder="Enter your student ID"
                  value={studentId}
                  onChange={(event) =>
                    setStudentId(
                      event.target.value
                    )
                  }
                  onKeyDown={
                    handleStudentIdKeyDown
                  }
                  disabled={authLoading}
                />
              </div>
            </div>
          )}

          {/* USERNAME */}
          <div className="form-group">
            <label htmlFor="username">
              Username
            </label>

            <div className="input-wrapper">
              <span>👤</span>

              <input
                id="username"
                ref={usernameRef}
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(event) =>
                  setUsername(
                    event.target.value
                  )
                }
                onKeyDown={
                  handleUsernameKeyDown
                }
                autoComplete="username"
                disabled={authLoading}
              />
            </div>
          </div>

          {/* PASSWORD */}
          <div className="form-group">
            <label htmlFor="password">
              Password
            </label>

            <div className="input-wrapper password-wrapper">
              <span>🔒</span>

              <input
                id="password"
                ref={passwordRef}
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                placeholder="Enter your password"
                value={password}
                onChange={(event) =>
                  setPassword(
                    event.target.value
                  )
                }
                onKeyDown={
                  handlePasswordKeyDown
                }
                autoComplete={
                  authMode === "login"
                    ? "current-password"
                    : "new-password"
                }
                disabled={authLoading}
              />

              {/* SHOW / HIDE PASSWORD */}
              <button
                type="button"
                className="password-toggle"
                onClick={() =>
                  setShowPassword(
                    (prev) => !prev
                  )
                }
                aria-label={
                  showPassword
                    ? "Hide password"
                    : "Show password"
                }
                disabled={authLoading}
              >
                {showPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>

          {/* SUBMIT */}
          <button
            type="button"
            className="auth-submit"
            onClick={
              authMode === "login"
                ? handleLogin
                : handleRegister
            }
            disabled={authLoading}
          >
            {authLoading ? (
              <>
                <span className="button-spinner" />
                Please wait...
              </>
            ) : authMode === "login" ? (
              <>Sign In →</>
            ) : (
              <>Create Account →</>
            )}
          </button>

          {/* FOOTER */}
          <div className="auth-footer">
            {authMode === "login"
              ? "Don't have an account?"
              : "Already have an account?"}

            <button
              type="button"
              onClick={() => {
                setAuthMode(
                  authMode === "login"
                    ? "register"
                    : "login"
                );

                setAuthError("");
                setAuthSuccess("");
                setShowPassword(false);
              }}
            >
              {authMode === "login"
                ? "Create one"
                : "Sign in"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ========================================
  // DASHBOARD LOADING
  // ========================================

  if (
    dashboardLoading &&
    !dashboard
  ) {
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

          <div className="loading-spinner" />
        </div>
      </div>
    );
  }

  // ========================================
  // DASHBOARD ERROR
  // ========================================

  if (
    dashboardError &&
    !dashboard
  ) {
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
              if (token) {
                loadDashboard(
                  studentName,
                  token
                );
              }
            }}
          >
            Try Again
          </button>

          <button
            className="secondary-error-button"
            onClick={logout}
          >
            Sign Out
          </button>
        </div>
      </div>
    );
  }

  // ========================================
  // MAIN DASHBOARD
  // ========================================

  return (
    <div className="app-container">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">
            🤖
          </div>

          <div>
            <h2>Student AI</h2>
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
              {studentName
                .charAt(0)
                .toUpperCase()}
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
            onClick={logout}
          >
            ↩ Sign Out
          </button>

        </div>
      </aside>

      {/* MAIN */}
      <main className="dashboard">

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
              {studentName
                .charAt(0)
                .toUpperCase()}
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
            {/* STAT CARDS */}
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

                <div
                  className={
                    dashboard.risk_level
                      .toLowerCase()
                      .includes("high")
                      ? "stat-value risk-high"
                      : "stat-value risk-low"
                  }
                >
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

            {/* MAIN GRID */}
            <section className="dashboard-grid">

              {/* PERFORMANCE */}
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

              {/* AI INSIGHT */}
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

            {/* SUMMARY */}
            <section className="summary-panel">

              <div>

                <span className="summary-label">
                  YOUR ACADEMIC SUMMARY
                </span>

                <h2>
                  {dashboard.overall_trend ===
                  "Improving"
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
                  </strong>.
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

      {/* FLOATING AI */}
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

      {/* CHAT */}
      {isChatOpen && (
        <>
          <div
            className="chat-overlay"
            onClick={() =>
              setIsChatOpen(false)
            }
          />

          <aside className="chat-panel">

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

              <div ref={chatEndRef} />

            </div>

            <div className="chat-input-area">

              <input
                type="text"
                placeholder="Ask about your academics..."
                value={message}
                onChange={(event) =>
                  setMessage(
                    event.target.value
                  )
                }
                onKeyDown={handleChatKeyDown}
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