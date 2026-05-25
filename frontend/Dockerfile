FROM node:20-alpine AS lint
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run lint

FROM nginx:1.27-alpine
COPY --from=lint /app/index.html /usr/share/nginx/html/index.html

EXPOSE 80
