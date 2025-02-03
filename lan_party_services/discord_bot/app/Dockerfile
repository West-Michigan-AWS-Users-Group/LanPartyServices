FROM --platform=linux/amd64 python:3.11-slim-bullseye

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y curl

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "bot.py"]
