# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

FROM nginxinc/nginx-unprivileged

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Run the application as a non-root user.
WORKDIR /certs
COPY --chmod=777 ./certs .

# Copy the rest of the source files into the image.
COPY ./dist/browser/ /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
