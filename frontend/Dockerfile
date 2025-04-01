# Build stage
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and lock file
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --legacy-peer-deps --ignore-scripts

# Copy project files
COPY . .

# Create directory for nginx
RUN mkdir -p nginx

# Copy nginx config if it doesn't exist in the project
RUN if [ ! -f nginx/default.conf ]; then \
    echo 'server { \
    listen 80; \
    server_name localhost; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > nginx/default.conf; \
fi

# Process CSS explicitly
RUN npx tailwindcss -i ./src/styles/tailwind.css -o ./src/styles/tailwind.output.css --minify

# Build the app (ignoring TypeScript errors in development)
RUN DISABLE_ESLINT_PLUGIN=true SKIP_PREFLIGHT_CHECK=true TSC_COMPILE_ON_ERROR=true CI=true npm run build

# Production stage
FROM nginx:alpine

# Copy nginx configuration - use the one from the nginx directory
COPY --from=build /app/nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy built files from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 