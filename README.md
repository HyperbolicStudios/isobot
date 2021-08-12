# ISO Bot

## Functionality

This bot does a few things: first, it stores in a database every post in games A, B, and C. Updates to the database are done every three hours, and typically takes under 10 minutes. Second, the bot collects posts and generates ISOs on command. The bot is also capable of generating ISOs for all players at once (if a mod wants to post links to every ISO at EoD, for instance) and can also generate ISOs restricted to page ranges.

# Assistance and setup

Note that the letter "X" in any command refers to the game you are analyzing - be it A, B, or C. (case-sensitive)

`$iso help` - prints this help message

`$iso info` - prints a summary of information stored in the databases, including URLs and number of posts stored.

`$isoX url <url>` - sets the URL of game X.

`$isoX wipe` - wipes the stored posts of game X. Useful if there's been a screwup of some kind, such as the bot missing a page.

## Retrieving ISOs

`$isoX <player name>` - generates a single ISO of player <player name> from game X exclusively. Link should persistent for one hour.
  
`$isoX name range:Y,Z` - generates a single ISO of player <player name> from game X, listing every post from page Y to page Z. Don't forget the comma.

`$isoX all` - posts links to ISOs of every single player in game X. Link should persist for one day.

## Updating the database
By default, the databases are updated every three hours. The bot is unresponsive during updates.

`$isoX updates on` - turns on the automatic updates

`$isoX updates off` - turns off the automatic updates

`$isoX update` - manually updates a database. Do not overuse this command.


## Channel visibilities
`$iso vis on` - gives read/write privileges to every discord user with the default role.

`$iso vis off` - removes read/write privileges for players that do not have special permissions.




All messages must be entered in the #iso-bot channel.
