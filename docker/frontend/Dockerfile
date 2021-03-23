FROM node:13.12.0-alpine

WORKDIR /web-front

ENV PATH /web-front/node_modules/.bin:$PATH

COPY ./frontend_challenge/package.json .
COPY ./frontend_challenge/package-lock.json .
RUN npm install

COPY . ./frontend_challenge

