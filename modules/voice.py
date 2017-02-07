import discord
from discord.ext import commands


class Voice():
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ref_voice(self, ctx, response: str = None):
        currentUser = ctx.message.author.name
        server = ctx.message.server
        for user in server.members:
            if user.name == currentUser:
                current_member = user

        string = ""
        for user in current_member.voice_channel.voice_members:
            string = string + user.mention + " "

        em = discord.Embed(description=string, timestamp=ctx.message.timestamp)

        await self.bot.say(string + " " + response)
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Voice(bot))