# MongoDB Migration Guide

## Overview
The Smart Task Manager application has been migrated from **SQLite** to **MongoDB**. All SQLite code has been commented out, allowing you to easily revert if needed.

## Changes Made

### 1. Database Configuration (`app/database.py`)
- ✅ **Removed**: SQLAlchemy ORM with SQLite
- ✅ **Added**: PyMongo with MongoDB connection
- ✅ **Collections Created**:
  - `users` - User accounts with unique indexes on username and email
  - `tasks` - Task records with indexes on user_id and created_at

### 2. Models (`models/__init__.py`)
- ✅ **Removed**: SQLAlchemy ORM models
- ✅ **Added**: Pure MongoDB models using `bson.ObjectId`
- Each model has `to_dict()` and `from_dict()` methods for serialization

### 3. Services
- ✅ **task_service.py**: Converted all queries from SQLAlchemy to MongoDB find/update/delete operations
- ✅ **user_service.py**: Converted user queries to MongoDB operations

### 4. Routes
- ✅ **auth.py**: Updated to work with MongoDB document dictionaries
- ✅ **task.py**: Updated to handle MongoDB ObjectId and document-based responses

### 5. Schemas (`schemas/__init__.py`)
- ✅ **Updated**: Pydantic models to support MongoDB field mappings
- ✅ **Changed**: `id` field uses MongoDB's `_id` with alias support
- ✅ **Changed**: `user_id` from integer to string (MongoDB ObjectId)

### 6. Dependencies
- ✅ **Added**: `pymongo` and `bson` to `requirements.txt`

## Prerequisites

### Install MongoDB Locally
1. Download MongoDB Community Edition from: https://www.mongodb.com/try/download/community
2. Install and start the MongoDB server
3. Verify connection:
   ```bash
   mongo mongodb://localhost:27017/
   ```

### Environment Variables
Your `.env` file should contain:
```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=smart_task_manager
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

## Installation & Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB (if not running)
```bash
# Windows
mongod

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### 3. Run the Application
```bash
python run.py
# or
uvicorn app.main:app --reload
```

The application will:
- ✅ Connect to MongoDB at `mongodb://localhost:27017/`
- ✅ Create the `smart_task_manager` database
- ✅ Automatically create `users` and `tasks` collections with proper indexes
- ✅ Print connection status in the console

## API Usage

### Register a User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task description", "priority": "high"}'
```

## Reverting to SQLite

If you need to revert to SQLite, uncomment the SQLite code in:
1. `app/database.py` - Uncomment SQLAlchemy configuration
2. `models/__init__.py` - Uncomment SQLAlchemy models
3. `services/task_service.py` - Uncomment SQLAlchemy queries
4. `services/user_service.py` - Uncomment SQLAlchemy queries
5. `routes/auth.py` - Revert imports and function signatures
6. `routes/task.py` - Revert imports and function signatures
7. `app/main.py` - Uncomment `Base.metadata.create_all()`

## MongoDB vs SQLite Differences

| Feature | SQLite | MongoDB |
|---------|--------|---------|
| **ID Field** | Integer | ObjectId |
| **Schema** | Fixed schema | Flexible documents |
| **Foreign Keys** | Native support | Manual references |
| **Indexing** | Limited | Rich indexing options |
| **Scaling** | Single file | Distributed |
| **Transactions** | Single table | Multi-document (v4.0+) |

## Data Types & Serialization

- **MongoDB ObjectId**: Stored as string in APIs for JSON compatibility
- **Datetime**: Stored as UTC datetime in MongoDB
- **Null Values**: Supported in MongoDB (no NOT NULL constraints)

## Troubleshooting

### "Failed to connect to MongoDB"
- ✗ MongoDB server is not running
- ✓ Solution: Start MongoDB service
  ```bash
  mongod  # Windows/macOS
  ```

### "Username already registered"
- ✗ Trying to create duplicate user
- ✓ Solution: Use a different username or check MongoDB for existing users
  ```javascript
  db.users.find()
  ```

### "Collection already exists"
- ✗ Collections exist from previous runs
- ✓ Solution: This is normal; MongoDB skips collection creation if it exists

### Task not found / 404 errors
- ✗ Invalid ObjectId format
- ✓ Make sure task_id is a valid MongoDB ObjectId (24 hex characters)

## Next Steps

1. ✅ Test all API endpoints
2. ✅ Migrate existing data if needed from SQLite
3. ✅ Set up MongoDB backups
4. ✅ Configure MongoDB authentication in production
5. ✅ Consider using MongoDB Atlas for cloud deployment

## Support

For MongoDB documentation: https://docs.mongodb.com/manual/
For PyMongo documentation: https://pymongo.readthedocs.io/
