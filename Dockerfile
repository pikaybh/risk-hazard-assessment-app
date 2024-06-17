FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y sqlite3 libsqlite3-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV OPENAI_API_KEY=<your_openai_api_key>
ENV LANGCHAIN_TRACING_V2=<your_langchain_tracing_v2>
ENV LANGCHAIN_API_KEY=<your_langchain_api_key>

# Create app directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the Streamlit port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py"]
