# Stage 1: Build React project
FROM node:14 AS build-stage

RUN mkdir -p /client

WORKDIR /client

COPY ./client/package*.json ./

RUN npm install

COPY ./client .

RUN npm run build

# Stage 2: Set up Python, Flask, and Nginect
FROM python:3.10-bullseye

WORKDIR /app

# Install Nginx and required Python packages
RUN apt-get update && apt-get install -y nginx
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set up Nginx configuration
RUN rm /etc/nginx/sites-enabled/default
COPY server/nginx.conf /etc/nginx/sites-enabled/

# Copy React build output and Flask server files
COPY --from=build-stage /client/build /app/statics
COPY server /app

# Expose port 5000
EXPOSE 5000

# Run Nginx and Flask server
CMD ["bash", "-c", "nginx && python app.py"]