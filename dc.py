import discord
from discord.ext import commands
from discord.ui import View, Button

# ======================================================
# BOT TOKEN
# ======================================================

TOKEN = "TOKEN"

# ======================================================
# INTENTS
# ======================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ======================================================
# BOT SETUP
# ======================================================

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ======================================================
# ROLE NAMES
# ======================================================

NEW_JOINER_ROLE = "🌱 New Joiner"
MEMBER_ROLE = "✅ Member"

# ======================================================
# READY EVENT
# ======================================================

@bot.event
async def on_ready():

    print(f"✅ Logged in as {bot.user}")

    # Persistent Views
    bot.add_view(RulesView())
    bot.add_view(InterestView())

# ======================================================
# MEMBER JOIN EVENT
# ======================================================

@bot.event
async def on_member_join(member):

    guild = member.guild

    # Add New Joiner Role
    new_role = discord.utils.get(
        guild.roles,
        name=NEW_JOINER_ROLE
    )

    if new_role:
        await member.add_roles(new_role)

    # Send Welcome DM
    try:

        embed = discord.Embed(
            title="🌱 Welcome!",
            description=(
                f"Hey {member.name} 👋\n\n"
                "Welcome to the community.\n\n"
                "Please complete onboarding:\n\n"
                "✅ Read rules\n"
                "✅ Select interests\n"
                "✅ Unlock channels\n\n"
                "Enjoy 🚀"
            ),
            color=discord.Color.green()
        )

        await member.send(embed=embed)

    except:
        print("❌ Could not send DM")

# ======================================================
# RULES VIEW
# ======================================================

class RulesView(View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="✅ I Agree",
        style=discord.ButtonStyle.success,
        custom_id="agree_rules"
    )

    async def agree_button(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        embed = discord.Embed(
            title="🎯 Choose Your Interests",
            description=(
                "Select your interests below.\n"
                "You can choose multiple roles."
            ),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=InterestView(),
            ephemeral=True
        )

# ======================================================
# INTEREST VIEW
# ======================================================

class InterestView(View):

    def __init__(self):
        super().__init__(timeout=None)

    async def toggle_role(self, interaction, role_name):

        guild = interaction.guild
        member = interaction.user

        role = discord.utils.get(
            guild.roles,
            name=role_name
        )

        if role is None:
            return f"❌ Role '{role_name}' not found"

        # Remove Role if already exists
        if role in member.roles:

            await member.remove_roles(role)

            return f"❌ Removed {role_name}"

        # Add Role
        else:

            await member.add_roles(role)

        # Remove New Joiner Role
        new_joiner = discord.utils.get(
            guild.roles,
            name=NEW_JOINER_ROLE
        )

        if new_joiner and new_joiner in member.roles:
            await member.remove_roles(new_joiner)

        # Add Member Role
        member_role = discord.utils.get(
            guild.roles,
            name=MEMBER_ROLE
        )

        if member_role:
            await member.add_roles(member_role)

        return f"✅ Added {role_name}"

    # ==================================================
    # BUTTONS
    # ==================================================

    @discord.ui.button(
        label="💻 Tech",
        style=discord.ButtonStyle.primary,
        custom_id="tech_btn"
    )

    async def tech_button(self, interaction, button):

        msg = await self.toggle_role(
            interaction,
            "💻 Tech"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

    @discord.ui.button(
        label="🤖 AI/ML",
        style=discord.ButtonStyle.success,
        custom_id="ai_btn"
    )

    async def ai_button(self, interaction, button):

        msg = await self.toggle_role(
            interaction,
            "🤖 AI/ML"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

    @discord.ui.button(
        label="🛡️ Cyber Security",
        style=discord.ButtonStyle.danger,
        custom_id="cyber_btn"
    )

    async def cyber_button(self, interaction, button):

        msg = await self.toggle_role(
            interaction,
            "🛡️ Cyber Security"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

    @discord.ui.button(
        label="📈 Markets",
        style=discord.ButtonStyle.secondary,
        custom_id="market_btn"
    )

    async def market_button(self, interaction, button):

        msg = await self.toggle_role(
            interaction,
            "📈 Markets"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

    @discord.ui.button(
        label="🚀 Startups",
        style=discord.ButtonStyle.primary,
        custom_id="startup_btn"
    )

    async def startup_button(self, interaction, button):

        msg = await self.toggle_role(
            interaction,
            "🚀 Startups"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

# ======================================================
# SETUP COMMAND
# ======================================================

@bot.command()

@commands.has_permissions(administrator=True)

async def setup(ctx):

    embed = discord.Embed(
        title="📜 Community Rules",
        description=(
            "Please follow the rules:\n\n"
            "• Respect everyone\n"
            "• No spam\n"
            "• No hate speech\n"
            "• No NSFW\n"
            "• Keep discussions valuable\n"
            "• Follow Discord ToS\n\n"
            "Click below to continue."
        ),
        color=discord.Color.green()
    )

    await ctx.send(
        embed=embed,
        view=RulesView()
    )

# ======================================================
# HELP COMMAND
# ======================================================

@bot.command()

async def helpme(ctx):

    embed = discord.Embed(
        title="🤖 Bot Commands",
        description=(
            "`!setup` → Start onboarding\n"
            "`!helpme` → Show commands"
        ),
        color=discord.Color.blurple()
    )

    await ctx.send(embed=embed)

# ======================================================
# ERROR HANDLER
# ======================================================

@setup.error

async def setup_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):

        await ctx.send(
            "❌ You need Administrator permission to use this command."
        )

# ======================================================
# RUN BOT
# ======================================================

bot.run(TOKEN)
