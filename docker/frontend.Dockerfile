FROM node:20-slim

WORKDIR /app

COPY frontend/package*.json ./
RUN npm ci

COPY frontend .

EXPOSE 3000

# `next dev` instead of a production build: faster iteration during the
# hackathon build window. Swap to `next build && next start` before a real
# deploy.
CMD ["npm", "run", "dev"]
