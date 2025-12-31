FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# O Next.js usa a porta 3000 por padrão
EXPOSE 3000

CMD ["npm", "run", "dev"]