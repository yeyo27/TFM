# Use the official lightweight Node.js 18 image.
# https://hub.docker.com/_/node
FROM node:18-slim

# Create and change to the src directory.
WORKDIR /usr/src/app

# Copy application dependency manifests to the container image.
# A wildcard is used to ensure both package.json AND package-lock.json are copied.
COPY package*.json ./

# Install all dependencies.
RUN npm install

# Copy local code to the container image.
COPY . .

# Build the app
RUN npm run build

# Expose port
EXPOSE 3000

# Run the web service on container startup.
CMD [ "npm", "start" ]