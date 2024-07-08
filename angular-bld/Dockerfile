# syntax=docker/dockerfile:1
FROM nginxinc/nginx-unprivileged

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Copy the rest of the source files into the image.
COPY ./release/browser /usr/share/nginx/html

# Run the application as a non-root user.
WORKDIR /etc/ssl/certs

EXPOSE 8080
EXPOSE 4443

CMD ["nginx", "-g", "daemon off;"]
