# STAR Library - Full-Stack Project

## Project Overview

The project is a simplified dashboard for an online library, designed to be clean, scalable, and easy to use. Its primary function is to fetch data from a custom-built API and display key statistics in a responsive and visually appealing user interface.

### Core Features
- **Dynamic Dashboard:** Displays the librarys most popular author, a user's total books read, and their personal list of favourite authors.
- **Ranked Book List:** Fetches and displays a list of the most popular books, sorted by the number of unique readers.
- **RESTful API:** Backend API built with FastAPI that serves all the necessary data.
- **Custom-Styled UI:** A responsive user interface built with React and styled with CSS Modules, custom style influenced by La Lakers' Purple and Gold.

## Technology Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite
- **Frontend:** React (with Vite)
- **Styling:** CSS 
- **Version Control:** Git

## Local Setup and Installation

To run this project on your local machine, please follow the instructions guide below.

### Prerequisites

- Python 3.9+
- Node.js 18+ and npm


### 1. Backend Setup

First, set up and run the backend server.

1.  **Navigate to the backend directory:**
    
    cd backend
    

2.  **Create and activate a Python virtual environment:**
    
   *   On **macOS / Linux** (in your terminal):
       
        python3 -m venv venv
        source venv/bin/activate

    *   On **Windows** (in Command Prompt):
       
        python -m venv venv
        venv\Scripts\activate
       

3.  **Install the required Python packages:**
    (A `requirements.txt` file is provided for this)
    
    pip install -r requirements.txt
    

4.  **Initialize and seed the database:**
    This two-step process only needs to be run once to set up the database.
    
    ## Step 1: Create the database tables

    python manage.py

    ## Step 2: Populate the tables with data

    python seed.py
    

5.  **Run the backend server:**
    
    uvicorn app.main:app --reload
    
    The backend API should now be running on `http://127.0.0.1:8000`.


### 2. Frontend Setup
Using Bash commands.
In a **new, separate terminal window**, set up and run the frontend application.

1.  **Navigate to the frontend directory:**
    
    cd frontend
  

2.  **Install the required Node packages:**
    
    npm install
    

3.  **Run the frontend development server:**
    
    npm run dev
    
    The frontend application should now be running on: `http://localhost:5173`.


Developed by Kelby Matthew.
