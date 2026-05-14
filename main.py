import os
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv

# ======================================================
# LOAD ENV VARIABLES
# ======================================================

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:

    raise ValueError(
        "❌ TOKEN missing in .env file"
    )

# ======================================================
# DISCORD INTENTS
# ======================================================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True

# ======================================================
# BOT SETUP
# ======================================================

bot = commands.Bot(
    command_prefix="k!",
    intents=intents,
    help_command=None,
    case_insensitive=True
)

# ======================================================
# BOT STATUS
# ======================================================

BOT_VERSION = "1.0.0"

# ======================================================
# READY EVENT
# ======================================================

@bot.event
async def on_ready():

    print("=" * 60)
    print(f"✅ Logged in as: {bot.user}")
    print(f"✅ Bot ID: {bot.user.id}")
    print(f"✅ Connected Servers: {len(bot.guilds)}")
    print(f"✅ Discord.py Version: {discord.__version__}")
    print(f"✅ KATALYST VERSION: {BOT_VERSION}")
    print("✅ KATALYST ONLINE")
    print("=" * 60)

    try:

        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="k!helpme"
            )
        )

    except Exception as e:

        print(f"❌ Presence Error: {e}")

# ======================================================
# GUILD JOIN EVENT
# ======================================================

@bot.event
async def on_guild_join(guild):

    print(
        f"✅ Joined new server: "
        f"{guild.name} ({guild.id})"
    )

# ======================================================
# GUILD REMOVE EVENT
# ======================================================

@bot.event
async def on_guild_remove(guild):

    print(
        f"❌ Removed from server: "
        f"{guild.name} ({guild.id})"
    )

# ======================================================
# LOAD COGS
# ======================================================

async def load_cogs():

    cogs = [
        "cogs.utility",
        "cogs.onboarding",
        "cogs.leveling"
    ]

    for cog in cogs:

        try:

            await bot.load_extension(cog)

            print(f"✅ Loaded Cog: {cog}")

        except Exception as e:

            print("=" * 60)
            print(f"❌ Failed to load cog: {cog}")
            print(e)
            print("=" * 60)

# ======================================================
# BASIC STATUS COMMAND
# ======================================================

@bot.command()

async def alive(ctx):

    embed = discord.Embed(
        title="✅ KATALYST ONLINE",
        description=(
            "KATALYST community system "
            "is operational."
        ),
        color=discord.Color.green()
    )

    embed.add_field(
        name="Prefix",
        value="`k!`",
        inline=True
    )

    embed.add_field(
        name="Servers",
        value=str(len(bot.guilds)),
        inline=True
    )

    embed.add_field(
        name="Latency",
        value=f"{round(bot.latency * 1000)}ms",
        inline=True
    )

    embed.set_footer(
        text=f"KATALYST v{BOT_VERSION}"
    )

    await ctx.send(embed=embed)

# ======================================================
# SERVER COUNT COMMAND
# ======================================================

@bot.command()

async def servers(ctx):

    await ctx.send(
        f"🌍 Connected Servers: "
        f"`{len(bot.guilds)}`"
    )

# ======================================================
# LATENCY COMMAND
# ======================================================

@bot.command()

async def latency(ctx):

    await ctx.send(
        f"⚡ Latency: "
        f"`{round(bot.latency * 1000)}ms`"
    )

# ======================================================
# RELOAD COMMAND
# ======================================================

@bot.command()

@commands.has_permissions(administrator=True)

async def reload(ctx):

    cogs = [
        "cogs.utility",
        "cogs.onboarding",
        "cogs.leveling"
    ]

    success = []
    failed = []

    for cog in cogs:

        try:

            await bot.reload_extension(cog)

            success.append(cog)

        except Exception as e:

            failed.append(
                f"{cog} → {e}"
            )

    embed = discord.Embed(
        title="♻️ Reload Results",
        color=discord.Color.blurple()
    )

    if success:

        embed.add_field(
            name="✅ Reloaded",
            value="\n".join(success),
            inline=False
        )

    if failed:

        embed.add_field(
            name="❌ Failed",
            value="\n".join(failed),
            inline=False
        )

    await ctx.send(embed=embed)

# ======================================================
# GLOBAL ERROR HANDLER
# ======================================================

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):

        await ctx.send(
            "❌ Unknown command.\n"
            "Use `k!helpme`"
        )

    elif isinstance(error, commands.CommandOnCooldown):

        await ctx.send(
            f"⏳ Slow down.\n"
            f"Try again in "
            f"`{round(error.retry_after, 1)}s`"
        )

    elif isinstance(error, commands.MissingPermissions):

        await ctx.send(
            "❌ You don't have permission."
        )

    elif isinstance(error, commands.BotMissingPermissions):

        await ctx.send(
            "❌ Bot lacks required permissions."
        )

    elif isinstance(error, commands.MissingRequiredArgument):

        await ctx.send(
            "❌ Missing required arguments."
        )

    else:

        print("=" * 60)
        print("❌ UNHANDLED ERROR")
        print(error)
        print("=" * 60)

        try:

            await ctx.send(
                "⚠️ Unexpected error occurred."
            )

        except:
            pass

# ======================================================
# STARTUP FUNCTION
# ======================================================

async def main():

    async with bot:

        await load_cogs()

        try:

            await bot.start(TOKEN)

        except discord.LoginFailure:

            print("❌ Invalid Discord Token")

        except Exception as e:

            print(f"❌ Fatal Startup Error: {e}")

# ======================================================
# RUN BOT
# ======================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print("🛑 Bot stopped manually")

    except Exception as e:

        print(f"❌ Critical Error: {e}")
