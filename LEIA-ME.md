# Treino do Dia

App de treino que abre no treino de cada dia, com vídeos dos exercícios, cronômetro de descanso, gráficos de progresso e acompanhamento do corpo.

- **Endereço:** GitHub Pages (grátis). Funciona com o computador desligado.
- **Dados:** Firebase do Google (grátis), com login pela sua conta Google. Os dados aparecem iguais no celular e no computador.
- **Celular:** dá para instalar na tela inicial. Depois de aberto uma vez, também funciona sem internet.

São cerca de 20 minutos, uma vez só. Você vai precisar de uma conta Google e de uma conta no GitHub.

---

## Parte 1: Firebase (onde ficam seus dados)

### 1. Criar o projeto
1. Entre em <https://console.firebase.google.com> com a sua conta Google.
2. Clique em **Criar um projeto** (ou **Adicionar projeto**) e dê o nome `treino-do-dia`.
3. O Google Analytics não é necessário: pode desativar. Clique em **Criar projeto**.

### 2. Ligar o login com Google
1. No menu da esquerda, abra **Criação → Authentication** e clique em **Vamos começar**.
2. Na aba **Método de login**, escolha **Google**, clique em **Ativar**, escolha seu e-mail como e-mail de suporte e clique em **Salvar**.

### 3. Pegar a configuração do app
1. Clique na engrenagem ⚙️ ao lado de "Visão geral do projeto" e depois em **Configurações do projeto**.
2. Em **Seus apps**, clique no ícone **`</>`** (Web). Dê o apelido `treino` e clique em **Registrar app**. Não marque o Firebase Hosting.
3. Vai aparecer um bloco `const firebaseConfig = { ... }`. Copie os valores para o arquivo **`firebase-config.js`**, trocando cada `COLE_AQUI`.
   Esses valores só identificam o projeto, não são senha; pode deixá-los no GitHub sem problema.

### 4. Autorizar o endereço do app
1. Volte em **Authentication → Configurações → Domínios autorizados**.
2. Clique em **Adicionar domínio** e coloque `SEU-USUARIO.github.io`, com o seu nome de usuário do GitHub.
   `localhost` já vem autorizado, para testes no computador.

### 5. Criar o banco de dados
1. No menu, abra **Criação → Firestore Database** e clique em **Criar banco de dados**.
2. Local: **southamerica-east1 (São Paulo)**. Modo: **produção**.
3. Na aba **Regras**, apague o que estiver lá, cole o conteúdo do arquivo **`firestore.rules`** e clique em **Publicar**.
   Essas regras fazem com que só a sua conta leia e grave os seus dados.

---

## Parte 2: GitHub Pages (o endereço do app)

### 6. Subir os arquivos
1. Crie uma conta em <https://github.com>, se ainda não tiver.
2. Clique em **New repository**, use o nome `treino`, deixe **Public** e clique em **Create repository**.
3. Envie os arquivos por um destes caminhos:
   - **Pelo site:** clique em **uploading an existing file** e arraste os arquivos e a pasta `icons`, **menos** `meus-dados.json` e `treino.html`. Depois clique em **Commit changes**.
   - **Pelo terminal** (o repositório já está pronto nesta pasta):
     ```
     git remote add origin https://github.com/SEU-USUARIO/treino.git
     git push -u origin main
     ```
     Na primeira vez, abre uma janela para você entrar no GitHub.

### 7. Ligar o GitHub Pages
1. No repositório, vá em **Settings → Pages**.
2. Em **Branch**, escolha `main` e a pasta `/ (root)`, depois clique em **Save**.
3. Em 1 ou 2 minutos o endereço aparece no topo da página: `https://SEU-USUARIO.github.io/treino/`.

---

## Parte 3: Usar

### 8. Trazer seus dados atuais
1. No computador, abra o endereço do app e entre com o Google.
2. Toque no botão de conta (o bonequinho no canto de cima) e escolha **Restaurar backup**.
3. Escolha o arquivo **`meus-dados.json`**, que está nesta pasta. Ele tem seu plano, os vídeos, o perfil e o peso inicial.
4. Pronto: no celular, depois de entrar com a mesma conta Google, tudo já aparece.

### 9. Instalar no celular
- **iPhone (Safari):** abra o endereço, toque em compartilhar ⬆️ e depois em **Adicionar à Tela de Início**.
- **Android (Chrome):** abra o endereço, toque no menu ⋮ e depois em **Instalar app** (ou **Adicionar à tela inicial**).

---

## Atualizar o app depois
1. Altere os arquivos.
2. No arquivo `sw.js`, aumente o número em `const CACHE = 'treino-v1'` (por exemplo, para `treino-v2`). É isso que faz os celulares pegarem a versão nova.
3. Envie de novo para o GitHub, pelo site ou com:
   ```
   git add -A
   git commit -m "Atualiza o app"
   git push
   ```

## Backup
No botão de conta tem **Baixar backup**, que gera um arquivo com tudo: plano, treinos registrados e medidas. Vale baixar de vez em quando e guardar no Google Drive.

## Arquivos
| Arquivo | O que é |
|---|---|
| `index.html` | O app inteiro |
| `cloud.js` | Login com Google e conexão com o banco de dados |
| `firebase-config.js` | A configuração do seu projeto Firebase (passo 3) |
| `firestore.rules` | As regras que protegem seus dados (passo 5) |
| `sw.js`, `manifest.webmanifest`, `icons/` | O que faz o app ser instalável e abrir sem internet |
| `meus-dados.json` | Seus dados atuais (não vai para o GitHub) |
| `treino.html` | A versão antiga, que rodava dentro do Claude (não vai para o GitHub) |
