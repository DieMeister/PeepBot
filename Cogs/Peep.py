import datetime
from datetime import datetime as dt, timedelta

from discord import app_commands, Member
from discord.ext import commands

import sqlite3
from typing import TYPE_CHECKING, Optional
from random import randint, choice

import lib
from lib import logging, get, embed
from lib.logging import Module, ExecutionMethod, CommandType

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context


class Peep(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logging.extension_success(Module.PEEP, "Cog initialised", ExecutionMethod.SETUP, "Peep")

    @commands.command()
    async def psps(self, ctx: "Context") -> None:
        timestamp = dt.now(datetime.UTC)

        # get the data of the guild and create a new entry if it doesn't exist
        lib.sql.add_guild(ctx.guild)
        guild = lib.sql.get_guild(ctx.guild.id)
        guild_last_try = get.dt_object(guild[4])

        # check if the used channel is valid
        channel = lib.sql.get_channel(ctx.channel.id)
        if not channel:
            logging.psps_denied(ctx, "Outside of allowed Channel")
            return

        # get the data of the member and create a new entry if it doesn't exist
        lib.sql.add_member(ctx.author)
        member = lib.sql.get_member(ctx.guild.id, ctx.author.id)
        member_last_try = get.dt_object(member[2])
        member_peeps = member[3]
        member_tries = member[4]

        # check if someone else tried within a minute
        if guild_last_try + timedelta(minutes=1) > timestamp:
            logging.psps_denied(ctx, "Within 1 minute of another member")
            return

        # check if the member tried again within their cooldown
        if ctx.author.id in lib.get.vip():
            if member_last_try + timedelta(minutes=5) > timestamp:
                logging.psps_denied(ctx, "vip used twice within 5 minutes")
                return
        elif ctx.author.id in lib.get.vup():
            if member_last_try + timedelta(minutes=30) > timestamp:
                logging.psps_denied(ctx, "vup used twice within 30 minutes")
                return
        elif member_last_try + timedelta(minutes=10) > timestamp:
            logging.psps_denied(ctx, "member used twice within 10 minutes")
            return

        member_tries += 1
        peep_number = randint(1, 7)
        if peep_number == 1:
            steal_number = randint(1, 100)
            # steal peep
            if steal_number == 1:
                mod = choice(lib.get.thieves())
                name = mod["name"]
                emote = mod["emote"]
                user_id = mod["id"]
                await ctx.reply(f"{emote} your peep got stolen")
                data_db = sqlite3.connect(get.database_path())
                stolen_peeps = data_db.execute("""
                SELECT stolen_peeps
                FROM users
                WHERE user_id = ?
                """, (user_id,)).fetchone()[0]
                if stolen_peeps is None:
                    stolen_peeps = 0
                data_db.execute("""
                UPDATE users
                SET stolen_peeps = ?
                WHERE user_id = ?
                """, ((stolen_peeps + 1), user_id))
                data_db.commit()
                data_db.close()
                logging.steal_peep(ctx, name, emote)
            # give member a peep
            else:
                member_peeps += 1
                await ctx.reply(f"{guild[1]} You have {member_peeps} peeps now")
                logging.catch_peep("Member got a Peep", ctx, member_peeps, peep_number)
        # scratch member
        elif peep_number == 2 or peep_number == 3:
            await ctx.reply(guild[2])
            logging.catch_peep("Member got scratched", ctx, member_peeps, peep_number)
        # don't get a peep
        else:
            await ctx.reply(guild[3])
            logging.catch_peep("Member did not get a Peep", ctx, member_peeps, peep_number)

        # update database
        con = sqlite3.connect(lib.get.database_path())
        con.execute("""
        UPDATE guilds
        SET last_peep = ?
        WHERE guild_id = ?
        """, (get.dt_string(timestamp), ctx.guild.id))
        con.execute("""
        UPDATE members
        SET
            last_peep = ?,
            caught_peeps = ?,
            tries = ?
        WHERE guild_id = ? AND user_id = ?
        """, (get.dt_string(timestamp), member_peeps, member_tries, ctx.guild.id, ctx.author.id))
        con.commit()
        con.close()

    @app_commands.command(name="leaderboard", description="shows the 10 Members with the most Peeps")
    async def leaderboard(self, interaction: "Interaction") -> None:
        connection = sqlite3.connect(lib.get.database_path())
        top_10 = connection.execute("""
           SELECT
               user_id,
               caught_peeps,
               tries,
               sent_peeps,
               received_peeps
           FROM
               members
           WHERE
               guild_id = ?
           AND
               caught_peeps > 0
           ORDER BY
               caught_peeps DESC,
               user_id ASC
           LIMIT 10
           """, (interaction.guild_id,)).fetchall()

        if len(top_10) == 0:
            await interaction.response.send_message("nobody got a peep yet")
            logging.command(Module.PEEP, "Leaderboard sent", interaction, CommandType.MEMBER)
        else:
            await interaction.response.send_message(embed=embed.leaderboard(interaction.guild, top_10))
            logging.command(Module.BOT, "Leaderboard sent", interaction, CommandType.MEMBER)

    @app_commands.describe(
        member="The Member whose rank you want to know"
    )
    @app_commands.command(name="rank", description="shows your peeps and total tries")
    async def rank(self, interaction: "Interaction", member: Optional[Member]=None) -> None:
        if member is None:
            member = interaction.user
        lib.sql.add_member(member)

        data_db = sqlite3.connect(lib.get.database_path())
        peeps, tries, sent, received = data_db.execute("""
           SELECT
               caught_peeps,
               tries,
               sent_peeps,
               received_peeps
           FROM
               members
           WHERE
               guild_id = ?
           AND
               user_id = ?
           """, (interaction.guild_id, member.id)).fetchone()
        await interaction.response.send_message(embed=embed.rank(member, str(tries), str(peeps), str(sent), str(received)))
        logging.rank(interaction, member.id)

    @app_commands.describe(
        amount="The number of Peeps you want to transfer. 0 < amount <= your peeps",
        recipient="The Member who gets your Peeps"
    )
    @app_commands.command(name="transfer_peeps", description="Gives a set amount of Peeps from you to another Member")
    async def transfer_peeps(self, interaction: "Interaction", amount: int, recipient: Member) -> None:
        if amount <= 0:
            await interaction.response.send_message("You need to transfer at least 1 Peep")
            logging.peep_transfer("Member tried to transfer < 1 Peeps", interaction, amount, recipient.id)
            return
        lib.sql.add_member(interaction.user)
        con = sqlite3.connect(lib.get.database_path())
        sender_total_peeps, sender_sent_peeps = con.execute("""
        SELECT
            caught_peeps,
            sent_peeps
        FROM members
        WHERE guild_id = ?
        AND user_id = ?
        """, (interaction.guild_id, interaction.user.id)).fetchone()
        if amount > sender_total_peeps:
            con.close()
            await interaction.response.send_message("You don't have that many Peeps to transfer")
            logging.peep_transfer("Member tried to transfer more Peeps than they have", interaction, amount, recipient.id, sender_total_peeps)
            return
        lib.sql.add_member(recipient)
        receiver_total_peeps, receiver_received_peeps = con.execute("""
        SELECT caught_peeps, received_peeps
        FROM members
        WHERE guild_id = ?
        AND user_id = ?
        """, (interaction.guild_id, recipient.id)).fetchone()

        # update receiving Member
        con.execute("""
        UPDATE members
        SET 
            caught_peeps = ?,
            received_peeps = ?
        WHERE guild_id = ?
        AND user_id = ?
        """, ((receiver_total_peeps + amount), (receiver_received_peeps + amount), interaction.guild_id, recipient.id))
        # update sending Member
        con.execute("""
        UPDATE members
        SET
            caught_peeps = ?,
            sent_peeps = ?
        WHERE guild_id = ?
        AND user_id = ?;
        """, ((sender_total_peeps - amount), (sender_sent_peeps + amount), interaction.guild_id, interaction.user.id))
        con.commit()
        con.close()
        await interaction.response.send_message(f"You transferred {amount} Peeps to <@{recipient.id}>")
        logging.peep_transfer("Member transferred Peeps to another Member", interaction, amount, recipient.id, sender_total_peeps, receiver_total_peeps)


async def setup(bot) -> None:
    await bot.add_cog(Peep(bot))
