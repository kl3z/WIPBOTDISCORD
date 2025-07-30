import discord
from discord.ext import commands
from discord.ui import View, Select, Button, Modal, TextInput
from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Emojis das roles
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

# Limites por role
LIMITES = {"Tank": 1, "Healer": 1, "DPS": 3}

# Estado global
grupo_mensagem_id = None
inscritos = {"Tank": [], "Healer": [], "DPS": []}
classes_escolhidas = {}
dungeon_escolhida = DUNGEONS[2]
dificuldade_escolhida = "10"
data_formatada = "06/08/2025"
hora_escolhida = "22:00"

# Controlos de alteração
alteracoes_feitas = {"dungeon": False, "dificuldade": False, "data": False}

# Embed

def format_grupo_embed():
    def format_role(role):
        players = inscritos[role]
        if not players:
            return "None"
        return "\n".join(f"{p} ({classes_escolhidas.get(p, 'sem classe')})" for p in players)

    embed = discord.Embed(
        title=f"Dungeon: {dungeon_escolhida}",
        description=(
            f"Difficulty: {dificuldade_escolhida}\n"
            f"Scheduled: {data_formatada} às {hora_escolhida}"
        ),
        color=0x00ffcc
    )
    embed.add_field(name=f"{EMOJI_TANK} Tank", value=format_role("Tank"), inline=False)
    embed.add_field(name=f"{EMOJI_HEALER} Healer", value=format_role("Healer"), inline=False)
    embed.add_field(name=f"{EMOJI_DPS} DPS", value=format_role("DPS"), inline=False)
    return embed

# Classes disponíveis por role
CLASSES_POR_ROLE = {
    "Tank": [
        ("Protection Paladin",    "https://wow.zamimg.com/images/wow/icons/large/spell_holy_avengershield.jpg"),
        ("Blood Death Knight",    "https://wow.zamimg.com/images/wow/icons/large/spell_deathknight_bloodpresence.jpg"),
        ("Vengeance Demon Hunter","https://wow.zamimg.com/images/wow/icons/large/ability_demonhunter_specdps.jpg"),
        ("Brewmaster Monk",       "https://wow.zamimg.com/images/wow/icons/large/spell_monk_brewmaster_spec.jpg"),
        ("Guardian Druid",        "https://wow.zamimg.com/images/wow/icons/large/ability_racial_bearform.jpg")
    ],
    "Healer": [
        ("Discipline Priest",     "https://wow.zamimg.com/images/wow/icons/large/spell_holy_powerwordshield.jpg"),
        ("Restoration Shaman",    "https://wow.zamimg.com/images/wow/icons/large/spell_nature_magicimmunity.jpg"),
        ("Mistweaver Monk",       "https://wow.zamimg.com/images/wow/icons/large/spell_monk_mistweaver_spec.jpg"),
        ("Restoration Druid",     "https://wow.zamimg.com/images/wow/icons/large/spell_nature_healingtouch.jpg"),
        ("Holy Paladin",          "https://wow.zamimg.com/images/wow/icons/large/spell_holy_holybolt.jpg"),
        ("Preservation Evoker",   "https://wow.zamimg.com/images/wow/icons/large/spell_spec_evoker_preservation.jpg")
    ],
    "DPS": [
        ("Arcane Mage",           "https://wow.zamimg.com/images/wow/icons/large/spell_holy_magicalsentry.jpg"),
        ("Balance Druid",         "https://wow.zamimg.com/images/wow/icons/large/spell_nature_starfall.jpg"),
        ("Unholy Death Knight",   "https://wow.zamimg.com/images/wow/icons/large/spell_deathknight_unholypresence.png"),
        ("Retribution Paladin",   "https://wow.zamimg.com/images/wow/icons/large/spell_holy_auraoflight.jpg"),
        ("Fire Mage",             "https://wow.zamimg.com/images/wow/icons/large/spell_fire_flamebolt.jpg"),
        ("Elemental Shaman",      "https://wow.zamimg.com/images/wow/icons/large/spell_nature_lightning.jpg"),
        ("Enhancement Shaman",    "https://wow.zamimg.com/images/wow/icons/large/spell_shaman_improvedstormstrike.jpg"),
        ("Marksmanship Hunter",   "https://wow.zamimg.com/images/wow/icons/large/ability_hunter_focusedaim.jpg"),
        ("Havoc Demon Hunter",    "https://wow.zamimg.com/images/wow/icons/large/ability_demonhunter_specdps.jpg"),
        ("Beast Mastery Hunter",  "https://wow.zamimg.com/images/wow/icons/large/ability_hunter_bestialdiscipline.jpg"),
        ("Assassination Rogue",   "https://wow.zamimg.com/images/wow/icons/large/ability_rogue_deadlybrew.jpg"),
        ("Outlaw Rogue",          "https://wow.zamimg.com/images/wow/icons/large/ability_rogue_waylay.jpg"),
        ("Shadow Priest",         "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_shadowwordpain.jpg"),
        ("Frost Death Knight",    "https://wow.zamimg.com/images/wow/icons/large/spell_deathknight_frostpresence.png"),
        ("Windwalker Monk",       "https://wow.zamimg.com/images/wow/icons/large/spell_monk_windwalkerspec.jpg"),
        ("Fury Warrior",          "https://wow.zamimg.com/images/wow/icons/large/ability_warrior_innerrage.jpg"),
        ("Arms Warrior",          "https://wow.zamimg.com/images/wow/icons/large/ability_warrior_savageblow.jpg"),
        ("Affliction Warlock",    "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_deathcoil.jpg"),
        ("Destruction Warlock",   "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_rainoffire.jpg"),
        ("Feral Druid",           "https://wow.zamimg.com/images/wow/icons/large/ability_druid_catform.jpg"),
        ("Devastation Evoker",    "https://wow.zamimg.com/images/wow/icons/large/spell_spec_evoker_devastation.jpg"),
        ("Survival Hunter",       "https://wow.zamimg.com/images/wow/icons/large/ability_hunter_camouflage.jpg"),
        ("Frost Mage",            "https://wow.zamimg.com/images/wow/icons/large/spell_frost_frostbolt02.jpg")
    ]
}


# Dropdown de seleção de classe
class ClasseDropdown(Select):
    def __init__(self, role, jogador):
        self.jogador = jogador
        options = [discord.SelectOption(label=nome, value=nome, description="", emoji=None) for nome, _ in CLASSES_POR_ROLE[role]]
        super().__init__(placeholder=f"Escolhe a classe ({role})", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        classes_escolhidas[self.jogador] = self.values[0]
        mensagem = await interaction.channel.fetch_message(grupo_mensagem_id)
        await mensagem.edit(embed=format_grupo_embed())
        await interaction.response.send_message(f"Classe escolhida: **{self.values[0]}**", ephemeral=True)

class ClasseView(View):
    def __init__(self, role, jogador):
        super().__init__(timeout=60)
        self.add_item(ClasseDropdown(role, jogador))

# Dropdowns principais
class DungeonDropdown(Select):
    def __init__(self):
        options = [discord.SelectOption(label=d, value=d) for d in DUNGEONS]
        super().__init__(placeholder="Escolhe a dungeon", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        global dungeon_escolhida
        if alteracoes_feitas["dungeon"]:
            await interaction.response.send_message("❌ A dungeon já foi escolhida e não pode ser alterada novamente.", ephemeral=True)
            return
        dungeon_escolhida = self.values[0]
        alteracoes_feitas["dungeon"] = True

        mensagem = await interaction.channel.fetch_message(grupo_mensagem_id)
        nova_view = DungeonView()
        if all(alteracoes_feitas.values()):
            nova_view.clear_items()
        await mensagem.edit(embed=format_grupo_embed(), view=nova_view)
        await interaction.response.send_message(f"Dungeon atualizada para **{dungeon_escolhida}**", ephemeral=True)

class DificuldadeDropdown(Select):
    def __init__(self):
        options = [discord.SelectOption(label=f"Chave {d}", value=d) for d in DIFICULDADES]
        super().__init__(placeholder="Escolhe a dificuldade", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        global dificuldade_escolhida
        if alteracoes_feitas["dificuldade"]:
            await interaction.response.send_message("❌ A dificuldade já foi definida e não pode ser alterada novamente.", ephemeral=True)
            return
        dificuldade_escolhida = self.values[0]
        alteracoes_feitas["dificuldade"] = True

        mensagem = await interaction.channel.fetch_message(grupo_mensagem_id)
        nova_view = DungeonView()
        if all(alteracoes_feitas.values()):
            nova_view.clear_items()
        await mensagem.edit(embed=format_grupo_embed(), view=nova_view)
        await interaction.response.send_message(f"Dificuldade atualizada para **+{dificuldade_escolhida}**", ephemeral=True)

# Modal de data/hora
class DataModal(Modal, title="Definir Data da Dungeon"):
    dia = TextInput(label="Dia do mês (1-31)", placeholder="Ex: 6", max_length=2)
    hora = TextInput(label="Hora (HH:MM)", placeholder="Ex: 22:30", max_length=5)

    async def on_submit(self, interaction: discord.Interaction):
        global data_formatada, hora_escolhida
        if alteracoes_feitas["data"]:
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

        except Exception:
            await interaction.response.send_message("❌ Data ou hora inválida.", ephemeral=True)
            return

        data_formatada = data_completa.strftime("%d/%m/%Y")
        hora_escolhida = hora_val
        alteracoes_feitas["data"] = True

        mensagem = await interaction.channel.fetch_message(grupo_mensagem_id)
        nova_view = DungeonView()
        if all(alteracoes_feitas.values()):
            nova_view.clear_items()
        await mensagem.edit(embed=format_grupo_embed(), view=nova_view)
        await interaction.response.send_message(f"Data agendada: **{data_formatada} às {hora_escolhida}**", ephemeral=True)

# Botão para abrir o modal
class BotaoData(Button):
    def __init__(self):
        super().__init__(label="🗓️ Definir Data", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(DataModal())

# View principal
class DungeonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        if not alteracoes_feitas["dungeon"]:
            self.add_item(DungeonDropdown())
        if not alteracoes_feitas["dificuldade"]:
            self.add_item(DificuldadeDropdown())
        if not alteracoes_feitas["data"]:
            self.add_item(BotaoData())

# Comando principal
@bot.command(name="criargrupo")
async def criar_grupo(ctx):
    global grupo_mensagem_id, inscritos, dungeon_escolhida, dificuldade_escolhida, data_formatada, hora_escolhida, alteracoes_feitas
    inscritos = {"Tank": [], "Healer": [], "DPS": []}
    classes_escolhidas.clear()
    dungeon_escolhida = DUNGEONS[2]
    dificuldade_escolhida = "10"
    data_formatada = "06/08/2025"
    hora_escolhida = "22:00"
    alteracoes_feitas = {"dungeon": False, "dificuldade": False, "data": False}

    embed = format_grupo_embed()
    mensagem = await ctx.send(embed=embed, view=DungeonView())
    grupo_mensagem_id = mensagem.id
    await mensagem.add_reaction(EMOJI_TANK)
    await mensagem.add_reaction(EMOJI_HEALER)
    await mensagem.add_reaction(EMOJI_DPS)

# Reações
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != grupo_mensagem_id or payload.user_id == bot.user.id:
        return
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is None:
        member = await guild.fetch_member(payload.user_id)
    nome = member.display_name
    emoji = str(payload.emoji)
    role = None
    if emoji == EMOJI_TANK:
        role = "Tank"
    elif emoji == EMOJI_HEALER:
        role = "Healer"
    elif emoji == EMOJI_DPS:
        role = "DPS"
    if role:
        if len(inscritos[role]) >= LIMITES[role] and nome not in inscritos[role]:
            channel = bot.get_channel(payload.channel_id)
            mensagem = await channel.fetch_message(payload.message_id)
            await mensagem.remove_reaction(emoji, member)
            return
        for r in inscritos:
            if nome in inscritos[r]:
                inscritos[r].remove(nome)
        inscritos[role].append(nome)
        channel = bot.get_channel(payload.channel_id)
        mensagem = await channel.fetch_message(payload.message_id)
        await mensagem.edit(embed=format_grupo_embed())
        if role in CLASSES_POR_ROLE:
            await channel.send(f"{member.mention}, escolhe a tua classe:", view=ClasseView(role, nome))

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != grupo_mensagem_id or payload.user_id == bot.user.id:
        return
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is None:
        member = await guild.fetch_member(payload.user_id)
    nome = member.display_name
    emoji = str(payload.emoji)
    role = None
    if emoji == EMOJI_TANK:
        role = "Tank"
    elif emoji == EMOJI_HEALER:
        role = "Healer"
    elif emoji == EMOJI_DPS:
        role = "DPS"
    if role and nome in inscritos[role]:
        inscritos[role].remove(nome)
        classes_escolhidas.pop(nome, None)
        channel = bot.get_channel(payload.channel_id)
        mensagem = await channel.fetch_message(payload.message_id)
        await mensagem.edit(embed=format_grupo_embed())

@bot.event
async def on_ready():
    print(f"Bot ligado como {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))

