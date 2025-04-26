
import discord
from discord import option
from discord.ext import commands
from dotenv import load_dotenv
import os
from modules import pressure_converter, chart_generator, tts_module, knowledge_base
from keep_alive import keep_alive

# 讀取 .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_LANGUAGE = "zh_tw"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
user_language = {}

@bot.event
async def on_ready():
    print(f"✅ 機器人已登入：{bot.user}")
    await bot.sync_commands()
    keep_alive()

@bot.slash_command(name="換算壓力", description="將壓力從一個單位轉換成另一個單位")
@option("數值", float, description="請輸入數值")
@option("原單位", description="選擇原單位", choices=list(pressure_converter.pressure_units.keys()))
@option("目標單位", description="選擇目標單位", choices=list(pressure_converter.pressure_units.keys()))
async def 換算壓力(ctx: discord.ApplicationContext, 數值: float, 原單位: str, 目標單位: str):
    result, formula = pressure_converter.convert(數值, 原單位, 目標單位)
    embed = pressure_converter.create_embed(數值, 原單位, 目標單位, result, formula)
    await ctx.respond(embed=embed)
    await chart_generator.send_chart(ctx, 數值, 原單位, result, 目標單位)
    await tts_module.speak(ctx, f"{數值} {原單位} 等於 {result:.6f} {目標單位}")

@bot.slash_command(name="單位小知識", description="查詢單位小知識")
@option("單位", str, description="輸入單位名稱，例如atm, psi, mmHg")
async def 單位小知識(ctx: discord.ApplicationContext, 單位: str):
    response = knowledge_base.get_info(單位)
    await ctx.respond(response)

bot.run(TOKEN)
