# Dev image: runs the Vite dev server with hot reload. (A production build comes with deployment.)
FROM node:22-slim

WORKDIR /app

# Install dependencies first so this layer is cached between code changes
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173

# --host so the server is reachable from outside the container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
