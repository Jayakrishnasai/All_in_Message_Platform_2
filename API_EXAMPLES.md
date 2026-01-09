# API Examples

Complete examples for testing all AI Backend endpoints.

## Base URL
```
http://localhost:8000
```

## 1. Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

## 2. Summarization

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I had a long conversation with customer support today. They helped me resolve my billing issue. The representative was very professional and understanding. I am satisfied with the service and would recommend it to others. The process took about 30 minutes but was worth it.",
    "max_length": 100,
    "min_length": 30
  }'
```

**Response:**
```json
{
  "summary": "Customer support helped resolve a billing issue professionally. The representative was understanding and the 30-minute process was satisfactory.",
  "original_length": 45,
  "summary_length": 18,
  "compression_ratio": 0.4
}
```

## 3. Intent Parsing

```bash
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need help with my order. When will it arrive?"
  }'
```

**Response:**
```json
{
  "intent": "question",
  "confidence": 0.85,
  "entities": []
}
```

**More Examples:**
```bash
# Complaint
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "This product is broken and not working!"}'

# Order
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to purchase this item"}'

# Support
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "I need customer support assistance"}'
```

## 4. Priority Ranking

```bash
curl -X POST http://localhost:8000/priority \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "body": "Hello",
        "user_id": "user1",
        "timestamp": 1704067200000
      },
      {
        "body": "URGENT: System is down! We need immediate help!",
        "user_id": "user2",
        "timestamp": 1704067260000
      },
      {
        "body": "Thanks for the help earlier",
        "user_id": "user1",
        "timestamp": 1704067320000
      },
      {
        "body": "I have a problem with my account. It is not working properly and I need assistance urgently.",
        "user_id": "user3",
        "timestamp": 1704067380000
      }
    ]
  }'
```

**Response:**
```json
{
  "ranked_messages": [
    {
      "body": "URGENT: System is down! We need immediate help!",
      "user_id": "user2",
      "timestamp": 1704067260000,
      "priority_score": 8.5
    },
    {
      "body": "I have a problem with my account. It is not working properly and I need assistance urgently.",
      "user_id": "user3",
      "timestamp": 1704067380000,
      "priority_score": 6.2
    },
    {
      "body": "Hello",
      "user_id": "user1",
      "timestamp": 1704067200000,
      "priority_score": 1.0
    },
    {
      "body": "Thanks for the help earlier",
      "user_id": "user1",
      "timestamp": 1704067320000,
      "priority_score": 0.8
    }
  ]
}
```

## 5. Vector Storage

```bash
curl -X POST http://localhost:8000/vector/store \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_123",
    "messages": [
      {
        "id": "msg_1",
        "body": "Hello, I need help with my order",
        "user_id": "user1",
        "timestamp": 1704067200000
      },
      {
        "id": "msg_2",
        "body": "Sure, I can help you with that. What is your order number?",
        "user_id": "support",
        "timestamp": 1704067260000
      },
      {
        "id": "msg_3",
        "body": "My order number is ORD-12345",
        "user_id": "user1",
        "timestamp": 1704067320000
      }
    ],
    "metadata": {
      "date": "2024-01-01",
      "category": "support"
    }
  }'
```

**Response:**
```json
{
  "status": "success",
  "conversation_id": "conv_123",
  "messages_stored": 3
}
```

## 6. Vector Search

```bash
curl -X POST http://localhost:8000/vector/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "order help",
    "top_k": 5
  }'
```

**Response:**
```json
{
  "results": [
    {
      "conversation_id": "conv_123",
      "message_id": "msg_1",
      "body": "Hello, I need help with my order",
      "user_id": "user1",
      "timestamp": 1704067200000,
      "similarity_score": 0.9234,
      "distance": 0.0832,
      "metadata": {
        "date": "2024-01-01",
        "category": "support"
      }
    }
  ]
}
```

## 7. Daily Report

```bash
curl -X POST http://localhost:8000/daily-report \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "admin",
    "date": "2024-01-15",
    "conversations": [
      {
        "id": "room_1",
        "messages": [
          {
            "body": "Hello, I need help",
            "user_id": "user1",
            "timestamp": 1704067200000
          },
          {
            "body": "Sure, how can I assist?",
            "user_id": "admin",
            "timestamp": 1704067260000
          },
          {
            "body": "My order is delayed. This is urgent!",
            "user_id": "user1",
            "timestamp": 1704067320000
          }
        ]
      },
      {
        "id": "room_2",
        "messages": [
          {
            "body": "What is your return policy?",
            "user_id": "user2",
            "timestamp": 1704067380000
          },
          {
            "body": "We offer 30-day returns",
            "user_id": "admin",
            "timestamp": 1704067440000
          }
        ]
      }
    ]
  }'
```

**Response:**
```json
{
  "user_id": "admin",
  "date": "2024-01-15",
  "total_conversations": 2,
  "total_messages": 5,
  "summary": "Admin handled customer inquiries including an urgent order delay issue and a return policy question. Provided assistance and information.",
  "priority_messages": [
    {
      "body": "My order is delayed. This is urgent!",
      "user_id": "user1",
      "timestamp": 1704067320000,
      "priority_score": 7.5
    },
    {
      "body": "What is your return policy?",
      "user_id": "user2",
      "timestamp": 1704067380000,
      "priority_score": 2.0
    }
  ],
  "intent_distribution": {
    "question": 2,
    "complaint": 1,
    "support": 1
  },
  "key_insights": [
    "1 complaint(s) require follow-up",
    "Multiple questions detected - consider FAQ or documentation"
  ]
}
```

## Using with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Summarize
response = requests.post(
    f"{BASE_URL}/summarize",
    json={"text": "Long conversation text..."}
)
print(response.json())

# Intent
response = requests.post(
    f"{BASE_URL}/intent",
    json={"message": "I need help"}
)
print(response.json())
```

## Using with JavaScript

```javascript
const BASE_URL = 'http://localhost:8000';

// Summarize
fetch(`${BASE_URL}/summarize`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Long conversation...' })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Error Responses

All endpoints return standard error format:

```json
{
  "detail": "Error message here"
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad Request
- `500`: Internal Server Error

---

**Note**: First request to AI endpoints may take longer as models are loaded into memory.
