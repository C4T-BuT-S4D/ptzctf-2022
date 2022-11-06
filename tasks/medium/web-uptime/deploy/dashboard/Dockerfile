FROM node:19

WORKDIR /usr/local/app

COPY package.json package-lock.json .
RUN npm ci --only=production

COPY . .
ENV NODE_ENV="production"
CMD [ "node", "main.js" ]