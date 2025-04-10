FROM node:18-alpine
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code
COPY public/ public/
COPY src/    src/

# Expose the development server port (typically 3000)
EXPOSE 3000

# Start the development server with hot reloading
CMD ["npm", "start"]