import discord
from discord.ext import commands
from discord.ui import View
import asyncio

# ======================================================
# ROLE CONFIG
# ======================================================

NEW_JOINER_ROLE = "🌱 New Joiner"
MEMBER_ROLE = "✅ Member"

INTEREST_ROLES = [
    "💻 Programming",
    "🤖 AI / ML",
    "🛡️ Cybersecurity",
    "🧠 Psychology",
    "📈 Markets",
    "🚀 Startups"
]

# ======================================================
# INTEREST BUTTON VIEW
# ======================================================

class InterestView(View):

    def __init__(self):

        super().__init__(timeout=None)

    # ==================================================
    # ROLE TOGGLE
    # ==================================================

    async def toggle_role(
        self,
        interaction,
        role_name
    ):

        try:

            guild = interaction.guild
            member = interaction.user

            role = discord.utils.get(
                guild.roles,
                name=role_name
            )

            if role is None:

                return (
                    f"❌ Role `{role_name}` "
                    f"not found."
                )

            # ==========================================
            # REMOVE ROLE
            # ==========================================

            if role in member.roles:

                await member.remove_roles(role)

                return (
                    f"❌ Removed "
                    f"`{role_name}`"
                )

            # ==========================================
            # ADD ROLE
            # ==========================================

            await member.add_roles(role)

            # ==========================================
            # REMOVE NEW JOINER ROLE
            # ==========================================

            joiner_role = discord.utils.get(
                guild.roles,
                name=NEW_JOINER_ROLE
            )

            if (
                joiner_role
                and joiner_role in member.roles
            ):

                await member.remove_roles(
                    joiner_role
                )

            # ==========================================
            # ADD MEMBER ROLE
            # ==========================================

            member_role = discord.utils.get(
                guild.roles,
                name=MEMBER_ROLE
            )

            if member_role:

                await member.add_roles(
                    member_role
                )

            return (
                f"✅ Added "
                f"`{role_name}`"
            )

        except Exception as e:

            print(
                f"❌ Role Toggle Error: {e}"
            )

            return (
                "⚠️ Something went wrong."
            )

    # ==================================================
    # PROGRAMMING
    # ==================================================

    @discord.ui.button(
        label="💻 Programming",
        style=discord.ButtonStyle.primary,
        custom_id="programming_btn"
    )

    async def programming_button(
        self,
        interaction,
        button
    ):

        msg = await self.toggle_role(
            interaction,
            "💻 Programming"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

    # ==================================================
    # AI / ML
    # ==================================================

    @discord.ui.button(
        label="🤖 AI / ML",
        style=discord.ButtonStyle.success,
        custom_id="ai_btn"
    )

    async def ai_button(
        self,
        interaction,
        button
    ):

        msg = await self.toggle_role(
            interaction,
            "🤖 AI / ML"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

    # ==================================================
    # CYBERSECURITY
    # ==================================================

    @discord.ui.button(
        label="🛡️ Cybersecurity",
        style=discord.ButtonStyle.danger,
        custom_id="cyber_btn"
    )

    async def cyber_button(
        self,
        interaction,
        button
    ):

        msg = await self.toggle_role(
            interaction,
            "🛡️ Cybersecurity"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

    # ==================================================
    # PSYCHOLOGY
    # ==================================================

    @discord.ui.button(
        label="🧠 Psychology",
        style=discord.ButtonStyle.secondary,
        custom_id="psychology_btn"
    )

    async def psychology_button(
        self,
        interaction,
        button
    ):

        msg = await self.toggle_role(
            interaction,
            "🧠 Psychology"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

    # ==================================================
    # MARKETS
    # ==================================================

    @discord.ui.button(
        label="📈 Markets",
        style=discord.ButtonStyle.secondary,
        custom_id="markets_btn"
    )

    async def markets_button(
        self,
        interaction,
        button
    ):

        msg = await self.toggle_role(
            interaction,
            "📈 Markets"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

    # ==================================================
    # STARTUPS
    # ==================================================

    @discord.ui.button(
        label="🚀 Startups",
        style=discord.ButtonStyle.secondary,
        custom_id="startups_btn"
    )

    async def startups_button(
        self,
        interaction,
        button
    ):

        msg = await self.toggle_role(
            interaction,
            "🚀 Startups"
        )

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )

# ======================================================
# RULES VIEW
# ======================================================

class RulesView(View):

    def __init__(self):

        super().__init__(timeout=None)

    @discord.ui.button(
        label="✅ I Agree",
        style=discord.ButtonStyle.success,
        custom_id="agree_rules_btn"
    )

    async def agree_button(
        self,
        interaction,
        button
    ):

        try:

            embed = discord.Embed(
                title="🎯 Choose Your Interests",
                description=(
                    "Select your interests below.\n\n"
                    "You can choose multiple roles."
                ),
                color=discord.Color.blurple()
            )

            embed.add_field(
                name="Available Interests",
                value=(
                    "💻 Programming\n"
                    "🤖 AI / ML\n"
                    "🛡️ Cybersecurity\n"
                    "🧠 Psychology\n"
                    "📈 Markets\n"
                    "🚀 Startups"
                ),
                inline=False
            )

            embed.set_footer(
                text="KATALYST Community System"
            )

            await interaction.response.send_message(
                embed=embed,
                view=InterestView(),
                ephemeral=True
            )

        except Exception as e:

            print(
                f"❌ Rules Button Error: {e}"
            )

# ======================================================
# ONBOARDING COG
# ======================================================

class Onboarding(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        # ==============================================
        # PERSISTENT VIEWS
        # ==============================================

        self.bot.add_view(
            RulesView()
        )

        self.bot.add_view(
            InterestView()
        )

    # ==================================================
    # MEMBER JOIN EVENT
    # ==================================================

    @commands.Cog.listener()

    async def on_member_join(
        self,
        member
    ):

        try:

            role = discord.utils.get(
                member.guild.roles,
                name=NEW_JOINER_ROLE
            )

            if role:

                await member.add_roles(role)

            # ==========================================
            # OPTIONAL WELCOME DM
            # ==========================================

            try:

                await member.send(
                    f"👋 Welcome to "
                    f"**{member.guild.name}**!\n\n"
                    f"Please read the rules "
                    f"and choose interests."
                )

            except:

                pass

        except Exception as e:

            print(
                f"❌ Member Join Error: {e}"
            )

    # ==================================================
    # SETUP COMMAND
    # ==================================================

    @commands.command()

    @commands.has_permissions(
        administrator=True
    )

    async def setup(
        self,
        ctx
    ):

        embed = discord.Embed(
            title="📜 Rules & Etiquette",
            description=(
                "✅ Respect everyone\n"
                "✅ No spam\n"
                "✅ No NSFW\n"
                "✅ No hate speech\n"
                "✅ Be helpful\n\n"
                "Click below to continue."
            ),
            color=discord.Color.green()
        )

        embed.add_field(
            name="🌱 Onboarding",
            value=(
                "1. Read rules\n"
                "2. Accept rules\n"
                "3. Choose interests\n"
                "4. Unlock community"
            ),
            inline=False
        )

        embed.set_footer(
            text="KATALYST Community"
        )

        await ctx.send(
            embed=embed,
            view=RulesView()
        )

    # ==================================================
    # ROLES COMMAND
    # ==================================================

    @commands.command()

    async def roles(
        self,
        ctx
    ):

        embed = discord.Embed(
            title="🎭 Available Roles",
            description=(
                "\n".join(INTEREST_ROLES)
            ),
            color=discord.Color.orange()
        )

        await ctx.send(embed=embed)

# ======================================================
# SETUP
# ======================================================

async def setup(bot):

    await bot.add_cog(
        Onboarding(bot)
    )
