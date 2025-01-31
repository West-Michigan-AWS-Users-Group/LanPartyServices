import interactions

bot = interactions.Client()


@interactions.listen()
async def on_startup():
    print("Bot is ready!")


bot.start("token")
