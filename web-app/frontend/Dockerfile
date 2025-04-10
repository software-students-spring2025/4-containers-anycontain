# 1) Build stage
FROM node:18-alpine AS build
WORKDIR /app

# Copy just package files and install deps
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of your source and build
COPY public/ public/
COPY src/    src/
RUN npm run build

# 2) Serve stage
FROM nginx:alpine
# Copy the compiled React app into nginx’s web root
COPY --from=build /app/build /usr/share/nginx/html

# (Optional) if you have a custom nginx.conf:
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
