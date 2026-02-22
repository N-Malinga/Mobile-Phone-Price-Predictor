# Use Node.js to build the app
FROM node:22-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the React code
COPY . .

# Expose the React port
EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev"]