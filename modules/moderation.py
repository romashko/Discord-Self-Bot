import discord
from discord.ext import commands


def embeds_allowed(message):
    return message.channel.permissions_for(message.author).embed_links


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    # Banning and Kicking commands

    # Bans a member
    @commands.command()
    async def ban(self, member: discord.Member = None):
        """Bans a member
        User must have ban member permissions"""
        # Are they trying to ban nobody? Are they stupid?
        # Why do they have mod powers if they're this much of an idiot?
        if member is None:
            return
        # Is the person being banned me? No we don't allow that
        elif member.id == '95953002774413312':
            await self.bot.say("http://i.imgur.com/BSbBniw.png")
            return
        # Bans the user
        await self.bot.ban(member, delete_message_days=1)
        # Prints to console

    # Kicks a member
    @commands.command()
    async def kick(self, member: discord.Member = None):
        """Kicks a member
        User must have kick member permissions"""
        # Same as above, are they stupid
        if member is None:
            return
        # Still not allowed to kick me
        elif member.id == '95953002774413312':
            await self.bot.say("http://i.imgur.com/BSbBniw.png")
            return
        # Kicks the user
        await self.bot.kick(member)
        # Prints to console

    # Information commands
    # Server info and member info

    # Gives the user some basic info on a user
    @commands.command(pass_context=True, no_pm=True, aliases=['memberinfo', 'meminfo', 'membinfo',
                                                              'member', 'userinfo', 'user'])
    async def info(self, ctx, member: discord.Member = None):
        """Information on a user"""
        if member is None:
            member = ctx.message.author
        rolelist = []
        for elem in member.roles:
            rolelist.append(elem.name)
        em = discord.Embed(title=member.nick, colour=member.colour)
        em.add_field(name="Name", value=member.name)
        em.add_field(name="Joined server", value=member.joined_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="ID", value=member.id)
        em.add_field(name="Has existed since", value=member.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Color", value=member.colour)
        em.add_field(name="Bot?", value=str(member.bot).replace("True", "✔").replace("False", "❌"))
        em.add_field(name="Server perms", value="[" + str(
            member.server_permissions.value) + "](https://discordapi.com/permissions.html#" + str(
            member.server_permissions.value) + ")")
        em.add_field(name="Roles", value="\n".join([str(x) for x in rolelist]), inline=False)
        em.set_image(url=member.avatar_url)
        em.set_thumbnail(url="https://xenforo.com/community/rgba.php?r=" + str(member.colour.r) + "&g=" + str(
            member.colour.g) + "&b=" + str(member.colour.b) + "&a=255")
        if embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say("```\n" +
                               "Name: "+member.name +
                               "\nJoined server: "+member.joined_at.strftime('%d.%m.%Y %H:%M:%S %Z') +
                               "\nID: "+member.id +
                               "\nHas existed since: "+member.created_at.strftime('%d.%m.%Y %H:%M:%S %Z') +
                               "\nColor: "+str(member.color) +
                               "\nBot?: "+str(member.bot).replace("True", "✔").replace("False", "❌") +
                               "\nServer perms: "+str(member.server_permissions.value) +
                               "\nRoles: "+"\n".join([str(x) for x in rolelist]) +
                               "```\n" +
                               member.avatar_url)
        await self.bot.delete_message(ctx.message)

    # Server Info
    @commands.command(pass_context=True, no_pm=True, aliases=['servinfo', 'serv', 'sv'])
    async def serverinfo(self, ctx, server: str = None):
        """Shows server information"""
        if server is None:
            server = ctx.message.server
        else:
            server = self.bot.get_server(server)
        if server is None:
            await self.bot.say("Failed to get server with provided ID")
            await self.bot.delete_message(ctx.message)
            return
        afk = server.afk_timeout / 60
        vip_regs = str("VIP_REGIONS" in server.features).replace("True", "✔").replace("False", "❌")
        van_url = str("VANITY_URL" in server.features).replace("True", "✔").replace("False", "❌")
        inv_splash = "INVITE_SPLASH" in server.features
        em = discord.Embed(title="Server info", colour=server.owner.colour)
        em.add_field(name="Name", value=server.name)
        em.add_field(name="Server ID", value=server.id)
        em.add_field(name="Region", value=server.region)
        em.add_field(name="Existed since", value=server.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Owner", value=server.owner)
        em.add_field(name="AFK Timeout and Channel", value=str(afk) + " min in " + str(server.afk_channel))
        em.add_field(name="Verification level",
                     value=str(server.verification_level).replace("none", "None").replace("low", "Low").replace(
                         "medium", "Medium").replace("high", "(╯°□°）╯︵ ┻━┻"))
        em.add_field(name="2FA admins", value=str(server.mfa_level).replace("0", "❌").replace("1", "✔"))
        em.add_field(name="Member Count", value=server.member_count)
        em.add_field(name="Role Count", value=str(len(server.roles)))
        em.add_field(name="Channel Count", value=str(len(server.channels)))
        em.add_field(name="VIP Voice Regions", value=vip_regs)
        em.add_field(name="Vanity URL", value=van_url)
        if not inv_splash:
            em.add_field(name="Invite Splash", value="❌")
        elif server.splash_url == "":
            em.add_field(name="Invite Splash", value="✔")
        else:
            em.add_field(name="Invite Splash", value="✔ [🔗](" + server.splash_url + ")")
        em.set_image(url=server.icon_url)
        if embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say("```\n" +
                               "Name: "+server.name +
                               "\nServer ID: "+server.id +
                               "\nRegion: "+str(server.region) +
                               "\nExisted since: "+server.created_at.strftime('%d.%m.%Y %H:%M:%S %Z') +
                               "\nOwner: "+str(server.owner) +
                               "\nAFK timeout and Channel: "+str(afk) + " min in " + str(server.afk_channel) +
                               "\nVerification level: " +
                               str(server.verification_level).replace("none", "None").replace("low", "Low")
                               .replace("medium", "Medium").replace("high", "(╯°□°）╯︵ ┻━┻") +
                               "\n2FA admins: "+str(server.mfa_level).replace("0", "❌").replace("1", "✔") +
                               "\nMember Count: "+str(server.member_count) +
                               "\nRole Count: "+str(len(server.roles)) +
                               "\nChannel Count: "+str(len(server.channels)) +
                               "\nVIP Voice Regions: "+vip_regs +
                               "\nVanity URL: "+van_url +
                               "\nInvite Splash: "+str(inv_splash).replace("True", "✔").replace("False", "❌") +
                               "\nInvite Splash URL: "+server.splash_url +
                               "```\n" +
                               server.icon_url)
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Moderation(bot))
