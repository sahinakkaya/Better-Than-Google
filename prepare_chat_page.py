import datetime
import textwrap
from parser import Chat
from chat_page_templates import html_template, info_template, color_template, chat_header, name_tag, message_bubble


class ChatPage:
    def __init__(self, file):
        self.filename = file
        self.chat = Chat(self.filename)
        self.today = datetime.date.today()
        self.current_date = datetime.date.fromtimestamp(self.chat.start_date.timestamp()) - datetime.timedelta(days=1)
        self.participant_colors = self.title = self.header = self.content = ""
        self.make_ready_everything()
        self.write_to_file()

    def make_ready_everything(self):
        self.participant_colors = self.get_colors()
        self.title = self.chat.title
        self.header = self.create_header()
        self.content = self.create_content()

    def get_colors(self):
        r = ""
        for person in self.chat.persons.values():
            r += color_template % (person.id_without_spaces, person.color)
        return r

    def create_header(self):
        type_ = "dual" if self.chat.type == "2 Person Chat" else "group"
        title = textwrap.shorten(self.chat.title, width=24, placeholder="...")
        participants = ""
        if type_ == "group":
            persons = self.get_sorted_person_list()
            participants = textwrap.shorten(", ".join(persons), 38, placeholder="...")

        return chat_header.format(type_=type_, title=title, participants=participants)

    def create_content(self):
        chat = self.chat
        current_date = datetime.date.fromtimestamp(chat.start_date.timestamp()) - datetime.timedelta(days=1)
        content = ""
        previous_person = None
        for line in chat.text[:150]:
            date, text, operation = line.time, line.text_without_time, line.operation
            difference = datetime.date.fromtimestamp(date.timestamp()).day - current_date.day
            if difference > 0:
                current_date = date
                content += self.format_date(date)
            if operation == "SendMessage":
                message, previous_person = self.send_message(line, previous_person)
                content += message
            elif operation == -1:
                content += info_template.format("wp_info", text)
            else:
                content += info_template.format("operation", text)
        return content

    def get_sorted_person_list(self):
        all_persons = list(self.chat.persons.values())
        try:
            all_persons.remove(self.chat.persons[self.chat.right_side_person])
        except ValueError:
            pass
        person_list = []
        for person in all_persons:
            if person.saved_contact_name:
                person_list.append(person.saved_contact_name.split()[0])
            else:
                person_list.append(person.unique_id)
        sorted_p_list = list(sorted(person_list, key=lambda x: ((x[0] == "+"), x)))
        return sorted_p_list

    def format_date(self, date):
        r = ""
        diff = (self.today - datetime.date.fromtimestamp(date.timestamp())).days
        if diff == 0:
            r += info_template.format("date", "today")
        elif diff == 1:
            r += info_template.format("date", "yesterday")
        else:
            r += info_template.format("date", date.strftime("%B %d, %Y"))

        return r

    def send_message(self, line, previous_person):
        chat = self.chat
        person = chat.persons[list(line.main_persons)[0]]
        content = line.text.split(": ", 1)[1][:-1]
        time = line.time.strftime("%-H:%M")
        side = "left"
        name = name_tag.format(non_space_id=person.id_without_spaces, id=person.unique_id, desc="")
        if previous_person == person.unique_id or chat.type == "2 Person Chat":
            name = ""
        else:
            previous_person = person.unique_id
        type_ = "normal"
        if self.chat.right_side_person == person.unique_id:
            side = "right"
            name = ""
        if content in ("This message was deleted", "You deleted this message", "<Media omitted>"):
            type_ = "special"
            content = content.replace("<", " &lt;").replace(">", "&gt;")
            content = '<img src="images/special_message.png" width="10" height="10"> ' + content
        return message_bubble.format(side=side, name=name, content=content, time=time, type_=type_), previous_person

    def get_page(self):
        return html_template.format(participant_colors=self.participant_colors, title=self.title, header=self.header,
                                    content=self.content)

    def write_to_file(self, file_name=None):
        if file_name:
            with open(file_name + ".html", "w") as f:
                f.write(self.get_page())
        else:
            with open("whatsapp_ui/" + self.filename + ".html", "w") as f:
                f.write(self.get_page())
