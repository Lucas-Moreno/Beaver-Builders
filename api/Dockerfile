# Étape de construction pour installer les dépendances et transpiler TypeScript
FROM node:18 AS builder

# Crée un répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copie le package.json et le package-lock.json dans le répertoire de travail
COPY package*.json ./

# Installe toutes les dépendances (y compris les devDependencies pour la construction)
RUN npm install

# Copie les fichiers de l'application dans le répertoire de travail
COPY . .

# Transpile TypeScript en JavaScript
RUN npx tsc

# Étape finale
FROM node:18

# Crée un répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copie uniquement les fichiers nécessaires depuis l'étape de construction
COPY --from=builder /usr/src/app/package*.json ./
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/dist ./dist

# Expose le port sur lequel l'application va écouter
EXPOSE 3001

# Commande de démarrage de l'application en production
CMD [ "node", "dist/index.js" ]
