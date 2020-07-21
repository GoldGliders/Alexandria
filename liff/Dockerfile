FROM node:12

WORKDIR /usr/src/app
RUN npm install
RUN npm install -g serve
RUN npm build

CMD ["serve", "-s", "build"]
