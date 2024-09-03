import os
from twitchio.ext import commands
from json import load, dump
from warnings import warn
from dotenv import load_dotenv
from inspect import signature

class Config():
    def __init__(self, configFileName, default) -> None:
        self.configFileName = configFileName
        self.default = default
        if not os.path.exists(self.configFileName):
            if input(f'Config File {self.configFileName} Not Found would you like for it to be created?(Y,N): ').lower() == 'y':
                open(self.configFileName, 'x').close()
                self.reset()
            else: return False
        else:
            configFile = open(self.configFileName, 'r')
            config = load(configFile)
            configFile.close()
            if config != self.default:
                keys = list(config.keys())
                values = list(config.values())
                print(
                    f'Config File {self.configFileName} is not Empty\nIt Contains the Following:')
                for i in range(len(config)):
                    print(f'{keys[i]}: {values[i]}')
                if input('Would you like to Empty it?(Y,N): ').lower() == 'y':
                    self.reset()

    def readConfig(self) -> dict:
        configFile = open(self.configFileName, 'r')
        config = load(configFile)
        configFile.close()
        return config

    def setConfig(self, key: str, value, config: dict = None):
        if not config:
            configFile = open(self.configFileName, 'r')
            config = load(configFile)
            configFile.close()
        configFile = open(self.configFileName, 'w')
        config[key] = value
        dump(config, configFile)
        configFile.close()
        return config

    def appendConfigArray(self, array: list, item):
        if not self.exists(array):
            warn('ERROR ARRAY NOT FOUND', stacklevel=2)
            return
        config = self.readConfig()
        if type(config[array]) == list and not item in config[array]:
            config[array].append(item)
            self.setConfig(array, config[array], config)
            return config
        elif not type(config[array]) == list:
            warn(f'PLEASE SEND ARRAY NOT {type(config[array])}', stacklevel=2)
        else:
            return

    def exists(self, key):
        try:
            self.readConfig()[key]
            return True
        except KeyError:
            return False

    def reset(self):
        configFile = open(self.configFileName, 'w')
        dump(self.default, configFile)
        configFile.close()


class Bot(commands.Bot):

    def __init__(self):
        print('BEGINNING CONFIG SETUP')
        self.defaultConfig = {
            "varibleNames": [],
            "funcithonNames": [],
            "importNames": [],
            "currentIndent": 0
        }
        try:
            self.config = Config(
                configFileName='config/betterconfig.json', default=self.defaultConfig)
            load_dotenv(dotenv_path='./config/.env')
        except TypeError:
            print('NO CONFIG FILE EXISTING PROGRAM')
            return False
        super().__init__(
            token=os.environ['Token'],
            client_id=os.environ['Client_ID'],
            prefix=os.environ['Bot_Prefix'],
            initial_channels=[os.environ['Target_Channel']]
        )
        self.targetFile = os.environ['Target_File']
        self.title = '# '+os.environ['Title']
        print('CONFIG SETUP COMPLETE')
        print('BEGINNING FILE SETUP')
        if not os.path.exists(self.targetFile):
            if input(f'File {self.targetFile} Not Found would you like for it to be created?(Y,N): ').lower() == 'y':
                codeFile = open(self.targetFile, 'x')
                codeFile.write(self.title)
                codeFile.close()
            else:
                return False
        else:
            codeFile = open(self.targetFile, 'r')
            code = codeFile.read()
            codeFile.close()
            if code != self.title:
                if len(code) <= 0 or input(f'File {self.targetFile} is not Empty Would you like it to empty it?(Y,N): ').lower() == 'y':
                    codeFile = open(self.targetFile, 'w')
                    codeFile.write(self.title)
                    codeFile.close()
        print('FILE SETUP COMPLETE')

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You're missing an argument. View !help")

    @commands.command(name='var', aliases=('varible'))
    async def var(self, ctx: commands.Context, varName: str, *, varValue: str):
        """Create a Varible"""
        varValue = self.autoString(varValue)
        varName = self.nameCorrecter(varName)
        self.writeToCode(f'{varName}={varValue}', userCredits=ctx.author.name)
        self.config.appendConfigArray('varibleNames', varName)
        await ctx.send(f'{varName}={varValue}')

    @commands.command(name='comment')
    async def comment(self, ctx: commands.Context, *, comment: str):
        """Create a Comment"""
        self.writeToCode(f'# {comment} written by {ctx.author.name}')
        await ctx.send(f'# {comment}')

    @commands.command(name='newline')
    async def newLine(self, ctx: commands.Context, *, amount: int = 1):
        """Create a NewLine"""
        self.writeToCode('\n'*amount)
        if amount == 1:
            await ctx.send(f'added {amount} new line')
        else:
            await ctx.send(f'added {amount} new lines')

    @commands.command(name='print')
    async def printer(self, ctx: commands.Context, *, text: str):
        """Create a print statment"""
        if not text in self.config.readConfig()['varibleNames']:
            text = self.autoString(text)
        self.writeToCode(f'print({text})', userCredits=ctx.author.name)
        await ctx.send(f'print({text})')

    @commands.command(name='if')
    async def ifCreator(self, ctx: commands.Context, thing1: str, operator: str, thing2: str):
        """Create a if statment"""
        operators = ['==', '!=', '>', '<', '>=', "<="]
        if operator in operators:
            if not thing1 in self.config.readConfig()['varibleNames']:
                thing1 = self.autoString(thing1)
            if not thing2 in self.config.readConfig()['varibleNames']:
                thing2 = self.autoString(thing2)
            self.writeToCode(
                f'if {thing1} {operator} {thing2}:', userCredits=ctx.author.name)
            self.config.setConfig(
                'currentIndent', self.config.readConfig()['currentIndent']+1)
            await ctx.send(f'if {thing1} {operator} {thing2}:')
        else:
            await ctx.send(f'operator {operator} is invalid, allowed operators: {", ".join(operators)}')

    @commands.command(name='setindent', aliases=('resetindent', 'escapeindent', 'escape', 'si', 'ri'))
    async def setIndent(self, ctx: commands.Context, indent: int = 0):
        """set the Indent"""
        self.config.setConfig('currentIndent', indent)
        self.writeToCode(f'# {ctx.author.name} set Indent to {indent}')
        await ctx.send(f'set Indent to {indent}')

    @commands.command(name='def', aliases=('createfunc', 'func', 'fun', 'voidstaticnull'))
    async def createFunc(self, ctx: commands.Context, funcname: str, *, paramters: str = ''):
        """Create a Funcithon"""
        paramters = paramters.split(' ')
        for i, paramter in enumerate(paramters):
            paramters[i] = self.nameCorrecter(paramter)
            self.config.appendConfigArray('varibleNames', paramter)
        self.writeToCode(f'def {funcname}({", ".join(paramters)}):', userCredits=ctx.author.name)
        self.config.setConfig(
            'currentIndent', self.config.readConfig()['currentIndent']+1)
        self.config.appendConfigArray('funcithonNames', funcname)

        await ctx.send(f'def {funcname}({", ".join(paramters)}):')

    @commands.command(name='runfunc', aliases=('run', 'start', 'use'))
    async def runFunc(self, ctx: commands.Context, funcname: str, *, paramters: str = ''):
        """Run a Funcithon"""
        config = self.config.readConfig()
        if funcname in config['funcithonNames']:
            paramters = paramters.split(' ')
            for i, paramter in enumerate(paramters):
                if not paramter in config['varibleNames']:
                    paramters[i] = self.autoString(paramter)
            self.writeToCode(f'{funcname}({", ".join(paramters)})', userCredits=ctx.author.name)
            await ctx.send(f'{funcname}({", ".join(paramters)})')
        else:
            await ctx.send(f'funcithon {funcname} is invalid use one of the existing funcithons or create your own with !def, existing funcithons: {", ".join(config["funcithonNames"])}')

    @commands.command(name='while')
    async def whileCreator(self, ctx: commands.Context, thing1: str, operator: str, thing2: str):
        """Create a While Loop"""
        operators = ['==', '!=', '>', '<', '>=', "<="]
        if operator in operators:
            if not thing1 in self.config.readConfig()['varibleNames']:
                thing1 = self.autoString(thing1)
            if not thing2 in self.config.readConfig()['varibleNames']:
                thing2 = self.autoString(thing2)
            self.writeToCode(
                f'while {thing1} {operator} {thing2}:', userCredits=ctx.author.name)
            self.config.setConfig(
                'currentIndent', self.config.readConfig()['currentIndent']+1)
            await ctx.send(f'while {thing1} {operator} {thing2}:')
        else:
            await ctx.send(f'operator {operator} is invalid, allowed operators: {", ".join(operators)}')
    @commands.command(name='math', aliases=('calc','mathmatics','oneplusone'))
    async def mathCreator(self, ctx: commands.Context, thing1: str, operator: str, thing2: str):
        """Create a Math Statment with the result going to thing1"""
        operators = ['+', '-', '*', '/', '%', "**", "//"]
        config = self.config.readConfig()
        if thing1 in config['varibleNames']:  
            if operator in operators:
                if not thing2 in config['varibleNames']:
                    thing2 = self.autoString(thing2)
                self.writeToCode(
                    f'{thing1} = {thing1} {operator} {thing2}', userCredits=ctx.author.name)
                await ctx.send(f'{thing1} = {thing1} {operator} {thing2}')
            else:
                await ctx.send(f'operator {operator} is invalid, allowed operators: {", ".join(operators)}')
        else:
            await ctx.send(f'thing1 must be a varible {thing1} is not an varible you can create a new one or use any of the prexisting ones, existing varibles: {", ".join(config["varibleNames"])}')
    @commands.command(name='help')
    async def helpy(self, ctx: commands.Context):
        """Display this help message."""
        for command_name, command_obj in self.commands.items():
            cmd_signature = signature(command_obj._callback)
            params = " ".join([f"<{param}>" for param in cmd_signature.parameters if param not in ['self', 'ctx']])
            command_help = f"!{command_name} {params} - {command_obj._callback.__doc__}"
            
            # Send each command's help message individually
            await ctx.send(command_help)
    def autoString(self, string: str) -> str:
        string = string.replace("'", "")
        string = string.replace('"', "")
        if string.lower() == "true" or string.lower() == "false":
            return string.capitalize()
        try:
            float(string)
            return string
        except ValueError:
            return '"' + string + '"'

    def nameCorrecter(self, name):
        extraCharcters = "{}'"
        for problematicCharcter in f'./,;[]{extraCharcters}(\ `~?><:|"!@#$%^&*()':
            name = name.replace(problematicCharcter, '')
        integerlessname = list(name)
        for i, char in enumerate(name):
            if self.isInteger(char):
                integerlessname[i] = ''
            else:
                break
        return ''.join(integerlessname)

    def isInteger(self, x: str):
        try:
            int(x)
            return True
        except ValueError:
            return False

    def writeToCode(self, text, indents=True, addnewLine=True, userCredits: str = None):
        global currentIndent
        code = open(self.targetFile, 'a')
        prefix = ''
        sufix = ''
        if indents:
            prefix = "\t" * self.config.readConfig()['currentIndent']
        if addnewLine:
            prefix = '\n'+prefix
        if userCredits:
            sufix = sufix + f"\t# added by {userCredits}"
        code.write(f'{prefix}{text}{sufix}')
        code.close()


try:
    bot = Bot()
    bot.run()
except TypeError as e:
    print('NO FILE CLOSING PROGRAM')
