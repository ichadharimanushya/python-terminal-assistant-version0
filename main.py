import commands as cmd
from commands import Assistant
import json

json_path = "data.json" #json path

name = input("Enter name of the user:\n>").lower()

try:
    with open(json_path, 'r') as f:
        data = json.load(f)
        if name not in data["users"]:
            data["users"][name] = {
                "name" : name,
                "count" : 0,
                "todos" : [],
                "history" : {}
                }
            print("--New user created--")
    with open(json_path, 'w') as f:
            json.dump(data, f, indent = 4)
            
except Exception as e:
    data = {
        "users" : {
            name : {
                "name" : name,
                "count" : 0,
                "todos" : [],
                "history" : {}
            }
        }
    }
    with open(json_path, 'w') as f:
        json.dump(data, f, indent = 4)
    print("--New user created--")

bot = Assistant(name)

# to initialize commands from a single block and not adding () yet to stop them from executing until required
"""inbuilt_Commands = {
    "time" :bot.ctime,
    "date" :bot.cdate,
    "clear" :bot.clear,
    "quote" :bot.quote,
    "rename" :bot.rename,
    "notes" :bot.notes,
    "note" :bot.note,
    "todo" :bot.todo,
    "todos" :bot.todos,
    "removetodo" :bot.removetodo,
    "searchnote" :bot.searchnote,
    "calc" :bot.calc,
    "searchtodo" :bot.searchtodo,
    "joke" :bot.joke,
    "stats" :bot.stats,
    "weather" :bot.weather,
    "fact" :bot.fact,
    "timer" :bot.timer,
    "users" : bot.users,
    "createuser" : bot.createuser,
}"""
inbuilt_Commands = [
    "time",
    "date",
    "clear",
    "quote",
    "rename",
    "notes",
    "note",
    "todo",
    "todos",
    "removetodo",
    "searchnote",
    "calc",
    "searchtodo",
    "joke",
    "stats",
    "weather",
    "fact",
    "timer",
    "users",
    "createuser",
    "deleteuser"
]

extras = ["switchuser",
          "history",
          "usage",
          "help",
          "exit"]



print("\n======WELCOME======\n")
while True:
    print()
    command = input("> ").strip() # to remove the trailing and leading spaces in the command to remove error
    if not command: continue

    parts = command.split()
    user = parts[0].lower()
    arg = " ".join(parts[1:])

    
    if user in inbuilt_Commands:
        getattr(bot, user)(arg) # bot.user(arg)
        bot.record_command(user)

    elif user in ["hi", "hello", "yo", "hola"]:
        bot.hello()
        
    elif user == "exit":
        print("\n======GOODBYE======\n")
        break

    elif user == "help":
        for command in inbuilt_Commands:
            print(command)
        for command in extras:
            print(command)

    elif user == "usage":
        print(f"You have entered {bot.data["count"]} commands.")

    elif user == "history":
        history_ = bot.data["history"].copy() #without .copy(), history_ and history refers to the same object (reference the same dictionary)
        while history_:
            maximum = max(history_, key=history_.get) #returns the key with maximun value in a dictionary
            print(f"{maximum} : {history_[maximum]}")
            del history_[maximum]

    elif user == "switchuser":
        if bot.switchuser(arg):
            arg_ = arg.strip().lower()
            bot = Assistant(arg_)
            print("--Switched Successfully--")

    else:
        print("Unknown command")

