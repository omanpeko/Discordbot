# -*- coding: utf-8 -*-
import os
import logging
import random
import discord
from discord.ext import commands
from discord.commands import Option  # py-cord のスラッシュコマンド用

logging.basicConfig(level=logging.INFO)

# ---- Intents（スラッシュは最低限でもOK。テキストコマンドも使うので message_content をON）----
intents = discord.Intents.default()
intents.message_content = True

# ---- Bot 本体 ----
bot = commands.Bot(command_prefix="!", intents=intents)

# ★複数サーバーID（あなたの2つを入れてあります）
GUILD_IDS = [
    932269784228306995,  # CYNTHIA
    1131436758970671104, # ぺこ
]

@bot.event
async def on_ready():
    # ギルド限定のコマンドは即時反映（開発がラク）
    try:
        await bot.sync_commands(guild_ids=GUILD_IDS)
    except Exception as e:
        logging.warning(f"sync_commands failed: {e}")

    await bot.change_presence(activity=discord.Game(name="/ad"))
    logging.info(f"✅ Logged in as {bot.user} (id: {bot.user.id})")

# ---- 動作確認用の通常コマンド（!ping → pong!）----
@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

# =======================================================================================
# /ad（攻守ロールを表示 + カスタムコード）:
#   - 表示順は「アタッカー→ディフェンダー」を固定、担当だけランダム
#   - アタッカー：薄い赤、ディフェンダー：青緑、カスタムコード：グレー（太字表示）
#   - みんなに見える通常メッセージで返信（ephemeral=False が既定）
# =======================================================================================
@bot.slash_command(
    name="ad",
    description="攻守ロールを表示（担当はランダム）＋カスタムコードを添える",
    guild_ids=GUILD_IDS,  # ←複数ギルドに即時登録
)
async def ad(
    ctx,
    you: Option(
        str,
        "あなたの名前を入力",
        name_localizations={"ja": "あなた"},
        description_localizations={"ja": "あなたの名前を入力"},
    ),
    other: Option(
        str,
        "相手の名前を入力",
        name_localizations={"ja": "相手"},
        description_localizations={"ja": "相手の名前を入力"},
    ),
    code: Option(
        str,
        "カスタムコードを入力",
        name_localizations={"ja": "カスタムコード"},
        description_localizations={"ja": "カスタムコードを入力"},
    ),
):
    you = you.strip()
    other = other.strip()
    code = code.strip()

    # 色は固定（アタッカー＝薄い赤、ディフェンダー＝青緑、カスタムコード＝グレー）
    atk_color  = discord.Color.from_rgb(255, 120, 120)  # 薄い赤
    def_color  = discord.Color.from_rgb(0, 180, 170)    # 青緑
    code_color = discord.Color.from_rgb(145, 145, 145)  # グレー

    # どちらがアタッカーになるかだけランダム（表示順は固定）
    if random.random() < 0.5:
        attacker_name, defender_name = you, other
    else:
        attacker_name, defender_name = other, you

    e1 = discord.Embed(
        description=f"**{attacker_name}** は 【アタッカー】",
        color=atk_color,
    )
    e2 = discord.Embed(
        description=f"**{defender_name}** は 【ディフェンダー】",
        color=def_color,
    )
    e3 = discord.Embed(
        description=f"カスタムコードは【**{code}**】",
        color=code_color,
    )

    await ctx.respond(embeds=[e1, e2, e3])  # みんなに見える通常返信

# ---- エントリーポイント ----
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("環境変数 DISCORD_TOKEN が未設定です。Railway の Variables に設定してください。")
    bot.run(token)
