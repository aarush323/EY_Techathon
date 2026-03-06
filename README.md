# Automotive Predictive Maintenance AI System (EY Techathon)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![LangChain](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain)](https://github.com/langchain-ai/langgraph)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

An autonomous, multi-agent fleet health management system designed for proactive automotive maintenance. This project leverages **LangGraph** orchestration, **FastAPI** backend, and a high-performance **React** dashboard to transform raw vehicle telemetry into actionable predictive insights and automated service workflows.

---

## 🚀 Key Features

### 🤖 Autonomous AI Orchestration
- **LangGraph Multi-Agent System**: A sophisticated DAG (Directed Acyclic Graph) of AI agents that process vehicle data, perform diagnostic reasoning, and initiate remedial actions.
- **Hybrid LLM Strategy**: Utilizes specialized models for different tasks (e.g., **Phi-3 via Ollama** for data cleaning, **GPT-class models via Cerebras** for complex diagnostics).

### 📈 Predictive Intelligence
- **Cross-Fleet RCA (Root Cause Analysis)**: Detects manufacturing-level failure patterns across the entire fleet to identify systemic defects.
- **Automated Risk Scoring**: Real-time calculation of vehicle health scores based on anomalous sensor telemetry and historical failure trends.

### 🔌 Real-Time Visibility
- **Live Execution Console**: A specialized SSE (Server-Sent Events) log stream that provides "Developer-in-the-Loop" visibility into the AI's thought process during active fleet analysis.
- **Glassmorphic Dashboard**: A premium, startup-grade UI featuring real-time health trends, failure distribution analytics, and interactive fleet maps.

### 📅 Service & Outreach Orchestration
- **Deterministic Appointment Booking**: Automatically identifies the nearest service center and schedules technicians based on specialization and availability.
- **Automated Customer Engagement**: Generates personalized outreach messages for vehicle owners, simulating real-world notifications.

---

## 🛠 Tech Stack

### Backend & AI
- **Python 3.12**: Core logic and data processing.
- **FastAPI**: High-performance REST API and SSE log streaming.
- **LangGraph**: Sophisticated agent state management and orchestration.
- **SQLite**: Local persistence for historical run data, failure logs, and appointments.
- **Uvicorn**: ASGI server implementation.

### Frontend
- **React 18 + Vite**: Lightning-fast UI development and HMR.
- **Tailwind CSS**: Utility-first styling with a custom modern design system.
- **Shadcn/UI**: Premium UI component primitives.
- **Framer Motion**: Smooth, high-fidelity micro-animations and page transitions.
- **Lucide React**: Modern, consistent iconography.

---

## 🏗 System Architecture

The system is split into two core layers:

1.  **Orchestration Layer (LangGraph)**:
    - **Data Analysis Node**: Cleans and validates telemetry sensor data.
    - **Medical Diagnosis Node**: Performs AI-driven root cause identification for predicted failures.
    - **Engagement Node**: Composes customer outreach messages.
    - **Service Node**: Handles appointment logistics and technician matching.
    - **Manufacturing Node**: Aggregates fleet-wide patterns for cross-run insights.

2.  **Infrastructure Layer (FastAPI & SQLite)**:
    - Acts as the bridge between the AI's autonomous runs and the persistent storage.
    - Manages a unified `get_db()` singleton pattern to ensure data consistency across the pipeline and API.

---

## 🚦 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- Ollama (for local LLM execution)

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd EY_LAtest_theres_hope
   ```

2. **Backend Setup**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd dashboard/client
   npm install
   ```

### Running the System

1. **Start the Backend**
   ```bash
   python main.py
   ```

2. **Start the Frontend**
   ```bash
   cd dashboard/client
   npm run dev
   ```

3. **Access the Application**
   - Open [http://localhost:5173](http://localhost:5173) in your browser.
   - Navigate to **Agent Control** and click **Run Fleet Analysis** to trigger the autonomous pipeline.

---

## 📂 Project Structure

```text
├── app/                  # FastAPI Backend & Core Logic
│   ├── api.py            # REST API Endpoints & SSE Streaming
│   ├── database.py       # SQLite Persistence (Singleton Pattern)
│   ├── pipeline.py       # Orchestration Glue for LangGraph
│   └── persistence.py    # Database Writing Logic
├── dashboard/client/     # React/Vite Frontend
│   ├── src/components/   # Reusable UI & Layout Components
│   └── src/pages/        # Feature Pages (Dashboard, Control, Insights)
├── graph/                # LangGraph Implementation
│   ├── nodes.py          # AI Agent Node definitions
│   └── state.py          # Pipeline State management
├── tools/                # Specialized APIs (Telematics, Service Centers)
└── main.py               # Entry point for the Backend
```

---

## 📝 Performance Note
To optimize for demonstration purposes, the system currently defaults to processing **5-10 vehicles** per run. This can be configured in `app/pipeline.py`.

---
*Developed for the EY Techathon - Automotive Predictive Maintenance Challenge.*
