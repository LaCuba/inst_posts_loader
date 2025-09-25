FROM node:20 AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN pnpm ci
COPY . .
RUN pnpm run build


FROM nginx:1.25-alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
