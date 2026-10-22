
FROM nginx:alpine

COPY src/frontend/index.html /usr/share/nginx/html/index.html
COPY src/frontend/style.css /usr/share/nginx/html/style.css
COPY src/frontend/script.js /usr/share/nginx/html/script.js

COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
