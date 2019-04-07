FROM node:8.15.1 as dev
RUN mkdir -p /code
ENV PATH="/data/node_modules/.bin:${PATH}"

WORKDIR /code
RUN mkdir -p ../node_modules && \
  ln -s ../node_modules

ADD code/package.json .
RUN yarn install -g

CMD yarn run dev

# FROM dev as builder
# RUN yarn build --force

# FROM nginx:1.15.7-alpine
# WORKDIR /usr/share/nginx/html

# COPY --from=builder /code/dist .
# RUN find .

