# -*- coding: utf-8 -*-
import os, logging, discord
from discord.ext import commands
from discord.commands import Option  # ← 追加（py-cordのスラッシュ引数用）

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ▼ ここにあなたのサーバーIDを入れる（数値のまま）
# GUILD_ID = 932269784228306995
GUILD_ID = 1131436758970671104

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="/ad"))
    logging.info(f"✅ Logged in as {bot.user} (id: {bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

# ===== スラッシュコマンド /ad =====
@bot.slash_command(name="ad", description="攻守ロールを表示", guild_ids=[GUILD_ID])
async def ad(
    ctx,
    you: Option(str, "あなたの名前を入力"),     # /ad の第1引数
    other: Option(str, "相手の名前を入力"),    # /ad の第2引数
):
    # Discordは“文字色指定”ができないので、色はEmbedで表現する
    atk_color = discord.Color.from_rgb(255, 120, 120)  # 薄い赤
    def_color = discord.Color.from_rgb(0, 180, 170)    # 青緑

    e1 = discord.Embed(
        description=f"**{you}** は 【アタッカー】",
        color=atk_color
    )
    e2 = discord.Embed(
        description=f"**{other}** は 【ディフェンダー】",
        color=def_color
    )

    # みんなに見えるように（ephemeral=False が既定）
    await ctx.respond(embeds=[e1, e2])
    
# 実行
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("環境変数 DISCORD_TOKEN が未設定です。")
    bot.run(token)
