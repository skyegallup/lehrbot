from discord.guild import Guild
from discord.member import Member


async def makeclass(caller: Member, channel, name: str) -> None:
    # check if caller has admin perms
    if not caller.guild_permissions.administrator:
        await channel.send(
            caller.mention + " You must be an administrator "
                             "to call this command."
        )

    guild: Guild = caller.guild
    await guild.create_role(
        name=name,
        mentionable=True,
        reason="Requested by " + caller.mention
    )
