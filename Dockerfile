# Static site — nginx:alpine
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
