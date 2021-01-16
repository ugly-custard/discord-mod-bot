# dunno-man-I-m-bad-at-naming
a discord mod bot with logging features, mod commands, youtube upload notifications, and some random crappy commands

# commands

```
AutoReply:
  ARadd     m:ARadd <trigger> | <reply> --> to add an auto reply trigger
  ARdisplay m:ARdisplay --> to display triggers and their replies
  ARremove  m:ARremove <trigger> --> to remove a trigger
  bully     m:bully --> sends an image saying 'no bully'
  insult    m:insult --> get insulted cuz why not
  welcome   m:welcome --> sends an image welcoming new users
  whyis     m:whyis <user mention> --> why is you...?
Moderation:
  avatar    m:av --> sends the avatar of a user and a link to it
  ban       m:ban <user mention>/<userID> [reason] --> bans a user
  kick      m:kick <user mention>/<userID> [reason] --> kicks a user
  purge     m:purge --> purges the chat
  roleinfo  m:roleinfo --> gives info on a role
  softban   m:softban <user mention>/<userID> [reason] --> softbans a user
  unban     m:unban <userID> [reason] --> unbans a user
  whois     m:whois --> gives info on a user
mutes:
  mute      m:mute <user mention>/<userID> <time> [reason] --> mutes a member
  mutes     m:mutes [user mention]/[userID] --> gives a list of muted members, gives a description on the mute if passed a muted user's ID
  unmute    m:unmute <user mention>/<userID> --> unmutes a user
No Category:
  help      Shows this message
  load      m:load --> only for me to load the cogs | change the userID in the check in the main file to whatever you want
  reload    m:reload --> only for me to reload cogs
  unload    m:unload --> only for me to unload cogs
```

# To host it yourself
Just change the CONSTANTS file to whatever you want, change the userID in the if check in the main file to whoever's userID you want

I host the bot on heroku, with heroku-postgres as the databse. Just connect a database to your app on heroku and deploy the code with necessary changes and you're good to go!

Do whatever the fuck you want with the code just give me credits :flushed:
