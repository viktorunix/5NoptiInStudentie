FROM debian:stable-slim
WORKDIR /app
RUN apt-get update && apt-get install -y python3 python3.13-venv python3-pip libgl1 libglib2.0-0 libasound2 && rm -rf /var/lib/apt/lists/*
COPY . .
RUN chmod +x launch.sh
CMD ["./launch.sh"]
