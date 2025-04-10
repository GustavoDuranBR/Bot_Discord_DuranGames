# 🤖 Bot DuranGames - Organização e Automação para seu Servidor Discord

Bem-vindo(a) ao servidor oficial do **DuranGames**!  
Este bot foi criado especialmente para **organizar salas**, **facilitar a entrada de membros** e **automatizar funções básicas** como atribuição de cargos, controle de salas via reactions e registro de eventos do servidor.

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

### 🔹 Logs:

| Comando / Evento            | Descrição                                                                          | Como usar                                          |
|----------------------------|------------------------------------------------------------------------------------|----------------------------------------------------|
| `.setlogs #canal`           | Define o canal onde os logs serão enviados.                                         | `.setlogs #nome-do-canal`                           |
| **on_message_delete**       | Loga mensagens apagadas.                                                           | Automático (não precisa comando)                    |
| **on_message_edit**         | Loga mensagens editadas.                                                           | Automático                                          |
| **on_member_join**          | Loga entrada de novos membros.                                                     | Automático                                          |
| **on_member_remove**        | Loga membros que saem ou são expulsos.                                             | Automático                                          |
| **on_member_update**        | Loga alterações de cargos.                                                         | Automático                                          |
| **on_member_ban**           | Loga banimento de membros.                                                         | Automático                                          |
| **on_member_unban**         | Loga desbanimento de membros.                                                      | Automático                                          |

---

### 🛠️ Permissões Necessárias:

O bot precisa das seguintes permissões para funcionar corretamente:

- **Gerenciar Cargos**
- **Gerenciar Mensagens**
- **Ler Histórico de Mensagens**
- **Banir/Expulsar Membros** (para logs de ban/unban)

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

## 💡 Sugestões para os Membros:

- Verifique qual cargo automático está configurado com:

  ```bash
  .ver_auto_role
  ```

- Personalize suas funções indo até o canal **#cargos** e reagindo com o emoji desejado para ganhar cargos automaticamente!

- Para acompanhar logs e atividades do servidor, configure um canal de logs usando:

  ```bash
  .setlogs #nome-do-canal
  ```

  Depois disso, o bot registrará eventos importantes como mensagens apagadas, membros banidos, alterações de cargos, entre outros.

---

## 🚀 Bot criado e mantido por [DuranGames](https://www.youtube.com/@DuranGames).