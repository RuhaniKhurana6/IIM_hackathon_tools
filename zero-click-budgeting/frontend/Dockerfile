FROM node:18-alpine
WORKDIR /usr/src/app
COPY package.json package-lock.json* ./
RUN npm install || true
COPY src ./src
EXPOSE 5173
CMD ["npm", "run", "dev"]