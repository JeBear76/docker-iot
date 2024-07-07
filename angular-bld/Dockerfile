# syntax=docker/dockerfile:1
FROM nginxinc/nginx-unprivileged

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Copy the rest of the source files into the image.
COPY ./release/browser /usr/share/nginx/html

# Run the application as a non-root user.
WORKDIR /certs
COPY --chmod=777 ./certs .

EXPOSE 8080

# CMD ls -la /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
