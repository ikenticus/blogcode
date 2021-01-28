ARG NODE_VER=lts

# ----- node build -----
FROM node:${NODE_VER} AS build

# Create app directory and copy everything for build
WORKDIR /prep
COPY . .

RUN npm version ${APP_VER}
RUN npm install

CMD ["node", "app.js"]
