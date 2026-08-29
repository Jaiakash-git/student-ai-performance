# 🎓 Student AI Assistant

An intelligent academic performance assistant that analyzes student marks, attendance, performance trends, academic risk, and provides personalized recommendations.

The system combines **Machine Learning, NLP, RAG, and Agent-based reasoning** to provide students with an interactive AI assistant for understanding their academic performance.

---

## 🚀 Features

### 📊 Academic Performance Analysis

* Calculate overall average marks
* Identify highest-scoring subject
* Identify lowest-scoring subject
* Analyze overall academic performance
* Analyze attendance

### 📈 Performance Trend Analysis

* Compare marks between internal examinations
* Calculate subject-wise improvement
* Identify overall performance trends
* Detect improving or declining subjects

### 🤖 Machine Learning

* Predict academic risk probability
* Classify students into risk levels
* Uses academic features such as:

  * Average marks
  * Attendance percentage
  * Highest mark
  * Lowest mark

### 🧠 NLP Intent Classification

The assistant understands different types of academic questions, including:

* Average
* Marks
* Attendance
* Highest subject
* Lowest subject
* Performance
* Risk
* Recommendation
* Trend
* Subject details
* Subject trends
* Greetings and conversational inputs

The NLP pipeline uses **TF-IDF and Logistic Regression** for intent classification.

### 🔎 RAG-Based Academic Knowledge

The system includes a Retrieval-Augmented Generation (RAG) pipeline for answering academic knowledge-based questions using retrieved contextual information.

### 🤖 Agent System

The Agent layer coordinates:

```text
User Question
      ↓
Intent Detection
      ↓
Agent Planning
      ↓
Memory / Context
      ↓
Tool Selection
      ↓
Student Data / ML / RAG
      ↓
Final Response
```

The agent also maintains conversational context such as:

* Current student
* Last intent
* Last subject
* Requested subject
* Previous result
* Last user input
* Subject context type

This allows follow-up questions such as:

```text
User: What is my lowest subject?
AI: OS is your lowest-scoring subject.

User: How much?
AI: Your mark in OS is 72.00.

User: Why?
AI: OS is your lowest-scoring subject because its mark is the lowest among your subjects.

User: How did I improve?
AI: Your mark in OS decreased by 4.00 marks.
```

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      User / UI       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Agent System      │
                    │  Planning + Memory   │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │    NLP     │    │     ML     │    │    RAG     │
      │   Intent   │    │ Risk Model │    │ Knowledge  │
      └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
                    ┌──────────────────────┐
                    │      Services        │
                    │ Marks / Attendance   │
                    │ Performance / Trend  │
                    │ Recommendation       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       MySQL DB       │
                    └──────────────────────┘
```

---

## 🛠️ Tech Stack

### Programming

* Python

### Backend

* FastAPI

### Database

* MySQL

### Machine Learning

* Scikit-learn
* Logistic Regression
* TF-IDF

### NLP

* Natural Language Processing
* Intent Classification
* TF-IDF Vectorization
* Logistic Regression

### AI

* Machine Learning
* RAG
* Agent-based architecture
* Conversational Memory

### Development Tools

* VS Code
* Git
* GitHub

---

## 📁 Project Structure

```text
Students_AI_Assistant/
│
├── agent/
│   ├── agent_core.py
│   ├── memory.py
│   └── ...
│
├── services/
│   ├── student_service.py
│   ├── attendance_service.py
│   ├── performance_service.py
│   ├── trend_service.py
│   ├── recommendation_service.py
│   └── ...
│
├── ml/
│   ├── train_model.py
│   ├── predict.py
│   └── ...
│
├── nlp/
│   ├── intent_dataset_v4.csv
│   ├── train_intent_model.py
│   └── ...
│
├── rag/
│   ├── rag_pipeline.py
│   └── ...
│
├── database.py
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 💬 Example Questions

The assistant can answer questions such as:

```text
What is my average?

What is my attendance?

What is my highest subject?

What is my lowest subject?

How much did I score in OS?

Am I performing well?

Am I at risk?

What should I improve?

What is my trend?

How did I improve in OS?

Tell me my performance and risk.
```

It also supports conversational follow-up questions using agent memory.

---

## 📊 Current ML Model

The academic risk prediction model uses:

```text
Average Marks
Attendance Percentage
Highest Mark
Lowest Mark
```

The model produces an estimated risk probability, while rule-based thresholds determine the final academic risk level.

Example:

```text
Average:       80.33
Attendance:    85.83%
Risk Level:    Low
Risk Probability: 15.39%
```

---

## 🧠 NLP Model

The NLP intent classifier is trained on a custom academic question dataset.

Current intent categories include:

```text
average
attendance
marks
highest_subject
lowest_subject
performance
risk
recommendation
trend
subject_detail
subject_trend
greeting
thanks
goodbye
```

The model uses:

```text
TF-IDF Vectorization
        +
Logistic Regression
```

---

## 🔄 Agent Memory

The Agent maintains contextual information during conversations.

Example:

```text
last_intent
last_subject
requested_subject
last_result
previous_result
last_subject_type
last_user_input
```

This enables the system to understand follow-up questions without requiring the user to repeat the subject.

---

## 🔮 Future Improvements

Planned improvements include:

* Better multi-intent question handling
* More natural follow-up understanding
* Improved conversational responses
* Complete RAG integration
* More advanced agent planning
* Authentication and user accounts
* Expanded academic knowledge base
* React frontend integration
* Improved ML model evaluation with larger datasets
* Deployment as a complete web application

---

## 👨‍💻 Project Status

**Current Status: Active Development**

The project currently includes working:

* Student data retrieval
* Academic analytics
* Attendance analysis
* Performance analysis
* Trend analysis
* ML-based risk prediction
* NLP intent classification
* Agent planning
* Conversational memory
* RAG pipeline foundation
* API/backend integration

The system is being continuously improved toward a complete AI-powered student performance platform.

---

## 📌 Purpose

This project was developed to explore how **Machine Learning, NLP, RAG, and Agentic AI** can be combined to build an intelligent academic assistant capable of analyzing student data and interacting with users conversationally.
