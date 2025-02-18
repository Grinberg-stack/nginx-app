#!/bin/bash

# Get the desired number of replicas from the first argument (default: 3)
SCALE_COUNT=${1:-3}

# Scale the application containers up or down
echo "Scaling app to $SCALE_COUNT instances..."
docker-compose up -d --scale app=$SCALE_COUNT

# Restart the Nginx container to ensure it recognizes the updated replicas
echo "Restarting Nginx container..."
docker-compose restart nginx

echo "Scaling and Nginx restart complete!"
