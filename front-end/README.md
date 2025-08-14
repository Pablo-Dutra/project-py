## Guia de Uso - fast-api-front

### 1. Rodando o projeto em ambiente local

1. Instale o Node.js (recomendado versão 20 ou superior).
2. Instale as dependências do projeto:
	```cmd
	npm install
	```
3. Inicie o servidor de desenvolvimento:
	```cmd
	npm run dev
	```
4. Acesse o projeto em [http://localhost:5173](http://localhost:5173) (ou porta exibida no terminal).

---


### 2. Build da aplicação para produção

#### Build local (Node.js)
1. Gere os arquivos otimizados:
	```cmd
	npm run build
	```
2. Os arquivos finais estarão na pasta `dist/`.

#### Build da imagem Docker
1. Para criar a imagem Docker, execute:
	```cmd
	docker build --no-cache --pull --rm -f Dockerfile -t fast-api-front:latest .
	```
	- Isso irá criar a imagem `fast-api-front:latest` usando o Dockerfile do projeto.

---

### 3. Rodando com Docker e Docker Compose

1. Certifique-se de ter o Docker Desktop instalado e em execução.
2. Para subir o projeto, execute na raiz do projeto:
	```cmd
	docker-compose up --build
	```
3. Acesse a aplicação em [http://localhost:8080](http://localhost:8080).

---

#### Observações
- O Dockerfile utiliza o Nginx para servir os arquivos estáticos gerados pelo build.
- O arquivo `nginx.conf` já está configurado para SPA (Single Page Application).
- Para adicionar backend ao docker-compose, inclua o serviço desejado e ajuste as portas conforme necessário.
