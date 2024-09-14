# TWITCH CHAT PLAYS PYTHON
simple python script to allow twitch chat to code in python
the code that twitch chat writes isnt excuted immeditaly but stored in another python file.
## Setup:
put project in folder

create venv

run `pip install -r requirements.txt`

inside the config folder create a file named .env

config/.env:
```
Client_ID = 'CLIENTID'
Token = 'TOKEN'
Bot_Prefix = '!'
Target_Channel = 'CHANNELNAME'
Target_File = 'chaos.py'
Title = 'TITLE'
```
replace `CLIENTID` with your bots client id
replace `TOKEN` with your bots Token
replace `CHANNELNAME` with your channels named
replace `TITLE` with the title that will appear at the top of the file
you can replace `chaos.py` with the name you want of the file twitch chat will be coding in

run main.py

## Commands
```
!var VARIBLENAME VARIBLEVALUE - creates a varible with name VARIBLENAME and value VARIBLEVALUE - aliases: "varible"

!comment COMMENT - creates a comment

!newline AMOUNT - creates AMOUNT of new lines or if AMOUNT is not given defaults to 1

!print THING - prints THING

!if THING1 OPERATOR THING2 - creates an if condithon - operators: "==, !=, >, <, >=, <="

!setindent INDENT - sets the current indent to INDENT if INDENT is not given will defaults to 0 - aliases: "resetindent, escapeindent, escape, si, ri"

!def FUNCNAME PARAMTERS - creates a funcithon with name FUNCNAME and paramters PARAMTERS if PARAMTERS is not given defaults to none - aliases: "createfunc, func, fun, voidstaticnull"

!runfunc FUNCNAME PARAMTERS - runs funcithon FUNCNAME with paramters PARAMTERS if PARAMTERS is not given will default to none - aliases: "run, start, use"

!while THING1 OPERATOR THING2 - creates a while loop - operators: "==, !=, >, <, >=, <="

!math THING1 OPERATOR THING2 - creates a math statment will save result in THING1 - aliases: "calc, mathmatics, oneplusone" - operators: "_+, -, *, /, %, \*\*, //_"
```
