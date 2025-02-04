# This code shows a very brief and small example of how to create a bot with our library.
# This example does not cover all the features of the library, but it is enough to get you started.
# In order to learn more about how to use the library, please head over to our documentation:
# https://interactions-py.github.io/interactions.py/

import logging
import os

ecs_environment = os.getenv("ENVIRONMENT")

# The first thing you need to do is import the library.
import interactions

# Now, let's create an instance of a bot.
# When you make a bot, we refer to it as the "client."
# The client is the main object that interacts with the Gateway, what talks to Discord.
# The client is also the main object that interacts with the API, what makes requests with Discord.
# The client can also have "intents" that are what the bot recieves,
# in this case the default ones and message content (a privilaged intent that needs
# to be enabled in the developer portal)
intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
client = interactions.Client(intents=intents)

# We need to get the token from the environment variables.
discord_bot_client_token = os.getenv("DISCORD_BOT_CLIENT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

featured_games = {
    "tee-worlds": {
        "info_link": "https://grlanparty.info/tee-world",
        "server_status_url": "https://api.grlanparty.info/status?stack_name=teeworlds",
        "description": "A fast-paced online multiplayer platformer.",
        "stack_name": "teeworlds",
    },
    "quake3": {
        "info_link": "https://grlanparty.info/quake3",
        "server_status_url": "https://api.grlanparty.info/status?stack_name=quake3",
        "description": "A first-person shooter game.",
        "stack_name": "quake3",
    },
    "ut99": {
        "info_link": "https://grlanparty.info/ut99",
        "server_status_url": "https://api.grlanparty.info/status?stack_name=ut99",
        "description": "A classic first-person shooter game.",
        "stack_name": "ut99",
    },
    "ut2k4": {
        "info_link": "https://grlanparty.info/ut2k4",
        "server_status_url": "https://api.grlanparty.info/status?stack_name=ut2k4",
        "description": "A futuristic first-person shooter game.",
        "stack_name": "ut2k4",
    },
    "bar": {
        "info_link": "https://grlanparty.info/bar",
        "description": "A real-time strategy game.",
    },
    "cnc_open_ra": {
        "info_link": "https://grlanparty.info/cnc_open_ra",
        "description": "A real-time strategy game based on Command & Conquer.",
    },
    "cnc_generals_zero_hour": {
        "info_link": "https://grlanparty.info/cnc_generals_zero_hour",
        "description": "An expansion pack for Command & Conquer: Generals.",
    },
    "total_annihilation": {
        "info_link": "https://grlanparty.info/total_annihilation",
        "description": "A real-time strategy game.",
    },
    "teeworlds": {
        "info_link": "https://grlanparty.info/teeworlds",
        "description": "A fast-paced online multiplayer platformer.",
    },
    "40k_speed_freeks": {
        "info_link": "https://grlanparty.info/40k_speed_freeks",
        "description": "A racing game set in the Warhammer 40k universe.",
    },
}
games_list_string = "\n".join([f"- `{game}`" for game in featured_games])
game_list_help_string = "\n".join([f"/game-info {game}" for game in featured_games])
hosted_server_list = [
    game for game in featured_games if "server_status_url" in featured_games[game]
]
hosted_server_list_help_string = "\n".join(
    [f"/server-info {game}" for game in hosted_server_list]
)


# With our client established, let's have the library inform us when the client is ready.
# These are known as event listeners. An event listener can be established in one of two ways.
# You can provide the name of the event, prefixed by an "on_", or by telling the event decorator what event it is.
@interactions.listen()
async def on_ready():
    logger.info(f"We're online! We've logged in as {client.app.name}.")
    if client.latency != float("inf") and client.latency is not None:
        logger.info(f"Our latency is {round(client.latency)} ms.")
    else:
        logger.info("Latency is infinity or undefined, cannot convert to integer.")


# We can either pass in the event name or make the function name be the event name.
@interactions.listen("on_message_create")
async def name_this_however_you_want(message_create: interactions.events.MessageCreate):
    # Whenever we specify any other event type that isn't "READY," the function underneath
    # the decorator will most likely have an argument required. This argument is the data
    # that is being supplied back to us developers, which we call a data model.

    # In this example, we're listening to messages being created. This means we can expect
    # a "message_create" argument to be passed to the function, which will contain the
    # data model for the message

    # We can use the data model to access the data we need.
    # Keep in mind that you can only access the message content if your bot has the MESSAGE_CONTENT intent.
    # You can find more information on this in the migration section of the quickstart guide.
    message: interactions.Message = message_create.message
    logger.info(
        f"We've received a message from {message.author.username}. The message is: {message.content}."
    )


# Now, let's create a command.
# A command is a function that is called when a user types out a command.
# The command is called with a context object, which contains information about the user, the channel, and the guild.
# Context is what we call the described information given from an interaction response, what comes from a command.
# The context object in this case is a class for commands, but can also be one for components if used that way.
@interactions.slash_command(
    name="hello-world",
    description='A command that says "hello world!" and returns the environment.',
)
async def hello_world(ctx: interactions.SlashContext):
    # "ctx" is an abbreviation of the context object.
    # You don't need to type hint this, but it's recommended to do so.

    # Now, let's send back a response.
    # The interaction response should be the LAST thing you do when a command is ran.
    await ctx.send(f"Hello, I am the LAN party bot running in the {ecs_environment}!")

    # However, any code you put after a response will still execute unless you prevent it from doing so.
    logger.info("we ran.")


@interactions.slash_command(
    name="user-help",
    description="Command that provides help information about this bot.",
)
async def user_help(ctx: interactions.SlashContext):
    await ctx.send(
        "Hello! I am the LAN Party Bot. I am used to provide information on games and assets used in a party setting. "
        "I can help with starting or stopping servers, as well as providing links to game information on how to install"
        "and play. "
        "**The available commands are:**\n"
        "`/user-help` - Get help information about this bot.\n"
        "`/server-info <game_name>` - Get the status of a specific server or all servers.\n"
        "`/start` - Start a server.\n"
        "`/stop` - Stop a server.\n"
        "`/game-info` - Get information about a game."
        "\n"
        "**The available games are:**\n"
        f"{games_list_string}"
    )
    logger.info("help command executed.")


@interactions.slash_command(
    name="server-info",
    description="Command that provides server information about this bot to the user.",
)
async def server_info(game_name: str = None) -> str:
    import aiohttp

    if not game_name:
        return f"No game specified. Please provide a game name. Valid options are:\n{games_list_string}"

    if game_name not in featured_games:
        return f"No information available for the game: {game_name}\n Try one of the following:\n{games_list_string}"

    game_info = featured_games.get(game_name)
    server_status_url = game_info.get("server_status_url")
    stack_name = game_info.get("stack_name", game_name)
    info_link = game_info.get("info_link", f"https://grlanparty.info/{stack_name}")

    if not server_status_url:
        return f"No hosted server configured for {game_name}. More info on multiplayer: {info_link}"

    async with aiohttp.ClientSession() as session:
        async with session.get(server_status_url) as response:
            if response.status == 200:
                data = await response.json()
                server_online = data.get("result", False)
                status_emoji = "🟢" if server_online else "🔴"
                status_message = "online" if server_online else "offline"
                return f"The server for {game_name} is {status_message} {status_emoji}. More info: {info_link}"
            else:
                return f"Error fetching server status for {game_name}."


@interactions.slash_command(
    name="start",
    description="Command to start a server.",
)
async def start_server(ctx: interactions.SlashContext, game_name: str):
    await ctx.send(f"Start server functionality not implemented yet for {game_name}...")
    # Placeholder logic for starting the server
    logger.info(f"Start server command executed for {game_name}.")


@interactions.slash_command(
    name="stop",
    description="Command to stop a server.",
)
async def stop_server(ctx: interactions.SlashContext, game_name: str):
    await ctx.send(f"Stop server functionality not implemented yet for {game_name}...")
    # Placeholder logic for stopping the server
    logger.info(f"Stop server command executed for {game_name}.")


@interactions.slash_command(
    name="game-info",
    description="Command to get information about a game.",
)
async def game_info(ctx: interactions.SlashContext, game_name: str):
    if game_name not in featured_games:
        await ctx.send(
            f"No information available for the game: {game_name}\n Try one of the following:\n {games_list_string}"
        )
        return

    game_info = featured_games.get(game_name)
    stack_name = game_info.get("stack_name", game_name)
    info_link = game_info.get("info_link", f"https://grlanparty.info/{stack_name}")
    description = game_info.get("description", "No description available.")

    await ctx.send(
        f"**{game_name}**\nDescription: {description}\nMore info: {info_link}"
    )
    logger.info(f"Game info command executed for {game_name}.")


# After we've declared all of the bot code we want, we need to tell the library to run our bot.
# In this example, we've decided to do some things in a different way without explicitly d saying it:

# - we'll be syncing the commands automatically.
#   if you want to do this manually, you can do it by passing disable_sync=False in the Client
#   object on line 13.
# - we are not setting a presence.
# - we are not automatically sharding, and registering the connection under 1 shard.
# - we are using default intents, which are Gateway intents excluding privileged ones
# - and the privilaged message content intent.
client.start(discord_bot_client_token)
