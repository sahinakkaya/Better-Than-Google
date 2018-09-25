import os
from parser import Chat
import datetime
import textwrap

main_page = """<!DOCTYPE html>
<html>
<head>
    <!-- Stylesheets -->
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <!-- Scripts -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script type="text/javascript" src="https://cdn.rawgit.com/asvd/dragscroll/master/dragscroll.js"></script>
    <meta charset="utf-8"></meta>
    <title>WhatsApp</title>
</head>
<body>
    <div class="container">

    <!-- Dropdown Menu -->
    <div class="dropdown_menu">
        <p class="dropdown_item">New group</p>
        <p class="dropdown_item">New broadcast</p>
        <p class="dropdown_item">WhatsApp Web</p>
        <p class="dropdown_item">Starred Messages</p>
        <p class="dropdown_item">Settings</p>
    </div>

    <!-- Search Bar -->
    <div class="back_trigger"></div>
    <input type="text" class="search_bar">

    <!-- Lightbox -->
    <div class="lightbox">
        <div class="lightbox_container">
            <h1 class="lightbox_name">Marc</h1>

            <div class="lightbox_image">
                <img src="images/chats/chat2.jpg">
            </div>

            <div class="lightbox_controls">
                <div class="one_control"><img src="images/icons/chat.png"></div>
                <div class="one_control"><img src="images/icons/phone.png"></div>
                <div class="one_control"><img src="images/icons/video.png"></div>
                <div class="one_control"><img src="images/icons/info.png"></div>
            </div>
        </div>
    </div>

        <div class="title_bar">
            <div class="title_top">
                <div class="title_container">
                    <p>WhatsApp</p>
                </div>

                <div class="icon_container">
                    <div><img src="images/menu.png"></div>
                    <div><img src="images/search.png"></div>
                </div>
            </div>

            <div class="tab_menu">
                <p class="single_tab active">CHATS</p>
                <p class="single_tab">STATUS</p>
                <p class="single_tab">CALLS</p>
            </div>
        </div>

        <div class="messages_section dragscroll">
            {}
        </div>

        <div class="android_controls">
            <div class="controls_inner">
                <div><img src="images/android/back.png"></div>
                <div><img src="images/android/menu.png"></div>
                <div><img src="images/android/tab.png"></div>
            </div>
        </div>
    </div>

    <script src="js/script.js"></script>
</body>
</html>
"""


def format_time(time):
    today = datetime.date.today()
    _time = datetime.date(time.year, time.month, time.day)
    difference = today - _time
    if difference.days == 0:
        return datetime.datetime.strftime(time, "%-I:%M %p")
    elif difference.days == 1:
        return "YESTERDAY"
    else:
        return datetime.datetime.strftime(time, "%-m/%-d/%y")


def format_message(chat):
    r = ""
    for i in reversed(chat.text):
        if i.operation == "SendMessage":
            if chat.type == "Group Chat":
                person = chat.persons[list(i.main_persons)[0]]
                if person.saved_contact_name:
                    if chat.right_side_person != person.saved_contact_name:
                        r += person.saved_contact_name.split()[0] + ": "
                else:
                    r += person.unique_id + ": "

            r += i.text.split(": ", 1)[1]
            break
    return textwrap.shorten(r, 45, placeholder="...")
def main():
    all_chats = []
    images = os.listdir("whatsapp_ui/images/chats")

    for file in os.listdir("chats"):
        chat = Chat(f"chats/{file}")
        chat_type = "single_chat" if chat.type == "2 Person Chat" else "single_chat"
        chat_image = f"{file}.jpg" if file + ".jpg" in images else "default.png"
        title = chat.title_history[-1]
        formatted_time = format_time(chat.end_date)
        last_message = format_message(chat)
        all_chats.append((chat_type, chat_image, title, formatted_time, last_message, chat.end_date))

    all_chats.sort(key=lambda x: x[5], reverse=True)

    chat_temp = """<div class="{}"> 
                        <div class="image_container">
                            <img src="images/chats/{}">
                        </div>
                        <div class="content_container">
                            <div class="content_container_inner">
                                <p class="user_name"><name> {}</name> <span>{}</span></p>
                                <p class="chat_content">{}</p>
                            </div>
                        </div>
                    </div>"""
    formatted_chats = []
    print(all_chats)
    for chat in all_chats:
        formatted_chats.append(chat_temp.format(*chat))

    f = open("whatsapp_ui/index.html", "w")
    print(main_page.format("\n".join(formatted_chats)), file=f)
    f.close()



if __name__ == '__main__':
    main()

