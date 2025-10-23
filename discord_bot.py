import discord
import os
import django
import asyncio
from discord.ext import commands

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheuzebux.settings')
django.setup()

from core.models import Order

TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = int(os.environ.get('DISCORD_CHANNEL_ID'))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    bot.loop.create_task(send_pending_orders())

async def send_pending_orders():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    while not bot.is_closed():
        pending_orders = Order.objects.filter(paid=False)
        if pending_orders:
            message = "**Pending Orders:**\n"
            for order in pending_orders:
                message += f"Order ID: {order.id}, Total: ${order.get_total_cost()}\n"
            await channel.send(message)
        else:
            await channel.send("No pending orders.")
        await asyncio.sleep(3600)

@bot.command()
async def pending(ctx):
    """Checks for pending orders."""
    pending_orders = Order.objects.filter(paid=False)
    if pending_orders.exists():
        message = "**Pending Orders:**\n"
        for order in pending_orders:
            message += f"  - Order ID: {order.id}\n"
            message += f"    Name: {order.first_name} {order.last_name}\n"
            message += f"    Total: ${order.get_total_cost()}\n"
            message += "    Items:\n"
            for item in order.items.all():
                message += f"      - {item.product.name} (x{item.quantity})\n"
        await ctx.send(message)
    else:
        await ctx.send("No pending orders found.")

bot.run(TOKEN)
