import discord, load
from discord.ext import commands
import helperFunctions

memberKickText = load.loadConfigData()["MEMBER_KICK_TEXT"]
memberPingText = load.loadConfigData()["MEMBER_PING_TEXT"]


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.has_any_role('Admin', 'Owner', 'Moderator')
    async def killBot(self, ctx):
        exit(0)

    @commands.command(
        brief="Verify members",
        description="Verify members by supplying command name + member ID or @member + MM/DD/YYYY format"
    )
    @commands.has_guild_permissions(manage_roles=True)
    async def verify(self, ctx, member: discord.Member, dateOfBirth):
        if not helperFunctions.overAge18(dateOfBirth):
            await ctx.reply("This user is not over the age of 18. Please remove them from the server")
        else:
            await member.add_roles(ctx.guild.get_role(708670870549168218))
            await member.remove_roles(ctx.guild.get_role(708671339820613743))
            channel = ctx.guild.get_channel(770382946011578420)
            await channel.send(str("<@" + str(member.id) + "> verified " + dateOfBirth))

    @commands.command()
    async def testPing(self, ctx, member: discord.Member):
        await ctx.channel.send(f"Hello {member.mention}! " + memberPingText)

    @commands.command(
        brief="Ping unverified members",
        description="Pings **ALL** members who have the unverified role."
    )
    @commands.has_guild_permissions(ban_members=True)
    async def pingUnverified(self, ctx):
        membersToPing = []
        for member in ctx.guild.members:
            for role in member.roles:
                if role.id == 708671339820613743:
                    membersToPing.append(member)
        count = 0
        for member in membersToPing:
            await ctx.channel.send(f"Hello {member.mention}! " + memberPingText)
            percentComplete = count/len(membersToPing)
            print(str(round(percentComplete * 100, 1)) + "%")
            count += 1

    @commands.command()
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    async def kickUnverified(self, ctx):
        membersToKick = []
        for member in ctx.guild.members:
            for role in member.roles:
                if role.id == 708671339820613743:
                    membersToKick.append(member)
        for member in membersToKick:
            if await self.sendTestMessage(member):
                await member.send(memberKickText)
                print("Message has been sent to user")
            await member.kick(reason=memberKickText)
            await ctx.channel.send(f' {member} ({member.id}) has been kicked for remaining unverified')
            print(member, "has been kicked")

    @commands.command(
        brief="Kick member",
        description="This command kicks the tagged member (or member ID). Must have kick permissions."
    )
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason="none"):
        await member.kick(reason=reason)

    @commands.command(
        brief="Ban member",
        description="This command bans the tagged member (or member ID). Must have ban permissions."
    )
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason="none"):
        await member.ban(reason=reason)

    @verify.error
    async def verify_error(self, ctx, error: commands.CommandError):
        print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permission to run this command!")
        else:
            await ctx.reply("Please include the users date of birth (MM/DD/YYYY)")

    @pingUnverified.error
    async def pingUnverified_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permission to run this command!")

    @kick.error
    async def kick_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permission to kick this person!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(error)

    @ban.error
    async def ban_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permission to ban this person!")

        print(helperFunctions.overAge18('05/18/1999'))

    async def sendTestMessage(self, member: discord.Member):
        try:
            await member.send()
        except discord.HTTPException as e:
            if e.code == 50006:
                return True
            elif e.code == 50007:
                return False
            else:
                raise

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(ModerationCog(bot))