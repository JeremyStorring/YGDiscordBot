import load
import discord
from discord.ext import commands

initial_extensions = ['cogs.moderation', 'cogs.errorHandler']
configData = load.loadConfigData()

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    prefixes = ['&']

    # Check if message is DMs
    if not message.guild:
        return '&'

    return commands.when_mentioned_or(*prefixes)(bot, message)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)


class embededHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)


bot.help_command = embededHelp()

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # await bot.change_presence(game=discord.Game(name='Cogs Example', type=1, url='https://twitch.tv/kraken'))
    print(f'Successfully logged in and booted...!')

bot.run(configData['TOKEN'], bot=True, reconnect=True)

