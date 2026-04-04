FROM node:20-alpine

LABEL maintainer="Snayder - Abismo Criativo"
LABEL description="Agência Abismo Criativo — Dashboard + Escritório Virtual"

WORKDIR /app/agencia

# Copiar projeto
COPY . .

# Instalar servidor estático leve
RUN npm install -g serve

# Porta do dashboard
EXPOSE 3456

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s \
  CMD wget -q --spider http://localhost:3456/office.html || exit 1

# Iniciar servidor
CMD ["serve", ".", "-l", "3456"]
