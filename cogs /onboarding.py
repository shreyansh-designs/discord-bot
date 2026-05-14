import discord
from discord.ext import commands
from discord.ui import View, Button

NEW_JOINER_ROLE = "🌱 New Joiner"
MEMBER_ROLE = "✅ Member"

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
            return f"❌ Role '{role_name}' not found."

        if role in member.roles:

            await member.remove_roles(role)

            return f"❌ Removed {role_name}"

        await member.add_roles(role)

        # Remove joiner role
        joiner = discord.utils.get(
            guild.roles,
            name=NEW_JOINER_ROLE
        )

        if joiner and joiner in member.roles:
            await member.remove_roles(joiner)

        # Add member role
        member_role = discord.utils.get(
            guild.roles,
            name=MEMBER_ROLE
        )

        if member_role:
            await member.add_roles(member_role)

        return f"✅ Added {role_name}"

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
        interaction,
        button
    ):

        embed = discord.Embed(
            title="🎯 Choose Interests",
            description=(
                "Select interests below."
            ),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=InterestView(),
            ephemeral=True
        )

class Onboarding(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.bot.add_view(RulesView())
        self.bot.add_view(InterestView())

    @commands.Cog.listener()
    async def on_member_join(self, member):

        role = discord.utils.get(
            member.guild.roles,
            name=NEW_JOINER_ROLE
        )

        if role:
            await member.add_roles(role)

    @commands.command()

    @commands.has_permissions(administrator=True)

    async def setup(self, ctx):

        embed = discord.Embed(
            title="📜 Rules & Etiquette",
            description=(
                "✅ Respect everyone\n"
                "✅ No spam\n"
                "✅ No NSFW\n\n"
                "Click below to continue."
            ),
            color=discord.Color.green()
        )

        await ctx.send(
            embed=embed,
            view=RulesView()
        )

async def setup(bot):

    await bot.add_cog(
        Onboarding(bot)
    )
