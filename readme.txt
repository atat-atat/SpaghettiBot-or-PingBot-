PingBot is an API made by Oppy, which is meant to be a bot-version of a swiss army knife.
The PingBot API has many features and commands and even various fun features. PingBot can be used on any server, by using !join <INVITE URL>

Features -
The bot displays a typing message when commands are entered.
PingBot has a plugin system that varies from different servers.
PingBot saves each server using a JSON file, and will read the json file to load plugins/

Plugins -
Memebot - A bot that contains various memes.

Transform Commands -
!transform name <NAME> - Changes the name of the bot.
!transform nameorig - Changes the name of the bot to its original name.
!transform game <NAME> - Changes the game the bot is playing.
!transform gamenone - Sets the bot's game to none.
!transform avatar <AVATARURL> - Changes the url of the bot. (WIP)

Stat Commands -
Stats are variables that can be created via Discord, you can interact with the stat in any way.
!stat create <STAT_NAME> - Create a stat.
!stat remove <STAT_ID/STAT_NAME> - Remove a stat.
!stat rename <STAT_ID/STAT_NAME> <STAT_NAME> - Rename a stat.
!stat value <STAT_ID/STAT_NAME> <VALUE> - Sets stat value.
!stat increment <STAT_ID/STAT_NAME> <VALUE> - Increase a stat by a value.
!stat reduction <STAT_ID/STAT_NAME> <VALUE> - Decrease a stat by a value.

Calculator Commands -
!calc <VALUE> <OPERATION> <VALUE> - Uses a calculator system.
Operations -
Operations go by its name, and not its symbol. (EX: it would be 'add' and no '+')
add - Adds two values.
sub - Subtracts two values.
mult - Multiply two values.
div - Divide two values.
sqrt - Find the square root of a value.
cube - Square root two values.

Search Commands -
!images <TEXT> - Finds the top result of an image on Google Images.
!youtube <TEXT> - Finds the top result of a YouTube video on Google Images.
!wolfram <TEXT> - Finds the wolfram information of your search.

Get Commands -
!get avatar <USER_MENTION/USER_ID> - Gets the avatar of a user or the user's id.
!get info <USER_MENTION/USER_ID> - Gets the user's information.

Reputation Commands -
!rep increment <USER> <VALUE> / !+<VALUE> <USER> - Increases reputation of a user by a value.
!rep reduction <USER> <VALUE> / !-<VALUE> <USER> - Decreases reputation of a user by a value.
!rep show <USER> - Displays the amount of reputation the user has.

Default Commands -
help <COMMAND> - Displays information about a command.
author - Displays who created PingBot.
version - Displays the version information.
start-enable - Enables key commands.

Key Commands -
func - Enables fun commands.
mas - Enables an arseny of memes.
mastbot - Enables sub-bots.
gameboy - Enables chat games.
asc - Enables admin/staff commands.

Func Commands -
dice - Roll the dice.
coinflip - Flip a coin.
poke - Bug someone.
votemute - Starts a votemute against a user, you can use !y to vote yes.
say - Make the bot say something.
avatar - Displays your avatar.

Mas Commands -
kek
anotherone
youloyal
yousmart
yougenius
yougrateful
ahegao
hitler
woop
lewd
:bruh:
cumstump
cummies
stump
clap
hanginthere
no
really
gaminginequality
lmao
kappa
heybudd
funfacts
triggered
rekt
spork
goodshit
porn
gayporn
fuckbots
wordsearch
prhello

Mastbot Commands -
musicbot - Enables a music bot.
chatbot - Enables a chat bot. (WIP)
searchbot - Enables a bot that can display a result from a google image search or a YouTube video.

Gameboy Commands -
petdog - Enables a chat game where you have to feed a dog or else it will die. Throughout the game, the dog can become something else.

Asc Commands -
kick - Kicks a user. (Requires key to be on)
ban - Bans a user. (Requires key to be on)
getid - Gets the ID of a user. (Requires key to be on)
getchaninv - Gets the invite URL of the channel.

To set PingBot up, you first need to have the following installed -
discord.py
opus

Then, click on run.bat to run PingBot.
Once you start PingBot, you wont have any commands available other than the basic help, author and version commands. You will have to enable
some keys, so to enable a key, you first need to run !start-key and then key commands will be available.
You can enable some key commands, type !enable and then the key command.

CHAT STRUCTURE -

VAGUE: CATALYST-GREET - > WAIT FOR RESPONSE - > RESPOND IN CONFUSED OR PLEASANT RESPONSE BASED ON THE WORD GIVEN, THEN PROVIDE NEXT QUESTION
- > WAIT FOR RESPONSE - > RESPOND IN EAGER MANNER OR STILL PLEASANT BASED ON WORD GIVEN, THEN PROVIDE A RESPONSE BASED ON WHETHER ITS MOOD IS EAGER OR PLEASANT - >
WAIT FOR RESPONSE - > CYCLE THROUGH WHILE DECREASING MOOD VARIABLE

There are two variables -
Mood { -> The bot's mood, this Mood is then broken up into two more variables -
   Eager { -> Eager mood, also broken up.
      Annoyed  -> Annoyed mood. This mood can be very annoyed, resulting in anger, or can be midly annoyed
      Confused -> Confused mood.
   }

   Pleasant { -> Pleasant mood, also broken up.
      Happy -> Happy mood. This mood can be very happy, resulting in giddiness, or can be just happy.
      Relaxed -> Mellow mood.
   }
}

Each mood variable begins with 0.

Mood {
Eager = 0
Pleasant = 0
}

The bot will break the words down and check whether the words might contain something bad.
Bad words (not neccessarily swear words) increase Eager by 1.
Words that are nice will increase Pleasant by 1.

The more of one mood will result in tone shifts of the bot.

Advanced Map (For future) -
The bot is comprised of engines.

Engine 1: Grammar and Spelling engine, which checks whether grammar and spelling is correct. It basically shows how words are formed, and etc.
Engine 2: Original Eager and Pleasant moods but more sub-moods, resulting in emotions.
Engine 3: 