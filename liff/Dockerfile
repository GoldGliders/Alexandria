FROM node:12

# copy
COPY ./app /usr/src/app

WORKDIR /usr/src/app

RUN npm install
RUN npm install -g serve
RUN npm run-script build

CMD ["serve", "-s", "build"]
