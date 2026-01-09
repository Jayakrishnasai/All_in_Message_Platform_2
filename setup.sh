#!/bin/bash

# Dailyfix Messaging Infrastructure Setup Script

set -e

echo "=========================================="
echo "Dailyfix Messaging Infrastructure Setup"
echo "=========================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose found"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "SYNAPSE_SERVER_NAME=localhost" > .env
    echo "✓ Created .env file with default server name (localhost)"
    echo "  Edit .env to set your DuckDNS domain if needed"
    echo ""
fi

# Create necessary directories
echo "Creating data directories..."
mkdir -p synapse/data
mkdir -p mautrix/data
mkdir -p backend/vector_store
echo "✓ Directories created"
echo ""

# Initialize Matrix Synapse
echo "Initializing Matrix Synapse..."
if [ ! -f synapse/data/homeserver.yaml ]; then
    echo "Generating Synapse configuration..."
    docker-compose run --rm synapse generate
    
    # Update server name in config
    if [ -f synapse/data/homeserver.yaml ]; then
        SERVER_NAME=$(grep SYNAPSE_SERVER_NAME .env | cut -d '=' -f2)
        if [ -n "$SERVER_NAME" ]; then
            echo "Updating server_name to: $SERVER_NAME"
            sed -i "s/server_name:.*/server_name: \"$SERVER_NAME\"/" synapse/data/homeserver.yaml
        fi
    fi
    echo "✓ Synapse configuration generated"
else
    echo "✓ Synapse configuration already exists"
fi
echo ""

# Start services
echo "Starting services..."
docker-compose up -d
echo "✓ Services started"
echo ""

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Create admin user
echo ""
echo "Creating admin user..."
echo "Username: admin"
echo "Password: admin123"
echo ""
docker-compose exec -T synapse register_new_matrix_user \
    -c /data/homeserver.yaml \
    -a \
    -u admin \
    -p admin123 \
    http://localhost:8008 || echo "User may already exist or service not ready yet"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Services:"
echo "  - Matrix Synapse: http://localhost:8008"
echo "  - AI Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "Next steps:"
echo "  1. Start the frontend:"
echo "     cd frontend && npm install && npm run dev"
echo ""
echo "  2. Access the app at http://localhost:3000"
echo ""
echo "  3. Login with:"
echo "     Username: admin"
echo "     Password: admin123"
echo ""
echo "  4. Test AI endpoints:"
echo "     curl http://localhost:8000/health"
echo ""
