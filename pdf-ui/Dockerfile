FROM nginx:alpine
COPY src /usr/share/nginx/html
WORKDIR /usr/share/nginx/html/site/import
RUN wget https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.15/lodash.min.js
WORKDIR /usr/share/nginx/html