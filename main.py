# -*- coding: utf-8 -*-
import os
import logging
import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

# --- Intents ---
intents = discord.Intents.default()
intents.message_content = True  # メッセージ本文を読み取る場合に必須

# --- Bot本体 ---
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!ping"))
    logging.info(f"✅ Logged in as {bot.user} (id: {bot.user.id})")

@bot.command()
async def ping(ctx):
    """接続確認用: !ping → pong!"""
    await ctx.send("pong!")

def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("環境変数 DISCORD_TOKEN が設定されていません。")
    bot.run(token)

if __name__ == "__main__":
    main()
