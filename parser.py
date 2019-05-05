from random import choice
import datetime
from patterns import OPERATIONS, SPLIT_PATTERN, is_phone_number, valid_hex_color


class Line:
    info_messages = [
        "Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info.\n",
        "Messages to this group are now secured with end-to-end encryption. Tap for more info.\n",
        "ERROR: can't send to this group, not a participant\n"]

    def __init__(self, line):
        self.text = self.remove_unicode_spaces(line)
        self.time = self.get_time(self.text)
        if self.time is not None:
            self.text_without_time = SPLIT_PATTERN.split(self.text)[1]
            self.operation = self.find_operation()
            self.main_persons = self.extract_persons()
            self.affected_persons = self.extract_persons("OTHER")

    @staticmethod
    def get_time(line):
        date = line.split(" -")[0]  # 8/26/17, 5:13 PM or 8/26/17, 17:13
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
        return Line(self.text + other.text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'{self.text}\n' \
            f'{datetime.datetime.strftime(self.time, "%d/%m/%Y, %-H:%M")}\n' \
            f'{self.operation}\n' \
            f'Main Persons: {self.main_persons}\n' \
            f'Affected Persons: {self.affected_persons}'

    @staticmethod
    def remove_unicode_spaces(line):
        new_line = ""
        for char in line:
            if char == '\xa0':
                new_line += " "
            elif char.isprintable() or char in "\t\n\r\f\v\u200d\u200e\u200c":
                new_line += char
        return new_line

    def extract_persons(self, p_type="MAIN"):
        if self.operation == -1:
            return set()
        regex = self.reverse_search_dict(OPERATIONS, self.operation)
        text = self.text_without_time
        person_list = self.slice_to_person(text, regex, p_type)
        return set(person_list)

    def isvalid(self):
        return self.time is not None

    def find_operation(self):
        text = self.text_without_time
        if text in self.info_messages:
            return -1
        for pattern in OPERATIONS.keys():
            if pattern.match(text):
                return OPERATIONS[pattern]
        else:
            raise Exception("Unknown operation\n", self.text)

    @staticmethod
    def reverse_search_dict(dictionary, search_string):
        for key, value in dictionary.items():
            if value == search_string:
                return key

    @staticmethod
    def slice_to_person(string, regex, p_type):
        if p_type in regex.groupindex:
            sliced_text = regex.match(string).group(p_type)
            sliced_text = sliced_text.rsplit(" and ", 1)
            sliced_text = sliced_text[0].split(", ") + [sliced_text[-1]]
            sliced_text = filter(None, sliced_text)
            return sliced_text
        else:
            return set()


class Person:
    colors = ['#1C5765', '#1B74F1', '#4C1BF1', '#B21BF1', '#F11B77', '#F11B1B', '#C4BC20',
              '#2BB518', '#1BF1B5', '#870202', '#778702', '#008A10', '#008A87', '#004E8A',
              '#46008A', '#8A004A', '#FF7A7A', '#E05C12', '#7BD2A1', '#30A41D', '#5DB693',
              '#7ADAFF', '#7A98FF', '#C77AFF', '#FF7AE1']
    __statistic_fields = ['AddPerson', 'RemovePerson', 'CreateGroup', 'LeftGroup', 'JoinedGroup', "ChangeGroupSettings",
                          'ChangeGroupIcon', 'AlreadyAdded', 'ChangeSubject', 'ChangeDescription', 'ChangeNumber',
                          'SendMessage', 'KickedOut', 'AddedBySomeone', 'SecurityCodeChanged', 'NumberOfWords',
                          'NumberOfLetters', 'ChangeNumber2This']

    def __init__(self, name):
        self.unique_id = name
        self.id_without_spaces = "_".join(self.unique_id.split()).replace("+", "_")
        self.descriptive_name = None
        self.saved_contact_name = None if is_phone_number(self.unique_id) else self.unique_id
        self.statistics = {i: 0 for i in Person.__statistic_fields}
        self.color = choice(self.colors)
        self.existence = [[None, None]]

    def update_desc_name(self, name):
        self.descriptive_name = name

    def update_contact_name(self, name):
        self.saved_contact_name = name

    def update_stats(self, operation, line):
        # print(line)
        # print(self.statistics)
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
        if valid_hex_color(color):
            self.color = color
        else:
            print(f"{color} is not valid hex color.")

    def __repr__(self):
        return f"ID: {self.unique_id}\n" \
            f"Descriptive Name: {self.descriptive_name}\n" \
            f"Saved Name: {self.saved_contact_name}\n" \
            f"Color: {self.color}\n" \
            f"Existence: {self.existence}\n"


class Chat:
    def __init__(self, filename):
        self.title_history = []
        self.text = self.read_file(filename)
        self.persons = {}
        self.add_persons()
        self.start_date = self.text[0].time
        self.end_date = self.text[-1].time
        self.right_side_person = self.ask_right_side()
        self.type = self.detect_chat_type(filename)
        self.adjust_right_side()

    def detect_chat_type(self, filename):
        with open(filename, encoding="utf8") as f:
            first_line = f.readline()
            if Line.info_messages[0] in first_line and len(self.persons) <= 2:
                return "2 Person Chat"
            elif Line.info_messages[1] in first_line or len(self.persons) > 2:
                return "Group Chat"
            else:
                raise Exception("Unsupported file.")

    @staticmethod
    def read_file(filename):
        text = []
        with open(filename, encoding="utf8") as f:
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
                    if person_name == "You":
                        person_name = "you"
                    if person_name not in self.persons:
                        person = Person(person_name)
                        self.persons[person_name] = person
                    self.persons[person_name].update_stats(operation, line)

                if operation in ("AddPerson", "RemovePerson", "ChangeNumber"):
                    for person_name in affected_persons:
                        if person_name == "You":
                            person_name = "you"
                        if person_name not in self.persons:
                            person = Person(person_name)
                            self.persons[person_name] = person
                        passive_operation = {"AddPerson": "AddedBySomeone", "RemovePerson": "KickedOut",
                                             "ChangeNumber": "ChangeNumber2This"}[operation]
                        self.persons[person_name].update_stats(passive_operation, line)

                elif operation in ("CreateGroup", "ChangeSubject"):
                    self.title_history.append(line.text.rsplit('"', 2)[-2])

    def ask_right_side(self):
        possible_persons = [person.saved_contact_name for person in self.persons.values() if not (
                is_phone_number(person.unique_id) or
                person.saved_contact_name in ('You', 'you')) and
                            person.existence == [[None, None]]]
        if len(possible_persons) == 0:  # This should be updated.
            possible_persons = self.persons.keys()
        print(*possible_persons, sep="\n")
        r = input("Who are you? ")
        while r not in possible_persons:
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
            raise Exception("Take a look at this")

    def adjust_right_side(self):
        if self.type == "Group Chat":
            self.persons[self.right_side_person].existence = []
            self.combine_stats(self.right_side_person, "you")
        else:
            for p in self.persons:
                if p != self.right_side_person:
                    self.title_history.append(p)
                    break

    @property
    def title(self):
        return self.title_history[-1]

    def __repr__(self):
        return f"Title: {self.title_history[-1]}\n" \
            f"Start Date: {self.start_date}\n" \
            f"End Date: {self.end_date}\n" \
            f"Type: {self.type}\n" \
            f"R-side person: {self.right_side_person}"

    def search(self, p):
        for line in self.text:
            if p in line.main_persons and line.operation == "SendMessage":
                print(line.text, end="")


if __name__ == '__main__':
    import os

    for file in os.listdir("chats/"):
        if not os.path.isdir(f"chats/{file}"):
            c = Chat(f"chats/{file}")
