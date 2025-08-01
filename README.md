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
- *Comando*

        !bot  

💡 Bibliotecas utilizadas
- [discord.py](https://discordpy.readthedocs.io/en/stable/) (API de bots do Discord) 

- [python-dotenv](https://pypi.org/project/python-dotenv/) (Gestão de tokens e variáveis de ambiente)

- [asyncio](https://docs.python.org/3/library/asyncio.html) (tarefas agendadas como apagar post)

- [datetime](https://docs.python.org/3/library/datetime.html) (gestão de datas e marcações)

🚀 Como usar
1. Cria um servidor com canal do tipo fórum chamado lfg

2. Usa o comando `/criargrupo` ou `!criargrupo` para iniciar um novo grupo

3. Os jogadores devem escolher a role → classe → e ficam inscritos

4. Dungeon, dificuldade e data são definidas com menus intuitivos

📌 Exemplo visual

<img width="743" height="647" alt="image" src="https://github.com/user-attachments/assets/105c68fc-2541-4c56-84b6-a4290999a97b" />

5. Adicionalmente pode ser adicionado o bot num canal do discord e com o comando `/bot` ou `!bot` ele cria um post no forum lfg.
   
6. Com esta opção permite ainda ao user introduzir o tipo de stack que enventualmente poderá querer.

<img width="694" height="215" alt="image" src="https://github.com/user-attachments/assets/9c171624-367f-427e-869f-b860776d5204" />


🔐 Segurança
- *O bot respeita os limites de cada role*

- *Impede que mais do que um jogador escolha role em simultâneo*

- *Elimina interações após uso para evitar spam*

👨‍💻 Desenvolvido por
Kl3z – este projeto é open-source e pode ser adaptado para qualquer comunidade WoW.

