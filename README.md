# World of Warcraft Dungeon Group Bot (WoW LFG Bot)

Este é um bot desenvolvido em Python com discord.py, desenhado para automatizar e organizar a criação de grupos de dungeons míticas+ (Mythic+) no Discord, facilitando a marcação, inscrição e gestão de jogadores segundo as suas roles e classes no World of Warcraft.

## Funcionalidades principais

🎯 Criação de Grupos com embed interativo que mostra:

- *Dungeon escolhida*

- *Nível da chave (+X)*

- *Data e hora da marcação*

- *Lista dinâmica de jogadores por role e classe*

🧩 Inscrição por Role (Tank, Healer, DPS) com limite automático:

- *1 Tank*

- *1 Healer*

- *3 DPS*

      🧙 Escolha de Classe apenas após escolher a role, com ícones e nomes específicos de cada especialização.

⛔ Sistema de bloqueio por jogador:

- *Apenas um jogador pode inscrever-se de cada vez.*

- *O processo de escolha de role é bloqueado até que a classe seja selecionada.*

🏰 Seleção de Dungeon e Dificuldade com menus suspensos (SelectDropdown)

- *Apenas configurável uma vez*

- *O título do post (thread) é atualizado com a dungeon e dificuldade*

📆 Definição de Data e Hora com Modal

- *Garante que os grupos sejam marcados para o futuro*

📬 Criação de Posts no canal de fórum

- *Permite criar threads com nomes customizados e eliminar menus após uso*

      *Comando !bot*  

💡 Tecnologias utilizadas
discord.py (API de bots do Discord)

python-dotenv (Gestão de tokens e variáveis de ambiente)

asyncio (tarefas agendadas como apagar post)

datetime (gestão de datas e marcações)

Discord UI components (botões, dropdowns, modals)

🚀 Como usar
Cria um servidor com canal do tipo fórum chamado lfg

Usa o comando /criargrupo ou !criargrupo para iniciar um novo grupo

Os jogadores devem escolher a role → classe → e ficam inscritos

Dungeon, dificuldade e data são definidas com menus intuitivos

O grupo é removido automaticamente 30 minutos após a hora da run

📌 Exemplo visual
plaintext
Copy
Edit
Dungeon: The Dawnbreaker
Dificuldade: 12
Marcação: 08/08/2025 às 21:30

🛡️ Tank
- João (Protection Paladin)

💚 Healer
- Maria (Restoration Druid)

⚔️ DPS
- Ana (Fire Mage)
- Rui (Outlaw Rogue)
- Pedro (Marksmanship Hunter)
🔐 Segurança
O bot respeita os limites de cada role

Impede que mais do que um jogador escolha role em simultâneo

Elimina interações após uso para evitar spam

👨‍💻 Desenvolvido por
Kl3z – este projeto é open-source e pode ser adaptado para qualquer comunidade WoW.

