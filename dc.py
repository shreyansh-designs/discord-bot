import discord
from discord.ext import commands
from discord.ui import View, Button

# ==========================================
# CONFIG
# ==========================================

DISCORD_BOT_TOKEN = "DISCORD_BOT_TOKEN"

# ==========================================
# OPENAI CLIENT
# ==========================================

# ==========================================
# DISCORD BOT SETUP
# ==========================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
# ROLE NAMES
# ==========================================

NEW_JOINER_ROLE = "New Joiner"
MEMBER_ROLE = "Member"

INTEREST_ROLES = {
    "Tech": "💻 Tech",
    "AI/ML": "🤖 AI/ML",
    "Startups": "🚀 Startups",
    "Psychology": "🧠 Psychology",
    "Markets": "📈 Markets"
}

# ==========================================
# BOT READY
# ==========================================

@bot.event
async def on_ready():
    print(f"✅ Builder Guide is online as {bot.user}")

# ==========================================
# NEW MEMBER JOIN
# ==========================================

@bot.event
async def on_member_join(member):

    guild = member.guild

    # Get New Joiner role
    new_joiner_role = discord.utils.get(guild.roles, name=NEW_JOINER_ROLE)

    if new_joiner_role:
        await member.add_roles(new_joiner_role)

    # Send welcome DM
    try:
        await member.send(
            f"""
🌱 Welcome to {guild.name}!

Please complete onboarding:

1️⃣ Read the rules
2️⃣ Select your interests
3️⃣ Unlock community access

Enjoy your journey 🚀
"""
        )
    except:
        print("Could not send DM")

# ==========================================
# RULES COMMAND
# ==========================================

class RulesView(View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ I Agree", style=discord.ButtonStyle.green)
    async def agree_button(self, interaction: discord.Interaction, button: Button):

        member = interaction.user
        guild = interaction.guild

        await interaction.response.send_message(
            "✅ Rules accepted! Now select your interests below.",
            ephemeral=True
        )

        # Send interests panel
        embed = discord.Embed(
            title="🎯 Select Your Interests",
            description="Click the buttons below to unlock channels.",
            color=discord.Color.blue()
        )

        await interaction.channel.send(
            embed=embed,
            view=InterestView()
        )

# ==========================================
# INTEREST BUTTONS
# ==========================================

class InterestView(View):

    def __init__(self):
        super().__init__(timeout=None)

    async def assign_role(self, interaction, role_name):

        guild = interaction.guild
        member = interaction.user

        role = discord.utils.get(guild.roles, name=role_name)

        if role:
            await member.add_roles(role)

        # Remove New Joiner role
        new_joiner = discord.utils.get(guild.roles, name=NEW_JOINER_ROLE)

        if new_joiner in member.roles:
            await member.remove_roles(new_joiner)

        # Add Member role
        member_role = discord.utils.get(guild.roles, name=MEMBER_ROLE)

        if member_role:
            await member.add_roles(member_role)

    @discord.ui.button(label="💻 Tech", style=discord.ButtonStyle.primary)
    async def tech_button(self, interaction: discord.Interaction, button: Button):

        await self.assign_role(interaction, "💻 Tech")

        await interaction.response.send_message(
            "✅ Tech role assigned!",
            ephemeral=True
        )

    @discord.ui.button(label="🤖 AI/ML", style=discord.ButtonStyle.success)
    async def ai_button(self, interaction: discord.Interaction, button: Button):

        await self.assign_role(interaction, "🤖 AI/ML")

        await interaction.response.send_message(
            "✅ AI/ML role assigned!",
            ephemeral=True
        )

    @discord.ui.button(label="🚀 Startups", style=discord.ButtonStyle.secondary)
    async def startup_button(self, interaction: discord.Interaction, button: Button):

        await self.assign_role(interaction, "🚀 Startups")

        await interaction.response.send_message(
            "✅ Startups role assigned!",
            ephemeral=True
        )

    @discord.ui.button(label="🧠 Psychology", style=discord.ButtonStyle.danger)
    async def psychology_button(self, interaction: discord.Interaction, button: Button):

        await self.assign_role(interaction, "🧠 Psychology")

        await interaction.response.send_message(
            "✅ Psychology role assigned!",
            ephemeral=True
        )

    @discord.ui.button(label="📈 Markets", style=discord.ButtonStyle.primary)
    async def markets_button(self, interaction: discord.Interaction, button: Button):

        await self.assign_role(interaction, "📈 Markets")

        await interaction.response.send_message(
            "✅ Markets role assigned!",
            ephemeral=True
        )

# ==========================================
# SETUP COMMAND
# ==========================================

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    embed = discord.Embed(
        title="📜 Community Rules",
        description="""
Please read the rules carefully:

• Respect everyone
• No spam
• No hate speech
• Keep discussions valuable
• Follow Discord ToS

Click below to continue.
""",
        color=discord.Color.green()
    )

    await ctx.send(embed=embed, view=RulesView())

# ==========================================
# AI CHAT COMMAND
# ==========================================

@bot.command()
async def ask(ctx, *, question):

    thinking_message = await ctx.send("🤖 Thinking...")

    try:

        response = client_ai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Builder Guide, a smart and friendly Discord community assistant.
You help users with startups, AI, tech, psychology, productivity, and business discussions.
Keep answers concise and beginner friendly.
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=300
        )

        reply = response.choices[0].message.content

        await thinking_message.edit(content=reply)

    except Exception as e:
        await thinking_message.edit(content=f"❌ Error: {e}")

# ==========================================
# RUN BOT
# ==========================================

bot.run(DISCORD_BOT_TOKEN)
