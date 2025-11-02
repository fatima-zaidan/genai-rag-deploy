# GenAI Assistant: 

GenAI Assistant is an AI-powered assistant system built using a **RAG (Retrieval-Augmented Generation)** architecture. It allows users to ask questions and get responses based on custom datasets. The system combines **FastAPI**, **PostgreSQL**, **Gradio**, and **Docker** for a scalable and interactive AI assistant. Data is stored in **AWS S3** and embeddings are managed using **FAISS**.

## Features
- Retrieval-Augmented Generation (RAG) pipeline for accurate answers
- Custom dataset support via AWS S3
- Embedding storage and search with FAISS
- Interactive frontend using Gradio
- RESTful API with FastAPI
- Containerized with Docker for easy deployment
- PostgreSQL for structured data management

## Tech Stack
Backend: FastAPI
Frontend: Gradio
Database: PostgreSQL
Vector Store: FAISS
Embeddings: HuggingFaceEmbeddings
Chat Model: ChatOpenAI
Deployment: Docker, Docker Compose, EC2

## Installation
Clone the repository
git clone https://github.com/fatima-zaidan/genai-assistant.git
cd genai-assistant

## Environment Variables
Create a .env file in the root directory:

OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_s3_bucket_name
DATABASE_URL=postgresql://user:password@host:port/dbname

## Install dependencies
pip install -r requirements.txt

## Running Locally
docker-compose up --build
The FastAPI backend will be available at: http://localhost:8000
The Gradio frontend will be available at: http://localhost:7860

## Deployment
EC2 + Docker
SSH into your EC2 instance
Pull your Docker image:
docker pull fatimazaidan26/genai-assistant:latest


## Folder Structure
genai-assistant/
├─ app/
│  ├─ main.py              # FastAPI app entry
│  ├─ pipeline/            # RAG pipeline logic
│  ├─ database/              # Database models
│  └─ utils/               # Helper functions
├─ Dockerfile           # Docker configuration
├─ requirements.txt
├─ docker-compose.yml
├─ README.md
└─ .env