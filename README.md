# 🤖 Bot DuranGames - Organização e Automação para seu Servidor Discord

Bem-vindo(a) ao servidor oficial do **DuranGames**!  
Este bot foi criado especialmente para **organizar salas**, **facilitar a entrada de membros** e **automatizar funções básicas** como atribuição de cargos e controle de salas via reactions.

---

## 📋 Comandos Disponíveis:

### 🔹 Reaction Roles:

| Comando                                                    | Função                                                               |
|------------------------------------------------------------|---------------------------------------------------------------------|
| `.adicionar_reaction_role <mensagem_id> <emoji> @cargo`     | Configura um Reaction Role para atribuir cargos por emoji.           |
| `.listar_reaction_roles`                                   | Lista todos os Reaction Roles configurados.                          |
| `.remover_reaction_roles @membro`                          | Remove todos os cargos de Reaction Role do usuário mencionado.       |

---

### 🔹 Auto Roles:

| Comando                       | Função                                                                 |
|-------------------------------|-----------------------------------------------------------------------|
| `.definir_auto_role @cargo`   | Define um cargo automático que será atribuído ao novo membro.         |
| `.remover_auto_role`          | Remove a configuração atual de cargo automático.                      |
| `.ver_auto_role`              | Mostra qual é o cargo automático configurado.                         |

---

### 🛠️ Permissões Necessárias:

O bot precisa das seguintes permissões para funcionar corretamente:

- **Gerenciar Cargos**
- **Gerenciar Mensagens**
- **Ler Histórico de Mensagens**

⚠️ Importante:  
O cargo do bot precisa estar **acima** dos cargos que ele irá atribuir para os membros no Discord!

---

## 🎙️ Organização das Salas do Servidor:

### **Sugestão de Categorias & Canais:**

```bash
📢・INFORMAÇÕES
├── 📜・regras
├── 📢・avisos
├── ✅・cargos          (Reaction Roles configurados)
└── 👋・boas-vindas

💬・GERAL
├── 💭・chat-geral
└── 📸・mídia-e-memes

🎮・GAMES
├── 🎮・procura-duo
├── 🎤・sala-voz-1
└── 🎤・sala-voz-2

🤖・BOT-COMANDOS
└── 🛠️・comandos-do-bot
```

---

## 💡 Sugestão para os membros:

- Use o comando:

  ```bash
  .ver_auto_role
  ```

  Para verificar qual cargo automático você receberá ao entrar no servidor.

- Quer personalizar sua função?  
  Vá até o canal **#cargos** e reaja com o emoji desejado para ganhar o cargo automaticamente!

---

## 🚀 Bot criado e mantido por [DuranGames](https://www.youtube.com/@DuranGames).