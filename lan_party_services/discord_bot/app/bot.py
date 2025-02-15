import logging
import os
from typing import Optional

import aiohttp
import interactions
from interactions import OptionType, slash_option

from github import start_adhoc_workflow
from lan_party_services.discord_bot.app.aws import check_stacks_exist

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variable for ECS environment
ecs_environment: Optional[str] = os.getenv("ENVIRONMENT")

# Discord bot client token from environment variables
discord_bot_client_token: Optional[str] = os.getenv("DISCORD_BOT_CLIENT_TOKEN")

# Featured games dictionary
featured_games: dict = {
    "tee-worlds": {
        "info_link": "https://grlanparty.info/tee-worlds/index.html",
        "server_status_url": "https://api.grlanparty.info/status?stack_name=teeworlds",
        "description": "A fast-paced online multiplayer platformer.",
        "stack_name": "teeworlds",
    },
    "quake3": {
        "info_link": "https://grlanparty.info/quake3/index.html",
        "server_status_url": "https://api.grlanparty.info/status?stack_name=quake3",
        "description": "A first-person shooter game.",
        "stack_name": "quake3",
    },
    "ut99": {
        "info_link": "https://grlanparty.info/ut99/index.html",
        "server_status_url": "https://api.grlanparty.info/status?stack_name=ut99",
        "description": "A classic first-person shooter game.",
        "stack_name": "ut99",
    },
    "ut2k4": {
        "info_link": "https://grlanparty.info/ut2k4/index.html",
        "server_status_url": "https://api.grlanparty.info/status?stack_name=ut2k4",
        "description": "A futuristic first-person shooter game.",
        "stack_name": "ut2k4",
    },
    "bar": {
        "info_link": "https://grlanparty.info/bar/index.html",
        "description": "A real-time strategy game.",
    },
    "cnc_open_ra": {
        "info_link": "https://grlanparty.info/cnc_open_ra/index.html",
        "description": "A real-time strategy game based on Command & Conquer.",
    },
    "cnc_generals_zero_hour": {
        "info_link": "https://grlanparty.info/cnc_generals_zero_hour/index.html",
        "description": "An expansion pack for Command & Conquer: Generals.",
    },
    "total_annihilation": {
        "info_link": "https://grlanparty.info/total_annihilation/index.html",
        "description": "A real-time strategy game.",
    },
    "teeworlds": {
        "info_link": "https://grlanparty.info/teeworlds/index.html",
        "description": "A fast-paced online multiplayer platformer.",
    },
    "40k_speed_freeks": {
        "info_link": "https://grlanparty.info/40k_speed_freeks/index.html",
        "description": "A racing game set in the Warhammer 40k universe.",
    },
}

# Games list strings for help messages
games_list_string: str = "\n".join([f"- `{game}`" for game in featured_games])
game_list_help_string: str = "\n".join(
    [f"/game-info {game}" for game in featured_games]
)
hosted_server_list: list = [
    game for game in featured_games if "server_status_url" in featured_games[game]
]
hosted_server_list_help_string: str = "\n".join(
    [f"`{game}`" for game in hosted_server_list]
)

# Create an instance of the bot client
intents: interactions.Intents = (
    interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
)
client: interactions.Client = interactions.Client(intents=intents)


@interactions.listen()
async def on_ready() -> None:
    """Event listener for when the bot is ready."""
    logger.info(f"We're online! We've logged in as {client.app.name}.")
    if client.latency != float("inf") and client.latency is not None:
        logger.info(f"Our latency is {round(client.latency)} ms.")
    else:
        logger.info("Latency is infinity or undefined, cannot convert to integer.")


@interactions.listen("on_message_create")
async def name_this_however_you_want(
    message_create: interactions.events.MessageCreate,
) -> None:
    """Event listener for when a message is created.

    Args:
        message_create (interactions.events.MessageCreate): The message create event.
    """
    message: interactions.Message = message_create.message
    logger.info(
        f"We've received a message from {message.author.username}. The message is: {message.content}."
    )


@interactions.slash_command(
    name="hello-world",
    description='A command that says "hello world!" and returns the environment.',
)
async def hello_world(ctx: interactions.SlashContext) -> None:
    """Slash command that says 'hello world!' and returns the environment.

    Args:
        ctx (interactions.SlashContext): The context of the command.
    """
    await ctx.send(f"Hello, I am the LAN party bot running in the {ecs_environment}!")
    logger.info("we ran.")


@interactions.slash_command(
    name="user-help",
    description="Command that provides help information about this bot.",
)
async def user_help(ctx: interactions.SlashContext) -> None:
    """Slash command that provides help information about this bot.

    Args:
        ctx (interactions.SlashContext): The context of the command.
    """
    await ctx.send(
        "Hello! I am the LAN Party Bot. I am used to provide information on games and assets used in a party setting. "
        "I can help with starting or stopping servers, as well as providing links to game information on how to install"
        " and play. "
        "**The available commands are:**\n"
        "`/user-help` - Get help information about this bot.\n"
        "`/server-info` - Get the status of hosted servers.\n"
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
    description="Command to get server information about a game.",
)
@slash_option(
    name="game_name",
    description="The name of the game",
    required=False,
    opt_type=OptionType.STRING,
)
async def server_info(
    ctx: interactions.SlashContext, game_name: Optional[str] = None
) -> None:
    """Slash command to get server information about a game.

    Args:
        ctx (interactions.SlashContext): The context of the command.
        game_name (Optional[str], optional): The name of the game. Defaults to None.
    """
    if not game_name:
        status_messages = []
        async with aiohttp.ClientSession() as session:
            for game in hosted_server_list:
                game_info = featured_games.get(game)
                server_status_url = game_info.get("server_status_url")
                stack_name = game_info.get("stack_name", game)
                info_link = game_info.get(
                    "info_link", f"https://grlanparty.info/{stack_name}"
                )
                server_url = (
                    f"{game_info['stack_name']}.grlanparty.info"
                    if "stack_name" in game_info
                    else None
                )

                if not server_status_url:
                    status_messages.append(
                        f"No hosted server configured for {game}. More info on multiplayer: {info_link}"
                    )
                    continue

                async with session.get(server_status_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        server_online = data.get("result", False)
                        status_emoji = "🟢" if server_online else "🔴"
                        status_message = "online" if server_online else "offline"
                        status_messages.append(
                            f"The server for {game} is {status_message} {status_emoji}.\n"
                            f"Server URL: {server_url}\n"
                            f"More info: {info_link}"
                        )
                    else:
                        status_messages.append(
                            f"Error fetching server status for {game}."
                        )

        await ctx.send("\n\n".join(status_messages))
        return

    if game_name not in featured_games:
        await ctx.send(
            f"No information available for the game: {game_name}\n Try one of the following:\n{hosted_server_list_help_string}"
        )
        return

    game_info: dict = featured_games.get(game_name)
    server_status_url: Optional[str] = game_info.get("server_status_url")
    stack_name: str = game_info.get("stack_name", game_name)
    info_link: str = game_info.get("info_link", f"https://grlanparty.info/{stack_name}")

    server_url: Optional[str] = None
    if "stack_name" in game_info:
        server_url = f"{game_info['stack_name']}.grlanparty.info"

    if not server_status_url:
        await ctx.send(
            f"No hosted server configured for {game_name}. More info on multiplayer: {info_link}"
        )
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(server_status_url) as response:
            if response.status == 200:
                data: dict = await response.json()
                server_online: bool = data.get("result", False)
                status_emoji: str = "🟢" if server_online else "🔴"
                status_message: str = "online" if server_online else "offline"
                await ctx.send(
                    f"The server for {game_name} is {status_message} {status_emoji}.\n "
                    f"Server URL: {server_url}\n "
                    f"More info: {info_link}"
                )
            else:
                await ctx.send(f"Error fetching server status for {game_name}.")


@interactions.slash_command(
    name="start",
    description="Command to start a server.",
)
@slash_option(
    name="game_name",
    description="The name of the game",
    required=False,
    opt_type=OptionType.STRING,
)
async def start(
    ctx: interactions.SlashContext, game_name: Optional[str] = None
) -> None:
    """Slash command to start a server.

    Args:
        ctx (interactions.SlashContext): The context of the command.
        game_name (Optional[str], optional): The name of the game. Defaults to None.
    """
    if not game_name:
        await ctx.send(
            f"No game specified. Please provide a game name. Valid options are:\n{hosted_server_list_help_string}"
        )
        return

    if game_name not in hosted_server_list:
        await ctx.send(
            f"No hosted server available for the game: {game_name}\n Try one of the following:\n{hosted_server_list_help_string}"
        )
        return

    # Check if core and nlb stacks are deployed
    if not check_stacks_exist(["core"]):
        await ctx.send(
            "Required stack 'core' is not deployed. Please deploy it and try again."
        )
        return

    if not check_stacks_exist(["nlb"]):
        await ctx.send(
            "Required stack 'nlb' is not deployed. Issuing deploy for NLB stack."
        )
        response = start_adhoc_workflow("nlb")
        await ctx.send(
            f"Started NLB stack. Response: {response}. Please wait about 3 minutes and try again"
        )
        return
    elif check_stacks_exist(["nlb"]) == "deploying":
        await ctx.send(
            "The 'nlb' stack is currently being deployed. Please wait until the deployment is complete and "
            "try again."
        )
        return

    try:
        # Call the start_adhoc_workflow function
        response = start_adhoc_workflow(game_name, "cdk_adhoc_deploy.yml")
        await ctx.send(
            f"Started server for {game_name}. Response: {response}. The server will send a notification upon"
            f" initialization."
        )
        logger.info(
            f"Start server command executed for {game_name}. Response: {response}"
        )
    except Exception as e:
        await ctx.send(f"Failed to start server for {game_name}. Error: {str(e)}")
        logger.error(f"Failed to start server for {game_name}. Error: {str(e)}")


@interactions.slash_command(
    name="stop",
    description="Command to stop a server.",
)
@slash_option(
    name="game_name",
    description="The name of the game",
    required=False,
    opt_type=OptionType.STRING,
)
async def stop(ctx: interactions.SlashContext, game_name: Optional[str] = None) -> None:
    """Slash command to stop a server.

    Args:
        ctx (interactions.SlashContext): The context of the command.
        game_name (Optional[str], optional): The name of the game. Defaults to None.
    """
    if not game_name:
        await ctx.send(
            f"No game specified. Please provide a game name. Valid options are:\n{hosted_server_list_help_string}"
        )
        return

    if game_name not in hosted_server_list:
        await ctx.send(
            f"No hosted server available for the game: {game_name}\n Try one of the following:\n{hosted_server_list_help_string}"
        )
        return

    # Check if the stack is deployed
    if not check_stacks_exist([game_name]):
        await ctx.send(
            f"Required stack '{game_name}' is not deployed. No action taken."
        )
        return

    try:
        # Call the stop_adhoc_workflow function
        response = start_adhoc_workflow(game_name, workflow="cdk_adhoc_destroy.yml")
        await ctx.send(
            f"Stopped server for {game_name}. Response: {response}. The server will send a notification upon"
            f" destruction."
        )
        logger.info(
            f"Stop server command executed for {game_name}. Response: {response}"
        )
    except Exception as e:
        await ctx.send(f"Failed to stop server for {game_name}. Error: {str(e)}")
        logger.error(f"Failed to stop server for {game_name}. Error: {str(e)}")


@interactions.slash_command(
    name="game-info",
    description="Command to get information about a game.",
)
@slash_option(
    name="game_name",
    description="The name of the game",
    required=False,
    opt_type=OptionType.STRING,
)
async def game_info(
    ctx: interactions.SlashContext, game_name: Optional[str] = None
) -> None:
    """Slash command to get information about a game.

    Args:
        ctx (interactions.SlashContext): The context of the command.
        game_name (Optional[str], optional): The name of the game. Defaults to None.
    """
    if not game_name:
        await ctx.send(
            f"No game specified. Please provide a game name. Valid options are:\n{games_list_string}"
        )
        return

    if game_name not in featured_games:
        await ctx.send(
            f"No information available for the game: {game_name}\n Try one of the following:\n{games_list_string}"
        )
        return

    game_info: dict = featured_games.get(game_name)
    stack_name: str = game_info.get("stack_name", game_name)
    info_link: str = game_info.get("info_link", f"https://grlanparty.info/{stack_name}")
    description: str = game_info.get("description", "No description available.")
    if "server_status_url" in game_info:
        async with aiohttp.ClientSession() as session:
            async with session.get(game_info["server_status_url"]) as response:
                if response.status == 200:
                    data = await response.json()
                    server_online = data.get("result", False)
                    status_emoji = "🟢" if server_online else "🔴"
                    server_info = f"Server status: {status_emoji}\nServer URL: {game_info['stack_name']}.grlanparty.info\n"
                else:
                    server_info = "Error fetching server status.\n"
    else:
        server_info = None
        await ctx.send(
            f"**{game_name}**\nDescription: {description}\nMore info: {info_link}"
        )
    if server_info:
        await ctx.send(
            f"**{game_name}**\nDescription: {description}\n{server_info}More info: {info_link}"
        )
    else:
        await ctx.send(
            f"**{game_name}**\nDescription: {description}\nMore info: {info_link}"
        )
    logger.info(f"Game info command executed for {game_name}.")


# Start the bot client
client.start(discord_bot_client_token)
