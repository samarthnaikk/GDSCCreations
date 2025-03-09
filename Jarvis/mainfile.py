import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from database import *
from helper import generate_upi_qr
from iWriter import writepdf
from datetime import datetime
import csv
import os
from PyPDF2 import PdfReader
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from tabulate import tabulate
import google.generativeai as genai

genai.configure(api_key="your_api_key")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot_ready = False

@bot.event
async def on_ready():
    global bot_ready
    check_reminders.start()
    if bot_ready:
        return
    bot_ready = True

@bot.command()
async def add(ctx, *, message: str = None): 
    author = str(ctx.author.id)
    downloads_dir = "./downloads"
    os.makedirs(downloads_dir, exist_ok=True)
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith(".txt"):
                file_path = os.path.join(downloads_dir, attachment.filename)                
                await attachment.save(file_path)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                store_(author, content)
                await ctx.send(f"`Message in {attachment.filename} saved.`")
                return
    text_content = message or ctx.message.content
    store_(author, text_content)
    await ctx.send(f"`Message saved:` {text_content}")

@bot.command()
async def ask(ctx,query: str) -> str:
    """
    Takes a query, checks what the user needs, and provides guidance.
    If the feature is not available, informs the user that an update will come soon.
    """
    commands = '''
These are the functions for your reference
add - !add (the message), adds the message for the user
delete - !delete (message id), will delete that message
generatepdf - !generatepdf (message id), will give the handwritten pdf, if the balance is enough
merge - !merge will merge all messages to one. !merge 1 2 will merge messgaes with id 1 and 2
show - !show will show all the messages of the user
upi - !upi (upi id) will update or add the user's upi id. Doing this gives 10 rupees.
    '''
    que = f"""
    There is an machine that return handwritten PDF for given text. 
    You are the receptionist.{commands} are the commands of the 
    machine. The following query is given by and user, please guide 
    them accordingly by telling them what to type. If anything is 
    out of commands, tell update will come soon. Answer only how much is asked, not more or less
    A few more facts about machine:
    Until you register using !upi, your payments will not be considered.
    To make payments you can directly pay to the QR Code given in how-to-order
    PDF will be sent instantly, if the user has enough balance, balance will not be updated instantly. At 9 PM it will be updated.
    """
    que+=query
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(que)
        await ctx.send(f"{ctx.author.mention}, {response.text}")
    except Exception as e:
        await ctx.send(f"An update will come soon! (Error: {str(e)})")

@bot.command()
async def c(ctx, *, message: str = None):
    author = str(ctx.author.id) 
    if message:
        store_1(author,message)
        l=get_tables("knowledge")
        content = ''
        for i in l:
            if i['author'] == author:
                content += i['text']+'\n'
        que = f'''
        You have to continue conversation with a user. Topic can be anything
        You will be given context.
        This is the context {content}
        '''
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(que)
            await ctx.send(f"{ctx.author.mention}, {response.text}")
        except Exception as e:
            await ctx.send(f"I am sorry, I cannot think of anything at this moment.")

@tasks.loop(minutes=10)
async def check_reminders():
    now = datetime.utcnow()
    reminders = get_ar()
    for reminder in reminders:
        reminder_id = reminder["id"]
        user_id = reminder["author"]
        reminder_time = datetime.strptime(reminder["time"], "%d-%m-%Y %H:%M")
        message = reminder["message"]
        notified = reminder["notified"]
        if not notified and (now >= reminder_time - timedelta(minutes=10)):
            user = await bot.fetch_user(int(user_id))
            if user:
                await user.send(f"**Reminder (10 min early):** {message}")
            notified_r(reminder_id)
        if now >= reminder_time:
            user = await bot.fetch_user(int(user_id))
            if user:
                await user.send(f"**Reminder:** {message}")
            delete_r(reminder_id)

@bot.command()
async def remind(ctx, *, message: str = None):
    """Command to set a reminder with date & time in DD-MM-YYYY HH:MM format"""
    if message is None:
        await ctx.send("Please provide a reminder in this format:\n`!c 10-03-2025 15:30 | Meeting`")
        return
    try:
        parts = message.split(" | ", 1)
        if len(parts) != 2:
            await ctx.send("Invalid format! Use: `DD-MM-YYYY HH:MM | Meeting`")
            return
        reminder_time, reminder_message = parts
        datetime.strptime(reminder_time, "%d-%m-%Y %H:%M")
        store_r(ctx.author.id, reminder_time, reminder_message)
        await ctx.send(f"Reminder set for **{reminder_time} UTC**: {reminder_message}. You will receive a DM.")
    except ValueError:
        await ctx.send("Invalid date/time format! Use `DD-MM-YYYY HH:MM | Meeting`.")

@bot.command()
async def poll(ctx, *, message: str = None):
    """Command to create a poll. Format: !poll Question | Option1 | Option2 | ..."""
    if message is None:
        await ctx.send("**Invalid format!** Use:\n`!poll Your question? | Option1 | Option2 | Option3`")
        return
    parts = message.split(" | ")
    if len(parts) < 2:
        await ctx.send("**Invalid format!** You must provide at least one option.")
        return
    question = parts[0]
    options = parts[1:]
    if len(options) > 10:
        await ctx.send("**You can only have up to 10 options!**")
        return
    emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    poll_embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.blue())
    poll_embed.set_footer(text=f"Poll created by {ctx.author.name}")
    description = ""
    for i, option in enumerate(options):
        description += f"{emoji_numbers[i]} {option}\n"
    poll_embed.add_field(name="Options", value=description, inline=False)
    poll_message = await ctx.send(embed=poll_embed)
    for i in range(len(options)):
        await poll_message.add_reaction(emoji_numbers[i])

@bot.command()
async def show(ctx):
    """Displays all stored messages of the user along with their IDs in a table format."""
    auth = str(ctx.author.id)
    messages = get_tables()  # Get all messages
    user_messages = [msg for msg in messages if msg['author'] == auth]
    if not user_messages:
        await ctx.send("You have no stored messages.")
        return
    table = [[msg['id'], msg['text_content']] for msg in user_messages]
    table_str = tabulate(table, headers=["ID", "Message"], tablefmt="grid")
    if len(table_str)>2000:
        f=open(f"{auth}.txt","w")
        f.write(table_str)
        f.close()
        f1 = open(f"{auth}.txt")
        await ctx.send(
            f"Messages are too big, hence are updated in the attached txt file.",
            file=discord.File(f1),
        )
        f1.close()
    else:
        await ctx.send(f"```\n{table_str}\n```")

@bot.command()
async def delete(ctx, message_id: int = None):
    auth = str(ctx.author.id)
    if message_id:
        response = supabase.table("messages").delete().match({"id": message_id, "author": auth}).execute()
        if response.data:
            await ctx.send(f"{ctx.author.mention}, message with ID `{message_id}` deleted successfully.")
        else:
            await ctx.send(f"{ctx.author.mention}, no message found with ID `{message_id}`.")
    else:
        response = supabase.table("messages").select("id, text_content").eq("author", auth).order("id", desc=True).limit(1).execute()
        if response.data:
            latest_msg = response.data[0]
            supabase.table("messages").delete().match({"id": latest_msg["id"]}).execute()
            await ctx.send(f"{ctx.author.mention}, latest message (`{latest_msg['text_content']}`) deleted successfully.")
        else:
            await ctx.send(f"{ctx.author.mention}, you have no messages to delete.")

@bot.command()
async def merge(ctx, *message_ids: int):
    auth = str(ctx.author.id)
    message_ids = list(message_ids) if message_ids else None
    response = merge_(auth, message_ids)
    if response:
        await ctx.send(f"{ctx.author.mention}, {response}")
    else:
        await ctx.send(f"{ctx.author.mention}, no messages found to merge.")

@bot.command()
async def stat(ctx):
    auth = str(ctx.author.id)
    credentials = get_tables("credential")
    status = next((record for record in credentials if record["author"] == auth), None)
    if status:
        table = [
            ["User", ctx.author.mention],
            ["UPI ID", status.get('upi_id', 'N/A')],
            ["Balance", status.get('balance', 'N/A')]
        ]
        formatted_table = f"```\n{tabulate(table, headers=['Field', 'Value'], tablefmt='grid')}\n```"
        await ctx.send(formatted_table)
    else:
        await ctx.send(f"{ctx.author.mention}, no record found in the database.")

@bot.command()
async def upi(ctx, upi_id: str):
    auth = str(ctx.author.id)
    response = update_(auth, upi_id)
    await ctx.send(f"{ctx.author.mention}, {response}")

@bot.command()
async def generatepdf(ctx, message_id: int):
    user_id = str(ctx.author.id)
    user_stats = get_tables("credential")
    balance = 0
    for user in user_stats:
        if user["author"] == user_id:
            balance = user["balance"]
            break
    messages = get_tables("messages")
    text = None
    for msg in messages:
        if msg["id"] == message_id:
            text = msg["text_content"]
            break
    if text is None:
        await ctx.send("Message not found!")
        return
    filename = f"{user_id}"
    writepdf(text, filename)
    filename+='.pdf'
    with open(filename, "rb") as f:
        reader = PdfReader(f)
        pages = len(reader.pages)
    cost_per_page = 4
    total_cost = pages * cost_per_page
    if balance >= total_cost:
        new_balance = balance - total_cost
        supabase.table("credential").update({"balance": new_balance}).eq("author", user_id).execute()
        await ctx.send(
            f"PDF generated successfully! Deducted ₹{total_cost}. Your new balance is ₹{new_balance}.",
            file=discord.File(filename),
        )
    else:
        await ctx.send(f"Insufficient balance! You need ₹{total_cost}, but you have ₹{balance}. Please add funds.")

bot.run("your_bot_token")
