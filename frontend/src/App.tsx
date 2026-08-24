import { useState } from "react";
import "./App.css";

interface Message {
  sender: "user" | "ai";
  text: string;
}

function App() {
  const [studentName, setStudentName] = useState("");
  const [nameInput, setNameInput] = useState("");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const startChat = () => {
    const name = nameInput.trim();

    if (!name) {
      return;
    }

    setStudentName(name);

    setMessages([
      {
        sender: "ai",
        text: `Hello ${name}! 👋 How can I help you today?`,
      },
    ]);
  };

  const sendMessage = async () => {
    if (!message.trim() || loading) {
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
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_name: studentName,
          message: userMessage,
          context: null,
        }),
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

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
          text: "Sorry, I couldn't connect to the AI server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  };

  // ==========================================
  // STUDENT NAME SCREEN
  // ==========================================

  if (!studentName) {
    return (
      <div className="welcome-container">
        <div className="welcome-card">
          <div className="logo">🤖</div>

          <h1>Student AI Assistant</h1>

          <p className="welcome-text">
            Your personal academic assistant
          </p>

          <label>Enter your student name</label>

          <input
            type="text"
            placeholder="Enter your name"
            value={nameInput}
            onChange={(event) =>
              setNameInput(event.target.value)
            }
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                startChat();
              }
            }}
          />

          <button onClick={startChat}>
            Continue →
          </button>
        </div>
      </div>
    );
  }

  // ==========================================
  // CHAT SCREEN
  // ==========================================

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div>
          <h1>🤖 Student AI Assistant</h1>
          <p>Welcome, {studentName}! 👋</p>
        </div>
      </header>

      <main className="chat-messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message-row ${msg.sender}`}
          >
            <div className="message-bubble">
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-row ai">
            <div className="message-bubble">
              Thinking... 🤔
            </div>
          </div>
        )}
      </main>

      <div className="chat-input-area">
        <input
          type="text"
          placeholder="Ask about your marks, attendance, performance..."
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          onKeyDown={handleKeyDown}
          disabled={loading}
        />

        <button
          onClick={sendMessage}
          disabled={loading || !message.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;