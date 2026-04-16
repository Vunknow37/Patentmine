
# PatentMine 

**Enterprise Intellectual Property Discovery & Analysis Platform**

PatentMine is a comprehensive platform designed to discover, track, and analyze high-value lapsed patents. It helps entrepreneurs, researchers, and enterprises identify strategic open-source intellectual property opportunities by evaluating patents using a custom Utility Scoring engine and augmenting the data with AI-driven commercial insights.

## Features

- **Advanced Patent Search**: Search through the database of lapsed patents by keywords, technology domains (e.g., Pharmaceuticals, Digital Communications, Digital Vehicles), and jurisdictions (US, EP, IN, WO).
- **Utility Scoring Engine**: Ranks patents out of 99 based on a composite score considering:
  - Citation counts (weighted)
  - Recency of lapse
  - Assignee prestige
  - Claim breadth
- **AI Executive Summaries**: Leverages LLMs to generate concise, 2-sentence commercial value propositions for technical abstracts.
- **Strategy Brief Exports**: Download detailed text briefs containing patent strategy, commercial opportunity, and technical summaries.
- **Watchlist Integration**: Add high-value patents to an email watchlist for future reference.
- **Interactive Dashboard**: Modern, light-themed, professional dashboard built with Streamlit.

## Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend API**: FastAPI (Python)
- **Database**: SQLite
- **Data Pipeline**: Custom Python scripts for data enrichment and scoring

## Project Structure

```text
patentmine/
├── api/             # FastAPI backend application
├── db/              # SQLite database storage
├── pipeline/        # Data enrichment scripts (e.g., Utility Score calculator)
├── scrapers/        # Scripts for raw patent data collection
├── ui/              # Streamlit frontend dashboard application
├── start.sh         # Main startup script for both frontend and backend
└── ...
```

## Getting Started

### Prerequisites

Ensure you have Python 3 installed on your system. The project uses standard Python libraries alongside `fastapi`, `uvicorn`, `streamlit`, and `pandas`.

### Running the Application

#### Option 1: Using the startup script (Recommended)

A convenience script is provided to launch both the backend API and the frontend dashboard simultaneously.

1. Navigate to the project root directory:
   ```bash
   cd patentmine
   ```

2. Run the startup script:
   ```bash
   ./start.sh
   ```

This script will:
- Clear any lingering processes on ports `8000` and `8501`.
- Start the FastAPI backend on `http://localhost:8000`.
- Start the Streamlit frontend on `http://localhost:8501`.
- Automatically open the dashboard in your default web browser.

#### Option 2: Running manually (Without start.sh)

If you prefer not to use the automated script, you can run the components manually in separate terminal windows.

1. **Start the Backend API:**
   Open a terminal, navigate to the project root, and run:
   ```bash
   python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```
   The API will run locally at `http://localhost:8000`.

2. **Start the Frontend Dashboard:**
   Open a separate terminal, navigate to the project root, and run:
   ```bash
   python3 -m streamlit run ui/app.py --server.port 8501
   ```
   The dashboard will run locally at `http://localhost:8501`.

### Shutting Down

To stop the application, simply press `Ctrl+C` in the terminal where `start.sh` is running. The script will securely handle terminating both the backend and frontend processes.

## API Endpoints

The FastAPI backend exposes the following key endpoints:
- `GET /patents` - Search patents by query parameters (`q`, `mode`, `domain`, `country`).
- `GET /stats` - Retrieve overall database metrics and volume per domain.
- `POST /watchlist` - Register an email alert for a specific patent ID.
