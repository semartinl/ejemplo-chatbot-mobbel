FROM node:23-alpine AS build
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
# RUN npm run build

# FROM node:23-alpine
# WORKDIR /app
# COPY package.json .
# RUN npm install
# COPY --from=build /app/dist ./dist
EXPOSE 5173
CMD ["npm", "run", "dev"]
# FROM node
# WORKDIR /app
# COPY . .

# CMD ["npm","run", "dev"]


# Etapa 2: Servir la aplicación
# FROM nginx:stable-alpine AS runtime
# FROM nginx:stable-alpine
# ADD ./config/default.conf /etc/nginx/conf.d/default.conf
# COPY --from=built /app/build /var/www/app/
# EXPOSE 80
# CMD ["nginx","-g", "daemon off;"]