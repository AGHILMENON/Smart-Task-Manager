# Smart Task Manager Backend

A FastAPI-based backend service for Smart Task Manager with JWT authentication and SQLite database.

## Features

- **FastAPI Framework**: High-performance, async web framework for building APIs.
- **SQLite Database**: Lightweight SQL database using SQLAlchemy ORM.
- **JWT Authentication**: Secure token-based authentication.
- **Task Management**: Full CRUD operations for tasks with user isolation.
- **Groq AI Integration**: AI-powered task management features.
- **Environment Configuration**: Secure configuration management using environment variables.

## Prerequisites

- Python 3.8+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AGHILMENON/Smart-Task-Manager.git
   cd Smart-Task-Manager
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your-secret-key-here
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   python run.py
   ```

2. Open your browser to `http://localhost:8000/docs` for the interactive API documentation.

2. Open your browser to `http://localhost:8000/docs` for the interactive API documentation.

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Tasks (requires authentication)
- `GET /tasks/` - Get all tasks for current user
- `POST /tasks/` - Create a new task
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

2. The API will be available at `http://localhost:8000`

3. Access the interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### Health Checks


## Project Structure

```
Smart-Task-Manager/

```

## Configuration

The application uses the following environment variables:



## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub.