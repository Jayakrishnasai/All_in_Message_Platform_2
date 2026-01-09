#!/bin/bash

# API Testing Script for Dailyfix AI Backend

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "Testing Dailyfix AI Backend API"
echo "=========================================="
echo ""

# Health check
echo "1. Health Check"
echo "   GET $BASE_URL/health"
curl -s "$BASE_URL/health" | jq '.' || echo "Response: $(curl -s $BASE_URL/health)"
echo ""
echo ""

# Summarization
echo "2. Summarization"
echo "   POST $BASE_URL/summarize"
SAMPLE_TEXT="I had a great conversation with the customer support team today. They helped me resolve my billing issue quickly. The representative was very professional and understanding. I'm satisfied with the service and would recommend it to others."
curl -s -X POST "$BASE_URL/summarize" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$SAMPLE_TEXT\"}" | jq '.' || curl -s -X POST "$BASE_URL/summarize" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$SAMPLE_TEXT\"}"
echo ""
echo ""

# Intent Parsing
echo "3. Intent Parsing"
echo "   POST $BASE_URL/intent"
curl -s -X POST "$BASE_URL/intent" \
  -H "Content-Type: application/json" \
  -d '{"message": "I need help with my order. When will it arrive?"}' | jq '.' || curl -s -X POST "$BASE_URL/intent" \
  -H "Content-Type: application/json" \
  -d '{"message": "I need help with my order. When will it arrive?"}'
echo ""
echo ""

# Priority Ranking
echo "4. Priority Ranking"
echo "   POST $BASE_URL/priority"
curl -s -X POST "$BASE_URL/priority" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"body": "Hello", "user_id": "user1", "timestamp": 1234567890},
      {"body": "URGENT: System is down!", "user_id": "user2", "timestamp": 1234567891},
      {"body": "Thanks for the help", "user_id": "user1", "timestamp": 1234567892}
    ]
  }' | jq '.' || curl -s -X POST "$BASE_URL/priority" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"body": "Hello", "user_id": "user1", "timestamp": 1234567890},
      {"body": "URGENT: System is down!", "user_id": "user2", "timestamp": 1234567891},
      {"body": "Thanks for the help", "user_id": "user1", "timestamp": 1234567892}
    ]
  }'
echo ""
echo ""

# Daily Report
echo "5. Daily Report"
echo "   POST $BASE_URL/daily-report"
TODAY=$(date +%Y-%m-%d)
curl -s -X POST "$BASE_URL/daily-report" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"admin\",
    \"date\": \"$TODAY\",
    \"conversations\": [
      {
        \"id\": \"room1\",
        \"messages\": [
          {\"body\": \"Hello, I need help\", \"user_id\": \"user1\", \"timestamp\": 1234567890},
          {\"body\": \"Sure, how can I assist?\", \"user_id\": \"admin\", \"timestamp\": 1234567891},
          {\"body\": \"My order is delayed\", \"user_id\": \"user1\", \"timestamp\": 1234567892}
        ]
      }
    ]
  }" | jq '.' || curl -s -X POST "$BASE_URL/daily-report" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"admin\",
    \"date\": \"$TODAY\",
    \"conversations\": [
      {
        \"id\": \"room1\",
        \"messages\": [
          {\"body\": \"Hello, I need help\", \"user_id\": \"user1\", \"timestamp\": 1234567890},
          {\"body\": \"Sure, how can I assist?\", \"user_id\": \"admin\", \"timestamp\": 1234567891},
          {\"body\": \"My order is delayed\", \"user_id\": \"user1\", \"timestamp\": 1234567892}
        ]
      }
    ]
  }"
echo ""
echo ""

echo "=========================================="
echo "API Testing Complete"
echo "=========================================="
