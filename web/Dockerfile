FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application code
COPY eslint.config.mjs /app
COPY next.config.ts /app
COPY next-env.d.ts /app
COPY package.json /app
COPY package-lock.json /app
COPY postcss.config.mjs /app
COPY public/ /app/public
COPY src/ /app/src
COPY tailwind.config.ts /app
COPY tsconfig.json /app

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "run", "dev"]
