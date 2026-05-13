import os
import discord
from discord.ext import commands
from discord.ui import View, Button
from dotenv import load_dotenv

# ======================================================
# LOAD ENV
# ======================================================

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError(
        "❌ TOKEN missing in .env or Railway Variables"
    )

# ======================================================
# INTENTS
# ======================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# ======================================================
# BOT SETUP
# ======================================================

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
    case_insensitive=True
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

    print("=" * 50)
    print(f"✅ Logged in as {bot.user}")
    print(f"✅ Bot ID: {bot.user.id}")
    print(f"✅ Servers: {len(bot.guilds)}")
    print("✅ Onboarding System Active")
    print("=" * 50)

    try:

        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="New Members Joining 🚀"
            )
        )

        # Persistent views
        bot.add_view(RulesView())
        bot.add_view(InterestView())

    except Exception as e:
        print(f"❌ Presence/View Error: {e}")

# ======================================================
# MEMBER JOIN EVENT
# ======================================================

@bot.event
async def on_member_join(member):

    guild = member.guild

    try:

        # Add new joiner role
        new_role = discord.utils.get(
            guild.roles,
            name=NEW_JOINER_ROLE
        )

        if new_role:
            await member.add_roles(new_role)

        # DM Welcome
        embed = discord.Embed(
            title="🚀 Welcome to the Community",
            description=(
                f"Hey {member.mention} 👋\n\n"
                "Complete onboarding:\n\n"
                "✅ Read rules\n"
                "✅ Select interests\n"
                "✅ Unlock channels\n\n"
                "Enjoy your journey 🚀"
            ),
            color=discord.Color.green()
        )

        embed.add_field(
            name="📚 Popular Topics",
            value=(
                "🛡️ Cybersecurity\n"
                "🤖 AI/ML\n"
                "💻 Programming\n"
                "🚀 Startups"
            ),
            inline=False
        )

        await member.send(embed=embed)

    except Exception as e:
        print(f"❌ Join Error: {e}")

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

        try:

            embed = discord.Embed(
                title="🎯 Choose Your Interests",
                description=(
                    "Select your interests below.\n"
                    "You can select multiple roles."
                ),
                color=discord.Color.blurple()
            )

            await interaction.response.send_message(
                embed=embed,
                view=InterestView(),
                ephemeral=True
            )

        except Exception as e:
            print(f"❌ Rules Button Error: {e}")

# ======================================================
# INTEREST VIEW
# ======================================================

class InterestView(View):

    def __init__(self):
        super().__init__(timeout=None)

    async def toggle_role(self, interaction, role_name):

        try:

            guild = interaction.guild
            member = interaction.user

            role = discord.utils.get(
                guild.roles,
                name=role_name
            )

            if role is None:
                return f"❌ Role '{role_name}' not found."

            # Remove role if already exists
            if role in member.roles:

                await member.remove_roles(role)

                return f"❌ Removed {role_name}"

            # Add role
            await member.add_roles(role)

            # Remove new joiner role
            new_joiner = discord.utils.get(
                guild.roles,
                name=NEW_JOINER_ROLE
            )

            if new_joiner and new_joiner in member.roles:
                await member.remove_roles(new_joiner)

            # Add member role
            member_role = discord.utils.get(
                guild.roles,
                name=MEMBER_ROLE
            )

            if member_role:
                await member.add_roles(member_role)

            return f"✅ Added {role_name}"

        except Exception as e:

            print(f"❌ Role Toggle Error: {e}")

            return "⚠️ Something went wrong."

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

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):

        return await ctx.send(
            "❌ Unknown command."
        )

    elif isinstance(error, commands.MissingPermissions):

        return await ctx.send(
            "❌ Missing permissions."
        )

    else:

        print(f"❌ Command Error: {error}")

# ======================================================
# RUN BOT
# ======================================================

try:

    bot.run(TOKEN)

except discord.LoginFailure:

    print("❌ Invalid Discord Token")

except Exception as e:

    print(f"❌ Fatal Error: {e}")
