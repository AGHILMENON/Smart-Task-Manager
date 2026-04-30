# MongoDB Smart Task Manager - Quick Start

## Prerequisites
- MongoDB running on `mongodb://localhost:27017/`
- Python 3.8+
- Dependencies installed: `pip install -r requirements.txt`

## Start the Server
```bash
python run.py
```

Expected output:
```
✓ Connected to MongoDB at mongodb://localhost:27017/
✓ Database: smart_task_manager
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## API Testing with cURL

### 1. Register a New User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password_123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

Save the `access_token` for next requests.

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=secure_password_123"
```

### 3. Create a Task
Replace `YOUR_TOKEN` with the token from step 1.

```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn MongoDB",
    "description": "Complete MongoDB fundamentals course",
    "priority": "high",
    "due_date": "2024-12-31T23:59:59"
  }'
```

**Response:**
```json
{
  "title": "Learn MongoDB",
  "description": "Complete MongoDB fundamentals course",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59",
  "id": "507f1f77bcf86cd799439011",
  "completed": false,
  "user_id": "507f1f77bcf86cd799439010",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### 4. Get All Your Tasks
```bash
curl -X GET "http://localhost:8000/tasks/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. Get a Specific Task
Replace `TASK_ID` with the id from the create response.

```bash
curl -X GET "http://localhost:8000/tasks/TASK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 6. Update a Task
```bash
curl -X PUT "http://localhost:8000/tasks/TASK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn MongoDB Advanced",
    "completed": true,
    "priority": "medium"
  }'
```

### 7. Delete a Task
```bash
curl -X DELETE "http://localhost:8000/tasks/TASK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 8. Get Task Suggestions (AI)
```bash
curl -X POST "http://localhost:8000/tasks/ai/suggest/TASK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 9. Generate Task from Description (AI)
```bash
curl -X POST "http://localhost:8000/tasks/ai/generate?description=Review%20pull%20requests%20for%20the%20new%20feature" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Check MongoDB Directly

```bash
# Connect to MongoDB
mongo mongodb://localhost:27017/smart_task_manager

# View all users
db.users.find()

# View all tasks
db.tasks.find()

# View indexes
db.users.getIndexes()
db.tasks.getIndexes()
```

## MongoDB Data Structure

### Users Collection
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439010"),
  "username": "john_doe",
  "email": "john@example.com",
  "hashed_password": "$2b$12...",
  "is_active": true,
  "created_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Tasks Collection
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "title": "Learn MongoDB",
  "description": "Complete MongoDB fundamentals course",
  "completed": false,
  "priority": "high",
  "due_date": ISODate("2024-12-31T23:59:59Z"),
  "user_id": ObjectId("507f1f77bcf86cd799439010"),
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

## Troubleshooting

### Error: "Failed to connect to MongoDB"
**Solution**: Make sure MongoDB is running
```bash
mongod  # Start MongoDB server
```

### Error: "Username already registered"
**Solution**: Use a different username or clear the users collection
```bash
mongo
use smart_task_manager
db.users.deleteMany({})
```

### Error: "Collection already exists"
**Solution**: This is normal and expected. MongoDB just skips the creation.

### How to Clear All Data
```bash
mongo
use smart_task_manager
db.users.deleteMany({})
db.tasks.deleteMany({})
```

## FastAPI Interactive Docs

Once the server is running, you can also use:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation and testing!

---

Enjoy your MongoDB-powered Smart Task Manager! 🚀
