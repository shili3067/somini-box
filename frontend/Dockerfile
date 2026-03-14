# Build stage
FROM node:20-slim AS build-stage

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Set build-time environment variable to use relative path for API
ENV VITE_API_BASE_URL=""

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine AS production-stage

# Copy built files from build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy custom nginx configuration if needed, or use default
# We will create a simple nginx config to handle SPA routing and API proxying
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
