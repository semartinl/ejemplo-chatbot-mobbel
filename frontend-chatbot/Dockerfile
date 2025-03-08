FROM node:23-alpine AS build
WORKDIR /app
COPY package.json .

# RUN rm -rf node_modules package-lock.json
RUN npm install esbuild@0.24.2 --save-dev
RUN npm install
COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev"]
