import os, sqlite3
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters


load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
DB    = "pokemon.db"

def get_pokemon(nombre: str):
    nombre = nombre.lower()
    conn = sqlite3.connect(DB)
    row  = conn.execute(
        "SELECT nombre,altura,peso,tipos,habilidades FROM pokemon WHERE nombre = ?", 
        (nombre,)
    ).fetchone()
    conn.close()
    if not row: return None
    name, h, w, tipos, habs = row
    return {"nombre": name.title(), "altura": h, "peso": w, "tipos": tipos, "habilidades": habs}

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Soy tu PokéDex Bot.\n"
        "Escribe /pokemon <nombre> para buscar."
    )

async def pokemon_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        return await update.message.reply_text("❌ Uso: /pokemon <nombre>")
    p = get_pokemon(ctx.args[0])
    if not p:
        return await update.message.reply_text(f"❌ No encontré “{ctx.args[0]}”.")
    msg = (
      f"🧬 *{p['nombre']}*\n"
      f"• Altura: {p['altura']}  Peso: {p['peso']}\n"
      f"• Tipos: {p['tipos']}\n"
      f"• Habilidades: {p['habilidades']}"
    )
    await update.message.reply_markdown(msg)

async def echo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.text.split()[0]
    await pokemon_cmd(update, ctx)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("pokemon", pokemon_cmd))
    app.add_handler(CommandHandler("echo",    echo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("🤖 Bot iniciado. Ctrl-C para parar.")
    app.run_polling()

if __name__ == "__main__":
    main()
