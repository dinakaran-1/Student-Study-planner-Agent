# 📚 Study Planner Agent

An AI-powered study planning application that creates personalized, realistic study schedules for any subject using Google Gemini, tool calling, Streamlit, and persistent memory.

## 🎯 Project Overview

Study Planner Agent is an AI agent designed to help students create structured study plans based on their subjects, available study time, preferred session length, and priority subjects.

Unlike a simple chatbot, the agent uses multiple tools to analyze subjects, build schedules, save study plans, retrieve previous plans, and remember student preferences.

The system can work with programming subjects, mathematics, science, languages, business subjects, competitive exams, certifications, interviews, and other learning goals.

## ✨ Features

- 🤖 AI-powered study planning using Google Gemini
- 📋 Personalized multi-day study schedules
- 🧠 Persistent student memory
- 💾 Save and retrieve previous study plans
- 🔧 Tool-based AI agent workflow
- ⏱️ Customizable daily study hours
- ⏰ Customizable study session duration
- ⭐ Priority subject support
- 📊 Study plan history
- 💬 Chat-based Streamlit interface
- 🔎 Agent tool execution trace
- 🔄 Revision and practice sessions
- 📚 Supports multiple subjects and learning categories

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core application and agent logic |
| Google Gemini API | AI reasoning and response generation |
| Google GenAI SDK | Communication with Gemini and function calling |
| Streamlit | Web-based user interface |
| python-dotenv | Secure API key configuration |
| JSON | Persistent storage for memory and saved plans |

## 🔧 AI Tools

The agent uses the following tools:

### 1. `analyze_subjects()`

Analyzes the student's subjects and assigns suitable study phases based on the subject category.

### 2. `build_schedule()`

Creates a concrete multi-day study schedule based on:

- Number of days
- Daily available hours
- Session duration
- Subjects
- Priority subject

### 3. `save_study_plan()`

Stores the generated study plan in persistent memory.

### 4. `get_study_history()`

Retrieves previously saved study plans and student preferences.

### 5. `remember_student_preference()`

Stores useful student preferences such as preferred session length, available study time, learning style, and preferred subjects.

## 🧠 Persistent Memory

The application stores its memory in:

`study_memory.json`

The memory system keeps track of:

- Student profile
- Available study time
- Preferred session length
- Saved study plans
- Recent chat history
- Student preferences

This allows the agent to use information from previous interactions instead of starting from scratch every time.

## 🔄 Agent Workflow

For a new study planning request, the agent can follow this workflow:

```text
Student Request
      ↓
Analyze Subjects
      ↓
Build Study Schedule
      ↓
Review Tool Results
      ↓
Save Study Plan
      ↓
Generate Final Response
