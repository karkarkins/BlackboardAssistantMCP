# Blackboard Assistant

**An AI-driven automation system for Blackboard Learn that scrapes, organizes, and contextualizes academic course data to enable intelligent draft generation, reminders, and task tracking.**

## 🚀 Features

**Course Scraping:** Uses Playwright MCP to log in and extract course content, assignments, discussions, and syllabi.

**Context Memory Layer:** Structures course data into JSON, preserving semester context for AI queries.

**AI Agent Integration:** Exposes Blackboard tasks through MCP tools (list_courses, list_assignments, get_course_context) for natural language interaction.

**Automation:** Supports academic workflows like draft generation, due date reminders, and progress tracking.

## 🏗️ Architecture

The system is built on a **3-layer design**:

### Data Collection (Playwright MCP)

Authenticates and navigates Blackboard.

Scrapes courses, assignments, discussions, and course content.

### Context Memory Layer

Stores structured data (JSON per course).

Preserves metadata like due dates, submission links, and references to readings.

### AI Agent Layer (MCP)

Defines MCP tools for Blackboard operations.

Enables AI agents to query memory, fetch assignments, and generate responses in context.

Blackboard → Playwright MCP Scraper → Context Memory (JSON) → MCP Agent → AI Assistant

## ⚙️ Tech Stack

Programming: Python

Automation: Playwright, asyncio

MCP Integration: Model Context Protocol (Playwright MCP server)

Data Storage: JSON-based context memory

Environment: dotenv for secrets management

## 📂 Project Structure
blackboard-assistant/
│── scraper.py              # Playwright automation (courses, assignments, discussions)
│── context_builder.py      # Context memory layer (JSON store)
│── mcp_server.py           # MCP server exposing Blackboard tools
│── draft_generator.py      # AI-driven draft generation using course context
│── .env                    # Blackboard credentials (not committed)
│── README.md               # Project documentation

## 🔧 Setup

Clone the repo:

git clone https://github.com/yourusername/blackboard-assistant.git
cd blackboard-assistant


Create a .env file:

BB_USERNAME=your_username
BB_PASSWORD=your_password
BB_LOGIN_URL=https://ncat.blackboard.com/


Install dependencies:

pip install -r requirements.txt


Run the scraper:

python scraper.py

## 🧑‍💻 Usage

Run scraper.py to collect Blackboard course data.

Context is automatically stored in context/.

MCP tools (e.g., list_courses, list_assignments) allow an AI agent to query course data.

Run draft_generator.py to create assignment drafts using stored context.

## 🔮 Future Work

Expand MCP tools for direct Blackboard submissions.

Integrate calendar sync for assignment deadlines.

Extend support beyond Blackboard to other LMS platforms.


