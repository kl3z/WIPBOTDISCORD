# World of Warcraft Dungeon Group Bot (WoW LFG Bot)

This is a Python bot developed with discord.py, designed to automate and organize the creation of Mythic+ dungeon groups in Discord, simplifying the scheduling, sign-up, and player management process based on their roles and classes in World of Warcraft.

## Main Features

### 🎯 Group creation with interactive embed displaying:

- *Selected dungeon*

- *Keystone level (+X)*

- *Scheduled date and time*

- *Dynamic player list by role and class*

### 🧩 Role signup (Tank, Healer, DPS) with automatic limits:

- *1 Tank*

- *1 Healer*

- *3 DPS*

🧙 Class selection is only available after choosing a role, with specific icons and names for each specialization.

### ⛔ Player lock system:

- *Only one player can sign up at a time.*

- *The role selection process is blocked until the class is chosen.*

### 🏰 Dungeon and Difficulty selection via dropdown menus (SelectDropdown):

- *Configurable only once*

- *The thread title is updated with the selected dungeon and difficulty*

### 📆 Date and Time setup via Modal:

- *Ensures the groups are scheduled for future times*

## 📬 Forum channel post creation:

- *Allows threads to be created with custom names and deletes dropdowns after use*

Command:


  !bot  


## 💡 Libraries Used

- *discord.py (Discord bot API)*

- *python-dotenv (Management of tokens and environment variables)*

- *asyncio (Scheduled tasks like deleting threads)*

- *datetime (Date and time management)*

## 🚀 How to Use

- *Create a server with a forum channel named lfg*

- *Use the command /criargrupo or !criargrupo to start a new group:*

```bash
!criargrupo
```
- *Players must choose their role → class → and they are signed up*

- *Dungeon, difficulty, and date are selected through intuitive menus*

## 📌 Visual Example

<img width="743" height="647" alt="image" src="https://github.com/user-attachments/assets/105c68fc-2541-4c56-84b6-a4290999a97b" />
Additionally, the bot can be added to a channel, and using the command /bot or !bot, it creates a post in the lfg forum:

```bash
!bot
```
This option also allows the user to select the type of stack they may want:

<img width="694" height="215" alt="image" src="https://github.com/user-attachments/assets/9c171624-367f-427e-869f-b860776d5204" />
## 🔐 Security

- *The bot respects the limits for each role*

- *Prevents more than one player from selecting a role at the same time*

- *Removes interaction elements after use to avoid spam*

## 👨‍💻 Developed by
Kl3z – This project is open-source and can be adapted for any WoW community.

