from datetime import datetime
import os
import random
import json
import urllib.request
import time

facturl = "https://uselessfacts.jsph.pl/api/v2/facts/random"
jokeurl  = "https://official-joke-api.appspot.com/random_joke"
json_path = "data.json" #json path
notefile = "notes.txt" #notefile path


quotes = ["You are much bigger than the challenges you face.",
          "Sometimes it is better to be quite, even if you lose the argument.",
          "We suffer more in our mind than we do in real life."]



class Assistant:
    def __init__(self, name):
        self.name = name
        self.database = self.loadjson()
        self.data = self.database["users"][name]

    def loadjson(self):
        with open(json_path, 'r') as f:
            return json.load(f)

    def savejson(self):
        with open(json_path, 'w') as f:
            json.dump(self.database, f, indent = 4)

    def refresh(self):
        self.database = self.loadjson()
        self.data = self.database["users"][self.name]

    def record_command(self, command):
        self.data["count"] += 1
        if command not in self.data["history"]:
            self.data["history"][command] = 1
        else:
            self.data["history"][command] += 1

        self.savejson() # if program crasshes, history is already saved

    def todo(self, arg = ""):
        if not arg:
            print("Usage: todo <detail/todo>")
            return
        try:
            self.data["todos"].append(arg)
            self.savejson()
            print("--Todo added successfully--")
        except Exception as e:
            print(f"ERROR : {e}")

    def hello(self):
        print(f"Hello {self.name}")

    def date(self, arg = ""):
        print(f"YYYY-MM-DD : {datetime.now().date()}")

    def time(self, arg = ""):
        print(f"HH-MM-SS : {str(datetime.now().time())[:8]}")

    def clear(self, arg = ""):
        os.system("cls")
        print("\n======WELCOME======\n")

    def quote(self, arg = ""):
        print(random.choice(quotes))

    #not this one rn, it changes the name inside user's data, but the username is still intact
    def rename(self, name = ""):
        if not name:
            print("Usage: rename <newName>")
            return
        self.name = name
        try:
            self.data["name"] = self.name
            self.savejson()
        except Exception as e:
            print(f"ERROR : {e}")

    def notes(self, arg = ""):
        try:
            with open(notefile) as f:
                file = f.read()
                if len(file) == 0:
                    print("--No notes available--")
                else:
                    print(file)
        except Exception as e:
                print(f"ERROR : {e}")

    def note(self, arg = ""):
        if not arg:
            print("Usage: note <detail/note>")
            return
        try:
            with open(notefile, 'a') as f:
                f.write(arg + "\n")
                print("--Note added successfully--")
        except Exception as e:
                print(f"ERROR : {e}")

    def removetodo(self, arg = ""):
        if not arg.isdigit():
            print("Usage: removetodo <integer>")
            return
        todonum = int(arg)
        if todonum <= 0:
            print("--Associated number cannot be less than 1--")
            return
        try:
            if todonum > len(self.data["todos"]):
                print(f"--No data found with number {arg}--")
                return
            del self.data["todos"][todonum - 1]
            print("--Removed successfully--")
            self.savejson()
        except Exception as e:
            print(f"ERROR : {e}")

    def todos(self, arg = ""):
        try:
            count = 1
            if not self.data["todos"]:
                print("--No todos available--")
                return
            for todo in self.data["todos"]:
                print(f"{count}. {todo}")
                count += 1
        except Exception as e:
            print(f"ERROR : {e}")

    def searchnote(self, arg = ""):
        count = 0
        if not arg.strip():
            print("Usage: searchnote <keyword>")
            return
        try:
            with open(notefile) as f:
                file = f.read().splitlines() # basically the split("\n") but inbuilt
                if not file:
                    print("--No notes available--")
                else:
                    search = arg.lower()
                    for line in file:
                        if search in line.lower():
                            print(line)
                            count += 1
                    if not count:
                        print("--No result matches you search--")
        except Exception as e:
                print(f"ERROR : {e}")


    def searchtodo(self, arg=""):
        if not arg:
            print("Usage: searchtodo <keyword>")
            return
        search = arg.lower()
        for todo in self.data["todos"]:
            if search in todo.lower():
                print(todo)

    def calc(self, arg=""):
        arg = arg.strip()
        if not arg:
            print("Usage: calc <simple_expression>")
            return
        try:
            ans = eval(arg)
            print(f"{arg} = {ans}")
        except NameError:
            print("--Invalid Expression--")
        except Exception as e:
            print(f"ERROR : {e}")

    def joke(self, arg=""):
        try:
            with urllib.request.urlopen(jokeurl) as response:
                data = json.loads(response.read().decode())
            print(f"Joke Type : {data['type']}")
            print(data["setup"])
            print(data["punchline"])
        except Exception as e:
            print(f"ERROR : {e}")

    def fact(self, arg=""):
        if arg:
            print("Usage : fact")
            return
        try:
            with urllib.request.urlopen(facturl) as response:
                data = json.loads(response.read().decode())
            print(f"Random fact:\n{data['text']}")
        except Exception as e:
            print(f"ERROR : {e}")

    def weather(self, arg=""):
        if not arg:
            print("Usage : weather <city_name>")
            return
        url = f"https://wttr.in/{arg}?format=j1"
        print(f"Fetching data from {url}")
        try:
            with urllib.request.urlopen(url, timeout = 10) as response:
                data = json.loads(response.read().decode()) 
            info = data["current_condition"][0]
            print(f"Temperature : {info['temp_C']}°C")
            print(f"Humidity    : {info['humidity']}%")
            print(f"Feels Like  : {info['FeelsLikeC']}°C")
            print(f"Description : {info['weatherDesc'][0]['value']}")
            print(f"Wind Speed  : {info['windspeedKmph']} km/h")
        except Exception as e:
            print(f"ERROR : {e}")

    def stats(self, arg=""):
        blabla = self.data["history"].copy()
        if not blabla:
            print("--history not available--")
            return
        print("Top commands : ")
        for i in range(0, 3):
            if not blabla: break
            maximum = max(blabla, key=blabla.get)
            print(f"{i+1}. {maximum} ({blabla[maximum]})")
            del blabla[maximum]

    def timer(self, arg=""):
        if not arg.isdigit():
            print("Usage: timer <seconds>")
            return
        arg = int(arg)
        if arg <= 0:
            print("--Associated number cannot be less than 1--")
            return
        remaining = arg
        for i in range(arg, 0, -1):
            hour = remaining // 3600
            minutes = (remaining % 3600) // 60
            sec = remaining % 60
            print(f"{hour:02}:{minutes:02}:{sec:02}")
            # :02 means that minimum width is 2 with padding using 0
            time.sleep(1)
            remaining -= 1
        print("Time's up!")

    def users(self, arg = ""):
        if not self.database["users"]:
            print("--No users found--")
            return
        print("Registered users:")
        for number, name in enumerate(self.database["users"], start = 1):
            print(f"{number}. {name}")

    def createuser(self, arg = ""):
        arg_ = arg.strip().lower()
        if not arg_:
            print("Usage : createuser <username>")
            return
        if arg_ not in self.database["users"]:
            self.database["users"][arg] = {
                "name" : arg_,
                "count" : 0,
                "todos" : [],
                "history" : {}
                }
            self.savejson()
            print(f"--User {arg} created successfully--")
        else:
            print("--User already exists--")
    
    def switchuser(self, arg = ""):
        if not arg:
            print("Usage : switchuser <username>")
            return
        arg_ = arg.strip().lower()
        if arg_ not in self.database["users"]:
            print("--User not found--")
            return 0
        return 1
    
    def deleteuser(self, arg=""):
        if not arg:
            print("Usage : deleteuser <username>")
            return
        arg_ = arg.strip().lower()
        if arg_ not in self.database["users"]:
            print("--User not found--")
            return
        del self.database["users"][arg_]
        print("--User deleted successfully--")