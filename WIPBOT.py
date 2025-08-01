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
grupo_mensagem_id = None
inscritos = {"Tank": [], "Healer": [], "DPS": []}
classes_escolhidas = {}
dungeon_escolhida = DUNGEONS[2]
dificuldade_escolhida = "10"
data_formatada = "06/08/2025"
hora_escolhida = "22:00"
alteracoes_feitas = {"dungeon": False, "dificuldade": False, "data": False}
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
    def __init__(self):
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

        # Cria o post no fórum
        thread = await forum_channel.create_thread(name=escolha, content=escolha)

        # Apaga a mensagem original com a combobox
        await interaction.message.delete()

        # Evita erro de timeout
        await interaction.response.defer()





@bot.command(name="bot")
async def bot_command(ctx):
    await ctx.send(view=StackView())

class StackView(View):
    def __init__(self):
        super().__init__()
        self.add_item(StackDropdown())

CLASSES_POR_ROLE = {
    "Tank": [
        ("Protection Paladin",    "https://wow.zamimg.com/images/wow/icons/large/spell_holy_avengershield.jpg"),
        ("Protection Warrior",    "https://wow.zamimg.com/images/wow/icons/large/spell_warrior_protetion_spec.jpg"),
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
        if isinstance(interaction.channel, discord.Thread):
            await interaction.channel.edit(name=f"{dungeon_escolhida} - Key {dificuldade_escolhida}")
        
        await interaction.response.defer()

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
        if isinstance(interaction.channel, discord.Thread):
            await interaction.channel.edit(name=f"{dungeon_escolhida} - Key {dificuldade_escolhida}")
        
        await interaction.response.defer()

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
        await interaction.response.defer()
class BotaoData(Button):
    def __init__(self):
        super().__init__(label="🗓️ Definir Data", style=discord.ButtonStyle.primary)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(DataModal())
class DungeonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        if not alteracoes_feitas["dungeon"]:
            self.add_item(DungeonDropdown())
        if not alteracoes_feitas["dificuldade"]:
            self.add_item(DificuldadeDropdown())
        if not alteracoes_feitas["data"]:
            self.add_item(BotaoData())
class RoleDropdown(Select):
    def __init__(self, jogador, ctx_channel_id, role_msg_id):
        self.jogador = jogador
        self.ctx_channel_id = ctx_channel_id
        self.role_msg_id = role_msg_id
        options = []
        for role in LIMITES:
            if len(inscritos[role]) < LIMITES[role]:
                options.append(discord.SelectOption(label=role, description="Escolher esta role"))

        placeholder = "Escolhe a tua role" if options else "Todas as roles preenchidas"
        super().__init__(placeholder=placeholder, options=options, disabled=(len(options) == 0))

    async def callback(self, interaction: discord.Interaction):
        global jogador_em_progresso
        jogador = interaction.user.display_name
        if jogador_em_progresso and jogador_em_progresso != jogador:
            await interaction.response.send_message(
                f"⏳ Aguarda que {jogador_em_progresso} termine a escolha da classe.",
                ephemeral=True
            )
            return
        jogador_em_progresso = jogador
        role = self.values[0]
        for r in inscritos:
            if jogador in inscritos[r]:
                inscritos[r].remove(jogador)
        if jogador not in inscritos[role] and len(inscritos[role]) < LIMITES[role]:
            inscritos[role].append(jogador)
            canal = bot.get_channel(self.ctx_channel_id)
            if isinstance(canal, discord.Thread):
                await canal.join()
            await interaction.message.delete()
            mensagem = await canal.fetch_message(grupo_mensagem_id)
            await mensagem.edit(embed=format_grupo_embed())
            await canal.send(
                f"{jogador}, agora escolhe a tua classe para **{role}**:",
                view=ClasseView(role, jogador, self.ctx_channel_id)
            )
            await interaction.response.defer()
        else:
            jogador_em_progresso = None
            await interaction.response.send_message("❌ Esta role já está cheia ou ocorreu um erro.", ephemeral=True)
class ClasseDropdown(Select):
    def __init__(self, role, jogador):
        self.jogador = jogador
        options = [discord.SelectOption(label=nome, value=nome) for nome, _ in CLASSES_POR_ROLE[role]]
        super().__init__(placeholder=f"Escolhe a classe ({role})", options=options)
    async def callback(self, interaction: discord.Interaction):
        global jogador_em_progresso
        classes_escolhidas[self.jogador] = self.values[0]
        canal = interaction.channel
        mensagem = await canal.fetch_message(grupo_mensagem_id)
        await mensagem.edit(embed=format_grupo_embed())
        await interaction.message.delete()
        jogador_em_progresso = None
        if any(len(inscritos[r]) < LIMITES[r] for r in LIMITES):
            await canal.send(
                "Escolher a tua **Role**:",
                view=RoleView(interaction.user.display_name, canal.id, grupo_mensagem_id)
            )
        await interaction.response.defer()
class ClasseView(View):
    def __init__(self, role, jogador, ctx_channel_id):
        super().__init__()
        dropdown = ClasseDropdown(role, jogador)
        dropdown.ctx_channel_id = ctx_channel_id
        self.add_item(dropdown)
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
    if isinstance(ctx.channel, discord.Thread):
        asyncio.create_task(agendar_remocao_thread(ctx.channel, data_formatada, hora_escolhida))
    role_msg = await ctx.send(
    "Escolher a tua **Role**:",
    view=RoleView(ctx.author.display_name, ctx.channel.id, grupo_mensagem_id)
    )
class RoleView(View):
    def __init__(self, jogador, ctx_channel_id, role_msg_id):
        super().__init__(timeout=None)
        self.add_item(RoleDropdown(jogador, ctx_channel_id, role_msg_id))
@bot.event
async def on_ready():
    print(f"Bot ligado como {bot.user}")
bot.run(os.getenv("DISCORD_TOKEN"))

