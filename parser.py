from random import choice
import re
import datetime


class NewException(Exception):
    def __init__(self, message):
        super(NewException, self).__init__(message)
        self.message = message


class Line:
    info_messages = [
        "Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info.",
        "Messages to this group are now secured with end-to-end encryption. Tap for more info.",
        "ERROR: can't send to this group, not a participant"]

    def __init__(self, line):
        self.text = self.remove_unicode_spaces(line)
        self.time = self.get_time(self.text)
        if self.time is not None:
            self.operation = self.find_operation()
            self.main_persons = self.slice_to_person(self.text)
            self.affected_persons = self.slice_to_person(self.text, "right", " added ", " removed ", " changed to ")
        else:
            pass

    @staticmethod
    def get_time(line):
        date = line.split(" -")[0]  # 8/26/17, 5:13 PM
        try:
            try:
                return datetime.datetime.strptime(date, "%m/%d/%y, %I:%M %p")
            except ValueError:
                return datetime.datetime.strptime(date, "%m/%d/%y, %H:%M")
        except ValueError:
            return None
        except Exception as e:
            raise Exception(e)

    def __add__(self, other):
        return Line(self.text + "\n" + other.text)

    def __str__(self):
        return self.text

    def __repr__(self):
        template = "{}\n{}\n{}\n" \
                   "Main Persons: {}\nAffected Persons: {}".format(
            self.text, datetime.datetime.strftime(self.time, "%d/%m/%Y, %-H:%M"), self.operation,
            self.main_persons, self.affected_persons)
        return template

    @staticmethod
    def remove_unicode_spaces(line):
        new_line = ""
        for char in line:
            if char == '\xa0':
                new_line += " "
            elif char.isprintable():
                new_line += char
        return new_line

    def slice_to_person(self, line, side="left", *keys):
        if line.split("- ")[1] in self.info_messages:
            return []
        if side == "left":
            sliced_text = line.split(":")[1].split("- ")[1]
            for i in Chat._all_operations.keys():
                sliced_text = sliced_text.split(i)[0]
            person_list = sliced_text.split(" and ")
            person_list = person_list[0].split(",") + [person_list[-1]]
            person_list = [i.strip() for i in person_list if i != ""]
            return set(person_list)
        elif side == "right":
            control = 0
            r = []
            for key in keys:
                try:
                    line.index(key)
                    persons = line.split(key)[-1].split(",")[:-1] + line.split(key)[-1].split(",")[-1].split(" and ")
                    if any(persons):
                        persons = [p.strip() for p in persons]
                        r += persons
                except ValueError:
                    control += 1
            if control == len(keys):
                return []
            else:
                return r

    def isvalid(self):
        return self.time is not None

    def find_operation(self):
        if self.text.split("- ")[1] in self.info_messages:
            return -1
        if len(self.text.split(":", 2)) == 3:
            return "SendMessage"  # Does matter! :)
        for i in Chat._all_operations.keys():
            if i == '!_*_!SendMessage!_*_!':
                continue
            # elif i == '!_*_!removed!_*_!':
            #     line.split(":", 2)[1].split(i)
            #     line.split("removed ")[-1].split(" and ")
            if len(self.text.split(":", 2)[1].split(i)) == 2:
                return Chat._all_operations[i]
        else:
            raise Exception("Unknown operation\n", self.text)


class Person:
    colors = ['#1C5765', '#1B74F1', '#4C1BF1', '#B21BF1', '#F11B77', '#F11B1B', '#C4BC20',
              '#2BB518', '#1BF1B5', '#870202', '#778702', '#008A10', '#008A87', '#004E8A',
              '#46008A', '#8A004A', '#FF7A7A', '#E05C12', '#7BD2A1', '#30A41D', '#5DB693',
              '#7ADAFF', '#7A98FF', '#C77AFF', '#FF7AE1']

    def __init__(self, name):
        self.unique_id = name
        self.descriptive_name = None
        if not re.match(r"^\+[\d\s()-]{14,17}$", self.unique_id):
            print(self.unique_id)
        self.saved_contact_name = None if re.match(r"^\+[\d\s]{11,19}$", self.unique_id) else self.unique_id
        self.statistics = {i: 0 for i in Chat._all_operations.values()}
        self.color = choice(self.colors)
        self.existence = [[None, None]]

    def update_desc_name(self, name):
        self.descriptive_name = name

    def update_contact_name(self, name):
        self.saved_contact_name = name

    def update_stats(self, operation, line):
        # print(self.name,self.statistics,operation,line,sep="\n")
        self.statistics[operation] += 1
        if operation == "SendMessage":
            message = line.text.rsplit(": ", 1)[1]
            self.statistics["NumberOfWords"] += len(message.split())
            self.statistics["NumberOfLetters"] += len(message)
        elif operation in ("KickedOut", "LeftGroup"):
            self.existence[-1][1] = line.time
        elif operation in ("AddedBySomeone", "JoinedGroup"):
            if self.existence[-1][1] is not None:
                self.existence.append([line.time, None])
            else:
                self.existence[-1][0] = line.time

    def update_color(self, color):
        if re.match(r"(^#[0-9A-F]{6}$)|(^#[0-9A-F]{3}$)", color, re.IGNORECASE):
            self.color = color
        else:
            print("{} is not valid hex color.".format(color))

    def __repr__(self):
        return "ID: {}\nDescriptive Name: {}\nSaved Name: {}\nColor: {}\nExistence: {}\n".format(self.unique_id,
                                                                                self.descriptive_name,
                                                                                self.saved_contact_name,
                                                                                self.color,
                                                                                self.existence)


class Chat:
    _all_operations = {' added ': 'AddPerson', ' removed ': 'RemovePerson', ' created': 'CreateGroup',
                       ' left': 'LeftGroup', ' joined': 'JoinedGroup',
                       "changed this group's settings": "ChangeGroupSettings",
                       " changed this group's icon": 'ChangeGroupIcon', ' was added': 'AlreadyAdded',
                       ' changed the subject': 'ChangeSubject', ' changed the group': 'ChangeDescription',
                       ' changed to ': 'ChangeNumber', '!_*_!SendMessage!_*_!': 'SendMessage',
                       '!_*_!removed!_*_!': 'KickedOut', '!_*_!added!_*_!': 'AddedBySomeone',
                       "'s security code": 'SecurityCodeChanged',
                       '!_*_!NumberOfWords!_*_!': 'NumberOfWords',
                       '!_*_!NumberOfLetters!_*_!': 'NumberOfLetters',
                       '!_*_!changed!_*_!to!_*_!': 'ChangeNumber2This'}

    def __init__(self, file):
        self.title_history = []
        self.text = self.read_file(file)
        self.persons = {}
        self.add_persons()
        self.start_date = self.text[0].time
        self.end_date = self.text[-1].time
        self.type = self.detect_chat_type(file)
        self.right_side_person = self.ask_right_side()
        self.adjust_right_side()

    def detect_chat_type(self, file):
        with open(file, encoding="utf8") as f:
            first_line = f.readline()
            if Line.info_messages[0] in first_line and len(self.persons) <= 2:
                return "2 Person Chat"
            elif Line.info_messages[1] in first_line or len(self.persons) > 2:
                return "Group Chat"
            else:
                raise Exception("Unsupported file.")

    @staticmethod
    def read_file(file):
        text = []
        with open(file, encoding="utf8") as f:
            for line in f.readlines():
                line = Line(line)
                if line.isvalid():
                    text.append(line)
                else:
                    text[-1] += line
        return text

    def add_persons(self):
        for line in self.text:
            operation = line.operation
            main_persons = line.main_persons
            affected_persons = line.affected_persons
            if operation != -1:
                for person_name in main_persons:
                    if person_name not in self.persons:
                        person = Person(person_name)
                        self.persons[person_name] = person
                    self.persons[person_name].update_stats(operation, line)

                if operation in ("AddPerson", "RemovePerson", "ChangeNumber"):
                    operation = self.reverse_search_dict(self._all_operations, operation)
                    for person_name in affected_persons:
                        if person_name not in self.persons:
                            person = Person(person_name)
                            self.persons[person_name] = person
                        passive_operation = self._all_operations[operation.replace(" ", "!_*_!")]
                        self.persons[person_name].update_stats(passive_operation, line)

                elif operation in ("CreateGroup", "ChangeSubject"):
                    self.title_history.append(line.text.rsplit('"', 2)[-2])

    @staticmethod
    def reverse_search_dict(dictionary, search_string):
        for key, value in dictionary.items():
            if value == search_string:
                return key

    def ask_right_side(self):
        r = input("Who are you? ")
        while not (r in self.persons and self.persons[r].existence == [[None, None]]):
            print("There is no such person in the person list or the person you entered is not you.")
            r = input("Try again: ")

        return r

    def combine_stats(self, actual_person, other):
        try:
            for key in self.persons[other].statistics.keys():
                self.persons[actual_person].statistics[key] += self.persons[other].statistics[key]
            self.persons[actual_person].existence += self.persons[other].existence.copy()
            self.persons[actual_person].existence.sort()
            del self.persons[other]
        except KeyError as e:
            print(e)

    def adjust_right_side(self):
        if self.type == "Group Chat":
            self.persons[self.right_side_person].existence = []
            for p in ['you', 'You']:
                self.combine_stats(self.right_side_person, p)
            one_second = datetime.timedelta(seconds=1)
            # for person in self.persons:
            #     if self.persons[person].existence[0][0] is None:
            #         self.persons[person].existence[0][0] = self.persons[self.right_side_person].existence[0][0] - one_second
            #     if self.persons[person].existence[-1][1] is None:
            #         self.persons[person].existence[-1][1] = self.end_date + one_second

    def __repr__(self):
        # self.title_history = []
        # self.text = self.read_file(file)
        # self.persons = {}
        # self.add_persons()
        # self.start_date = self.text[0].time
        # self.end_date = self.text[-1].time
        # self.type = self.detect_chat_type(file)
        # self.right_side_person = self.ask_right_side()
        return "Title: {}\nStart Date: {}\nEnd Date: {}\nType: {}\nR-side person: {}".format(
            self.title_history[-1],self.start_date,self.end_date,self.type,self.right_side_person)

