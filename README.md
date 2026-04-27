# Park Easy - A Vehicle Parking App

## Technologies Used

| Area         | Technology                                                                                             |
|--------------|--------------------------------------------------------------------------------------------------------|
| **Backend**  | Python, Flask, Flask-RESTful, Flask-JWT-Extended, Flask-Caching, SQLAlchemy, Celery, Redis |
| **Frontend** | Vue.js 3, Vite, Vue Router, Chart.js, Bootstrap 5                                    |
| **Database** | SQLite with SQLAlchemy ORM                             |

---

## Project Setup

### Prerequisites
- Python 3.8+
- Node.js 18+ and npm
- Redis Server (for caching and Celery message broker)

### Backend Setup

1.  **Clone the repository:**
    ```sh
    https://github.com/yuzikage/park-easy.git
    cd park-easy
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    *(Note: A `requirements.txt` file should be generated using `pip freeze > requirements.txt`)*
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure Environment:**
    - Ensure your Redis server is running.
    - Update the configuration with your database URI, mail server settings, etc.

5.  **Run the Backend Services:**
    - **Navigate to the backend folder:**
      ```sh
      cd backend
      ```
    - **Run Flask Application:**
      ```sh
      python main.py
      ```
    - **Celery Worker (for background tasks):**
      ```sh
      celery -A main.celery worker -l info
      ```
    - **Celery Beat (for scheduled tasks):**
      ```sh
      celery -A main.celery beat -l info
      ```

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```sh
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```sh
    npm install
    ```

3.  **Run the development server:**
    ```sh
    npm run dev
    ```

4.  **Access the application:**
    Open your browser and navigate to the URL provided by Vite (usually `http://localhost:5173`). The frontend is configured to proxy API requests to the Flask backend running on `http://127.0.0.1:5000`.
