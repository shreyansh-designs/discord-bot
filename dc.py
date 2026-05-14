import os
import discord
from discord.ext import commands
from discord.ui import View, Button
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ TOKEN missing in .env or Railway Variables")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# ======================================================
# ROLE IDS (PUT YOUR REAL ROLE IDS HERE)
# ======================================================

TECH_ROLE_ID = 123456789012345678
AI_ROLE_ID = 123456789012345679
CYBER_ROLE_ID = 123456789012345680

NEW_JOINER_ROLE_ID = 123456789012345681
MEMBER_ROLE_ID = 123456789012345682

# ======================================================
# VIEWS
# ======================================================

class InterestView(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def toggle_role(self, interaction, role_id):
        try:
            guild = interaction.guild
            member = interaction.user

            role = guild.get_role(role_id)

            if role is None:
                return "❌ Role not found."

            # REMOVE ROLE
            if role in member.roles:
                await member.remove_roles(role)
                return f"❌ Removed {role.name}"

            # ADD ROLE
            await member.add_roles(role)

            # AUTO ROLE MANAGEMENT
            new_joiner = guild.get_role(NEW_JOINER_ROLE_ID)
            member_role = guild.get_role(MEMBER_ROLE_ID)

            if new_joiner and new_joiner in member.roles:
                await member.remove_roles(new_joiner)

            if member_role and member_role not in member.roles:
                await member.add_roles(member_role)

            return f"✅ Added {role.name}"

        except discord.Forbidden:
            return "❌ Bot lacks Manage Roles permission."

        except Exception as e:
            print(f"❌ Role Toggle Error: {e}")
            return "⚠️ Something went wrong."

    # ==================================================
    # BUTTONS
    # ==================================================

    @discord.ui.button(
        label="Tech",
        style=discord.ButtonStyle.primary,
        emoji="💻",
        custom_id="tech_btn"
    )
    async def tech_button(self, interaction, button):
        msg = await self.toggle_role(interaction, TECH_ROLE_ID)
        await interaction.response.send_message(msg, ephemeral=True)

    @discord.ui.button(
        label="AI/ML",
        style=discord.ButtonStyle.success,
        emoji="🤖",
        custom_id="ai_btn"
    )
    async def ai_button(self, interaction, button):
        msg = await self.toggle_role(interaction, AI_ROLE_ID)
        await interaction.response.send_message(msg, ephemeral=True)

    @discord.ui.button(
        label="Cyber Security",
        style=discord.ButtonStyle.danger,
        emoji="🛡️",
        custom_id="cyber_btn"
    )
    async def cyber_button(self, interaction, button):
        msg = await self.toggle_role(interaction, CYBER_ROLE_ID)
        await interaction.response.send_message(msg, ephemeral=True)

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
    async def agree_button(self, interaction: discord.Interaction, button: Button):

        embed = discord.Embed(
            title="🎯 Choose Your Interests",
            description="Select your interests below.\nYou can select multiple roles.",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=InterestView(),
            ephemeral=True
        )

# ======================================================
# BOT CORE
# ======================================================

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
    case_insensitive=True
)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    bot.add_view(RulesView())
    bot.add_view(InterestView())

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="New Members 🚀"
        )
    )

@bot.event
async def on_member_join(member):
    try:
        new_role = member.guild.get_role(NEW_JOINER_ROLE_ID)

        if new_role:
            await member.add_roles(new_role)

    except Exception as e:
        print(f"❌ Join Error: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    embed = discord.Embed(
        title="📜 Community Rules",
        description="• Respect everyone\n• No spam\n• No NSFW\n\nClick below to continue.",
        color=discord.Color.green()
    )

    await ctx.send(embed=embed, view=RulesView())

@bot.command()
async def helpme(ctx):
    await ctx.send("`!setup` to start onboarding.")

bot.run(TOKEN)
