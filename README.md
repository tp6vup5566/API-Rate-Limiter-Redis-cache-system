# API-Rate-Limiter-Redis-cache-system
Designed and implemented a backend service featuring JWT authentication, per-user rate limiting via Redis atomic counters, and cache-aside optimization to improve scalability and prevent overload. Containerized with Docker to simulate production-ready deployment.

## Features

- FastAPI REST API
- Redis cache
- Three rate limiting algorithms
  - Fixed Window
  - Sliding Window
  - Token Bucket
- API Key authentication
- Logging
- Docker deployment

## Project Structure
- app
├── main.py            # FastAPI app
├── auth.py            # API key verification
├── cache.py           # Redis cache helper
├── database.py        # mock database
├── limiter.py         # fixed window rate limiter
├── rate_limiter.py    # sliding window rate limiter
├── token_bucket.py    # token bucket rate limiter
├── redis_client.py    # Redis connection
└── models.py          # Pydantic models

Dockerfile
docker-compose.yml

## Technologies Used

- Python
- FastAPI
- Redis
- Docker
- Uvicorn

## Purpose of This Project

This project was built to practice:

- FastAPI backend development
- Redis caching
- rate limiting algorithms
- Docker containerization