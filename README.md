# AI Travel Studio: Multi-Agent Orchestration 🌟

AI Travel Studio is a professional-grade Multi-Agent AI Travel Planner built using **LangChain**, **LangGraph**, and **xAI (Grok)**. It orchestrates a team of specialized AI agents to transform simple natural language requests into comprehensive, high-quality travel itineraries.

![AI Travel Studio Architecture](https://raw.githubusercontent.com/Aditya-P01/Multi-Agent-System-/main/architecture_diagram.png) *(Note: Placeholder link, replace with actual image after upload)*

## 🚀 Features

- **Multi-Agent Collaboration**: 4 specialized agents (Coordinator, Activity Specialist, Logistics Expert, Lead Curator) working in sync.
- **Shared State Management**: Agents communicate via a shared context passed through a LangGraph workflow.
- **Premium UI**: Modern, glassmorphism-inspired React frontend with real-time progress tracking.
- **Lightning Fast**: Powered by xAI's Grok inference engine.
- **Structured Output**: Sophisticated parsing of natural language into structured JSON data.

## 🏗️ Architecture

The system uses a **Directed Acyclic Graph (DAG)** to manage agent execution:

1.  **Coordinator Agent**: Parses the user's intent, destination, and duration into structured JSON.
2.  **Activity Specialist**: Research and suggests high-quality tours and attractions based on user interests.
3.  **Logistics Expert**: Handles neighborhood recommendations and local transport methods.
4.  **Lead Curator**: Compiles all research into an elegant, master Markdown itinerary.

## 🛠️ Tech Stack

- **Framework**: LangChain & LangGraph
- **LLM**: xAI (Grok)
- **Backend**: FastAPI (Python)
- **Frontend**: React (Vanilla JS/Tailwind CSS)
- **State Management**: Python TypedDict

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- An xAI API Key (Get one at [console.x.ai](https://console.x.ai/))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aditya-P01/Multi-Agent-System-.git
   cd Multi--Agent-System
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   XAI_API_KEY=your_api_key_here
   ```

## 🏃 Running the Application

### Option 1: Full-Stack (Web UI)
1. Start the FastAPI server:
   ```bash
   python backend.py
   ```
2. Open your browser to `http://localhost:8000`.

### Option 2: Terminal Only
Run the agent orchestration directly in your terminal:
```bash
python multi_agent_system.py
```

## 🎥 Project Walkthrough
A detailed presentation script and walkthrough guide can be found in [walkthrough.md](./walkthrough.md).

---
Built with ❤️ for the AI Agentic Coding Assignment.

