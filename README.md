# Daily Report Conversion API

A FastAPI backend service that receives unstructured "Daily Site Reports" in text format, utilizes Groq's Llama-3 AI model to extract structured data, and saves the information into a SQLite database. It also provides an endpoint to generate concise daily report summaries of all recorded entries.

## Project Architecture & Flow

1. **Receive Data**: The `POST /webhook` endpoint receives raw text data.
2. **AI Extraction**: The unstructured text is sent to the Groq API (`llama-3.3-70b-versatile`) via `ai/extractor.py`. The AI model is instructed to output JSON containing key metrics: `workers`, `delay_hours`, `work_done`, and `issues`.
3. **Database Storage**: The structured JSON data is saved to a SQLite database (`test.db`) via SQLAlchemy.
4. **Retrieve & Summarize**: 
   - `GET /reports`: Retrieves all saved reports from the database.
   - `GET /summary`: Aggregates the data of all stored reports and uses the Groq AI to generate a clean, professional text summary.

## Tech Stack
- **Framework**: FastAPI
- **Database**: SQLite & SQLAlchemy (ORM)
- **AI Processing**: Groq API (Llama-3.3-70b-versatile)
- **Data Validation**: Pydantic

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Groq API Key

### 2. Installation
Create a virtual environment and install the required packages:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install fastapi uvicorn sqlalchemy groq python-dotenv pydantic
```

### 3. Environment Variables
Ensure there is a `.env` file in the root directory that contains your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Running the Application
Start the FastAPI development server using Uvicorn:
```bash
uvicorn main:app --reload
```
The application will be accessible at: `http://127.0.0.1:8000`. You can also view the interactive API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints Reference

### Health Check
- **GET `/`**
  - **Description**: Verifies that the server is running.

### Submit Report
- **POST `/webhook`**
  - **Content-Type**: `application/json`
  - **Body**: 
    ```json
    {
      "message": "We had 15 workers today. Work done: poured concrete for the foundation. No delays. Everything went smoothly."
    }
    ```
  - **Description**: Parses the unstructured text with AI, extracts metrics, and saves the structured report to the database.
  - **Response**: Returns a success message along with the saved structured data.

### Get All Reports
- **GET `/reports`**
  - **Description**: Returns an array of all site reports stored in the SQLite database.

### Generate Overall Summary
- **GET `/summary`**
  - **Description**: Aggregates all reports currently in the database and generates a short, professional AI summary of the total work done, total worker count, delays, and issues.
