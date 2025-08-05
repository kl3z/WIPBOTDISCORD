#!pip install discord.py python-dotenv
import discord
from discord.ext import commands
from discord.ui import View, Select, Button, Modal, TextInput
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()
jogador_em_progresso = None
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
EMOJI_TANK = "🛡️"
EMOJI_HEALER = "💚"
EMOJI_DPS = "⚔️"
DUNGEONS = [
    "Eco-Dome Al'dani",
    "Ara-Kara, City of Echoes",
    "The Dawnbreaker",
    "Operation: Floodgate",
    "Priory of the Sacred Flame",
    "Halls of Atonement",
    "Tazavesh, the Veiled Market: Streets of Wonder",
    "Tazavesh, the Veiled Market: So'leah's Gambit"
]
DIFICULDADES = [str(i) for i in range(0, 21)] + ["20+"]
LIMITES = {"Tank": 1, "Healer": 1, "DPS": 3}
# grupo_mensagem_id = None
# inscritos = {"Tank": [], "Healer": [], "DPS": []}
# classes_escolhidas = {}
# dungeon_escolhida = DUNGEONS[2]
# dificuldade_escolhida = "10"
# data_formatada = "06/08/2025"
# hora_escolhida = "22:00"
# alteracoes_feitas = {"dungeon": False, "dificuldade": False, "data": False}
# jogador_em_progresso = None

def format_grupo_embed():
    def format_role(role):
        players = inscritos[role]
        if not players:
            return "None"
        return "\n".join(f"{p} ({classes_escolhidas.get(p, 'sem classe')})" for p in players)

    embed = discord.Embed(
        title=f"Dungeon: {dungeon_escolhida}",
        description=(
            f"Dificuldade: {dificuldade_escolhida}\n"
            f"Marcação: {data_formatada} às {hora_escolhida}"
        ),
        color=0x00ffcc
    )
    embed.add_field(name=f"{EMOJI_TANK} Tank", value=format_role("Tank"), inline=False)
    embed.add_field(name=f"{EMOJI_HEALER} Healer", value=format_role("Healer"), inline=False)
    embed.add_field(name=f"{EMOJI_DPS} DPS", value=format_role("DPS"), inline=False)
    embed.set_footer(text="Bot created by Kl3z")
    return embed

async def criar_grupo_customizado(canal):
    global grupo_mensagem_id, inscritos, dungeon_escolhida, dificuldade_escolhida, data_formatada, hora_escolhida, alteracoes_feitas
    inscritos = {"Tank": [], "Healer": [], "DPS": []}
    classes_escolhidas.clear()
    dungeon_escolhida = DUNGEONS[2]
    dificuldade_escolhida = "10"
    data_formatada = "06/08/2025"
    hora_escolhida = "22:00"
    alteracoes_feitas = {"dungeon": False, "dificuldade": False, "data": False}
    embed = format_grupo_embed()
    mensagem = await canal.send(embed=embed, view=DungeonView())
    grupo_mensagem_id = mensagem.id
    await canal.send(
        "Escolher a tua **Role**:",
        view=RoleView("Novo jogador", canal.id, grupo_mensagem_id)
    )
class StackDropdown(Select):
    def __init__(self, grupo):
        self.grupo = grupo
        options = [
            discord.SelectOption(label="Plate Stack"),
            discord.SelectOption(label="Leather Stack"),
            discord.SelectOption(label="Mail Stack"),
            discord.SelectOption(label="Cloth Stack")
        ]
        super().__init__(placeholder="Escolhe o tipo de stack", options=options)

    async def callback(self, interaction: discord.Interaction):
        escolha = self.values[0]
        forum_channel = discord.utils.get(interaction.guild.channels, name="lfg", type=discord.ChannelType.forum)
        if not forum_channel:
            await interaction.response.send_message("❌ Canal de fórum 'lfg' não encontrado ou não é do tipo fórum.", ephemeral=True)
            return
        thread = await forum_channel.create_thread(name=escolha, content=escolha)
        await interaction.message.delete()
        await interaction.response.defer()

class StackView(View):
    def __init__(self, grupo):
        super().__init__()
        self.grupo = grupo
        self.add_item(StackDropdown(grupo))
        

@bot.command(name="bot")
async def bot_command(ctx):
    grupo_temporario = GrupoDungeon()
    await ctx.send(view=StackView(grupo_temporario))
    
    membro = discord.utils.get(ctx.guild.members, name="carlitosqt")
    if membro:
        await ctx.send(f"Parabéns {membro.mention}!")

CLASSES_POR_ROLE = {
    "Tank": [
        ("Paladin",    "https://wow.zamimg.com/images/wow/icons/large/spell_holy_avengershield.jpg"),
        ("Warrior",    "https://wow.zamimg.com/images/wow/icons/large/spell_warrior_protetion_spec.jpg"),
        ("Death Knight",    "https://wow.zamimg.com/images/wow/icons/large/spell_deathknight_bloodpresence.jpg"),
        ("Demon Hunter","https://wow.zamimg.com/images/wow/icons/large/ability_demonhunter_specdps.jpg"),
        ("Monk",       "https://wow.zamimg.com/images/wow/icons/large/spell_monk_brewmaster_spec.jpg"),
        ("Druid",        "https://wow.zamimg.com/images/wow/icons/large/ability_racial_bearform.jpg")
    ],
    "Healer": [
        ("Priest",     "https://wow.zamimg.com/images/wow/icons/large/spell_holy_powerwordshield.jpg"),
        ("Shaman",    "https://wow.zamimg.com/images/wow/icons/large/spell_nature_magicimmunity.jpg"),
        ("Monk",       "https://wow.zamimg.com/images/wow/icons/large/spell_monk_mistweaver_spec.jpg"),
        ("Druid",     "https://wow.zamimg.com/images/wow/icons/large/spell_nature_healingtouch.jpg"),
        ("Paladin",          "https://wow.zamimg.com/images/wow/icons/large/spell_holy_holybolt.jpg"),
        ("Evoker",   "https://wow.zamimg.com/images/wow/icons/large/spell_spec_evoker_preservation.jpg")
    ],
    "DPS": [
        ("Mage",           "https://wow.zamimg.com/images/wow/icons/large/spell_holy_magicalsentry.jpg"),
        ("Druid",         "https://wow.zamimg.com/images/wow/icons/large/spell_nature_starfall.jpg"),
        ("Paladin",   "https://wow.zamimg.com/images/wow/icons/large/spell_holy_auraoflight.jpg"),
        ("Shaman",      "https://wow.zamimg.com/images/wow/icons/large/spell_nature_lightning.jpg"),
        ("Hunter",  "https://wow.zamimg.com/images/wow/icons/large/ability_hunter_bestialdiscipline.jpg"),
        ("Rogue",   "https://wow.zamimg.com/images/wow/icons/large/ability_rogue_deadlybrew.jpg"),
        ("Demon Hunter","https://wow.zamimg.com/images/wow/icons/large/ability_demonhunter_specdps.jpg"),
        ("Priest",         "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_shadowwordpain.jpg"),
        ("Death Knight",    "https://wow.zamimg.com/images/wow/icons/large/spell_deathknight_frostpresence.png"),
        ("Monk",       "https://wow.zamimg.com/images/wow/icons/large/spell_monk_windwalkerspec.jpg"),
        ("Warrior",          "https://wow.zamimg.com/images/wow/icons/large/ability_warrior_innerrage.jpg"),
        ("Warlock",    "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_deathcoil.jpg"),
        ("Evoker",    "https://wow.zamimg.com/images/wow/icons/large/spell_spec_evoker_devastation.jpg")
    ]
}

class GrupoDungeon:
    def __init__(self):
        self.inscritos = {"Tank": [], "Healer": [], "DPS": []}
        self.classes_escolhidas = {}
        self.dungeon_escolhida = DUNGEONS[2]
        self.dificuldade_escolhida = "10"
        self.data_formatada = "06/08/2025"
        self.hora_escolhida = "22:00"
        self.alteracoes_feitas = {"dungeon": False, "dificuldade": False, "data": False}
        self.jogador_em_progresso = None
        self.mensagem_id = None
        self.canal_id = None
        self.thread = None

    def format_grupo_embed(self):
        def format_role(role):
            players = self.inscritos[role]
            if not players:
                return "None"
            return "\n".join(f"{p} ({self.classes_escolhidas.get(p, 'sem classe')})" for p in players)

        embed = discord.Embed(
            title=f"Dungeon: {self.dungeon_escolhida}",
            description=(
                f"Dificuldade: {self.dificuldade_escolhida}\n"
                f"Marcação: {self.data_formatada} às {self.hora_escolhida}"
            ),
            color=0x00ffcc
        )
        embed.add_field(name=f"{EMOJI_TANK} Tank", value=format_role("Tank"), inline=False)
        embed.add_field(name=f"{EMOJI_HEALER} Healer", value=format_role("Healer"), inline=False)
        embed.add_field(name=f"{EMOJI_DPS} DPS", value=format_role("DPS"), inline=False)
        embed.set_footer(text="Bot created by Kl3z")
        return embed

grupos_ativos = {}

class DungeonDropdown(Select):
    def __init__(self, grupo: GrupoDungeon):
        self.grupo = grupo
        options = [discord.SelectOption(label=d, value=d) for d in DUNGEONS]
        super().__init__(placeholder="Escolhe a dungeon", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.grupo.alteracoes_feitas["dungeon"]:
            await interaction.response.send_message("❌ A dungeon já foi escolhida e não pode ser alterada novamente.", ephemeral=True)
            return
        
        self.grupo.dungeon_escolhida = self.values[0]
        self.grupo.alteracoes_feitas["dungeon"] = True

        canal = bot.get_channel(self.grupo.canal_id)
        mensagem = await canal.fetch_message(self.grupo.mensagem_id)
        
        nova_view = DungeonView(self.grupo)
        if all(self.grupo.alteracoes_feitas.values()):
            nova_view.clear_items()
        
        await mensagem.edit(embed=self.grupo.format_grupo_embed(), view=nova_view)
        
        if self.grupo.thread:
            await self.grupo.thread.edit(name=f"{self.grupo.dungeon_escolhida} - Key {self.grupo.dificuldade_escolhida}")
        
        await interaction.response.defer()

class DificuldadeDropdown(Select):
    def __init__(self, grupo):
        self.grupo = grupo
        options = [discord.SelectOption(label=f"Chave {d}", value=d) for d in DIFICULDADES]
        super().__init__(placeholder="Escolhe a dificuldade", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.grupo.alteracoes_feitas["dificuldade"]:
            await interaction.response.send_message("❌ A dificuldade já foi definida e não pode ser alterada novamente.", ephemeral=True)
            return
        
        self.grupo.dificuldade_escolhida = self.values[0]
        self.grupo.alteracoes_feitas["dificuldade"] = True

        canal = bot.get_channel(self.grupo.canal_id)
        mensagem = await canal.fetch_message(self.grupo.mensagem_id)
        nova_view = DungeonView(self.grupo)
        if all(self.grupo.alteracoes_feitas.values()):
            nova_view.clear_items()
        
        await mensagem.edit(embed=self.grupo.format_grupo_embed(), view=nova_view)
        
        if self.grupo.thread:
            await self.grupo.thread.edit(name=f"{self.grupo.dungeon_escolhida} - Key {self.grupo.dificuldade_escolhida}")
        
        await interaction.response.defer()

class DataModal(Modal, title="Definir Data da Dungeon"):
    def __init__(self, grupo):
        super().__init__()
        self.grupo = grupo
        self.dia = TextInput(label="Dia do mês (1-31)", placeholder="Ex: 6", max_length=2)
        self.hora = TextInput(label="Hora (HH:MM)", placeholder="Ex: 22:30", max_length=5)
        self.add_item(self.dia)
        self.add_item(self.hora)

    async def on_submit(self, interaction: discord.Interaction):
        if self.grupo.alteracoes_feitas["data"]:
            await interaction.response.send_message("❌ A data e hora já foram definidas e não podem ser alteradas novamente.", ephemeral=True)
            return
        try:
            dia_num = int(self.dia.value)
            if not 1 <= dia_num <= 31:
                raise ValueError("Dia fora do intervalo")
            hora_val = datetime.strptime(self.hora.value, "%H:%M").strftime("%H:%M")

            hoje = datetime.now()
            mes = hoje.month
            ano = hoje.year
            if dia_num < hoje.day:
                mes += 1
                if mes > 12:
                    mes = 1
                    ano += 1
            data_completa = datetime(year=ano, month=mes, day=dia_num)

            self.grupo.data_formatada = data_completa.strftime("%d/%m/%Y")
            self.grupo.hora_escolhida = hora_val
            self.grupo.alteracoes_feitas["data"] = True

            canal = bot.get_channel(self.grupo.canal_id)
            mensagem = await canal.fetch_message(self.grupo.mensagem_id)
            nova_view = DungeonView(self.grupo)
            if all(self.grupo.alteracoes_feitas.values()):
                nova_view.clear_items()
            await mensagem.edit(embed=self.grupo.format_grupo_embed(), view=nova_view)
            await interaction.response.defer()

        except Exception:
            await interaction.response.send_message("❌ Data ou hora inválida.", ephemeral=True)

class BotaoData(Button):
    def __init__(self, grupo):
        super().__init__(label="🗓️ Definir Data", style=discord.ButtonStyle.primary)
        self.grupo = grupo

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(DataModal(self.grupo))

class DungeonView(View):
    def __init__(self, grupo):
        super().__init__(timeout=None)
        self.grupo = grupo
        if not self.grupo.alteracoes_feitas["dungeon"]:
            self.add_item(DungeonDropdown(self.grupo))
        if not self.grupo.alteracoes_feitas["dificuldade"]:
            self.add_item(DificuldadeDropdown(self.grupo))
        if not self.grupo.alteracoes_feitas["data"]:
            self.add_item(BotaoData(self.grupo))

class RoleDropdown(Select):
    def __init__(self, jogador, ctx_channel_id, role_msg_id, grupo):
        self.jogador = jogador
        self.ctx_channel_id = ctx_channel_id
        self.role_msg_id = role_msg_id
        self.grupo = grupo
        options = []
        for role in LIMITES:
            if len(self.grupo.inscritos[role]) < LIMITES[role]:
                options.append(discord.SelectOption(label=role, description="Escolher esta role"))

        placeholder = "Escolhe a tua role" if options else "Todas as roles preenchidas"
        super().__init__(placeholder=placeholder, options=options, disabled=(len(options) == 0))

    async def callback(self, interaction: discord.Interaction):
        if self.grupo.jogador_em_progresso and self.grupo.jogador_em_progresso != interaction.user.display_name:
            await interaction.response.send_message(
                f"⏳ Aguarda que {self.grupo.jogador_em_progresso} termine a escolha da classe.",
                ephemeral=True
            )
            return
            
        self.grupo.jogador_em_progresso = interaction.user.display_name
        role = self.values[0]
        for r in self.grupo.inscritos:
            if interaction.user.display_name in self.grupo.inscritos[r]:
                self.grupo.inscritos[r].remove(interaction.user.display_name)
        
        if interaction.user.display_name not in self.grupo.inscritos[role] and len(self.grupo.inscritos[role]) < LIMITES[role]:
            self.grupo.inscritos[role].append(interaction.user.display_name)
            canal = bot.get_channel(self.ctx_channel_id)
            
            if isinstance(canal, discord.Thread):
                await canal.join()
            
            await interaction.message.delete()
        
            mensagem = await canal.fetch_message(self.grupo.mensagem_id)
            await mensagem.edit(embed=self.grupo.format_grupo_embed())
            
            await canal.send(
                f"{interaction.user.display_name}, agora escolhe a tua classe para **{role}**:",
                view=ClasseView(role, interaction.user.display_name, self.ctx_channel_id, self.grupo)
            )
            
            await interaction.response.defer()
        else:
            self.grupo.jogador_em_progresso = None
            await interaction.response.send_message("❌ Esta role já está cheia ou ocorreu um erro.", ephemeral=True)

class ClasseDropdown(Select):
    def __init__(self, role, jogador, grupo):
        self.jogador = jogador
        self.role = role
        self.grupo = grupo
        options = [discord.SelectOption(label=nome, value=nome) for nome, _ in CLASSES_POR_ROLE[role]]
        super().__init__(placeholder=f"Escolhe a classe ({role})", options=options)

    async def callback(self, interaction: discord.Interaction):
        self.grupo.classes_escolhidas[self.jogador] = self.values[0]
        canal = interaction.channel
    
        mensagem = await canal.fetch_message(self.grupo.mensagem_id)
        await mensagem.edit(embed=self.grupo.format_grupo_embed())
        
        await interaction.message.delete()
        self.grupo.jogador_em_progresso = None
        
        if any(len(self.grupo.inscritos[r]) < LIMITES[r] for r in LIMITES):
            await canal.send(
                "Escolher a tua **Role**:",
                view=RoleView(interaction.user.display_name, canal.id, self.grupo.mensagem_id, self.grupo)
            )
        
        await interaction.response.defer()

class ClasseView(View):
    def __init__(self, role, jogador, ctx_channel_id, grupo):
        super().__init__(timeout=None)
        self.grupo = grupo
        self.add_item(ClasseDropdown(role, jogador, grupo))

import asyncio

async def agendar_remocao_thread(thread: discord.Thread, data_str: str, hora_str: str):
    try:
        alvo = datetime.strptime(f"{data_str} {hora_str}", "%d/%m/%Y %H:%M")
        agora = datetime.now()
        segundos_ate_apagar = (alvo + timedelta(minutes=30) - agora).total_seconds()

        if segundos_ate_apagar > 0:
            await asyncio.sleep(segundos_ate_apagar)
            await thread.delete()
            print(f"[INFO] Thread '{thread.name}' apagada automaticamente após 30 minutos.")
        else:
            print(f"[INFO] Tempo já passou, thread '{thread.name}' não foi agendada.")
    except Exception as e:
        print(f"[ERRO] ao agendar remoção: {e}")

@bot.command(name="criargrupo")
async def criar_grupo(ctx):
    if not (isinstance(ctx.channel, discord.ForumChannel) or 
            (isinstance(ctx.channel, discord.Thread) and 
             isinstance(ctx.channel.parent, discord.ForumChannel))):
        await ctx.send("❌ Este comando só pode ser usado em um canal de fórum ou em posts de fórum!", ephemeral=True)
        return
    forum_channel = ctx.channel if isinstance(ctx.channel, discord.ForumChannel) else ctx.channel.parent
    novo_grupo = GrupoDungeon()
    
    try:
        tags = []
        dungeon_tag = discord.utils.get(forum_channel.available_tags, name=novo_grupo.dungeon_escolhida)
        if dungeon_tag:
            tags.append(dungeon_tag)
        thread, message = await forum_channel.create_thread(
            name=f"{novo_grupo.dungeon_escolhida} - Key {novo_grupo.dificuldade_escolhida}",
            content=f"Dungeon group created by {ctx.author.mention}",
            embed=novo_grupo.format_grupo_embed(),
            view=DungeonView(novo_grupo),
            applied_tags=tags
        )
        novo_grupo.thread = thread
        novo_grupo.canal_id = thread.id
        novo_grupo.mensagem_id = message.id
        grupos_ativos[message.id] = novo_grupo
        await thread.send(
            f"{ctx.author.mention}, escolhe a tua **Role**:",
            view=RoleView(ctx.author.display_name, thread.id, message.id, novo_grupo)
        )
        asyncio.create_task(
            agendar_remocao_thread(
                thread, 
                novo_grupo.data_formatada, 
                novo_grupo.hora_escolhida
            )
        )
        if ctx.channel.id != thread.id: 
            await ctx.send(f"✅ Grupo criado com sucesso! {thread.mention}", ephemeral=True)
            
    except discord.HTTPException as e:
        await ctx.send("❌ Erro ao criar post no fórum. Verifique as permissões do bot.", ephemeral=True)
        print(f"Erro HTTP ao criar post: {e}")
    except Exception as e:
        await ctx.send("❌ Ocorreu um erro inesperado ao criar o grupo.", ephemeral=True)
        print(f"Erro ao criar grupo: {e}")
        if 'thread' in locals() and thread:  
            await thread.delete()

class RoleView(View):
    def __init__(self, jogador, ctx_channel_id, role_msg_id, grupo):
        super().__init__(timeout=None)
        self.grupo = grupo
        self.add_item(RoleDropdown(jogador, ctx_channel_id, role_msg_id, grupo))


@bot.event
async def on_ready():
    print(f"Bot ligado como {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))
