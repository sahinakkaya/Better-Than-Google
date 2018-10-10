html_template = """<!DOCTYPE html>
<html>
<head>
  <!-- Stylesheets -->
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <!-- Scripts -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script type="text/javascript" src="https://cdn.rawgit.com/asvd/dragscroll/master/dragscroll.js"></script>
  <meta charset="utf-8"></meta>
  <style>
    {participant_colors}
  </style>
  <title>{title}</title>
</head>
<body>
  <div class="container">
    {chat_header}
    <div class="messages_section">
      <div class="speech-wrapper">
        {chat_content}
      </div>
      <div class="android_controls">
        <div class="controls_inner">
          <div><img src="images/android/back.png"></div>
          <div><img src="images/android/menu.png"></div>
          <div><img src="images/android/tab.png"></div>
        </div>
      </div>
    </div>
  </div>
  <script src="js/script.js"></script>
</body>
</html>
"""
chat_header = """<div class="chat_header {}">
      <img class="back_to_chats" src="images/icons/back.png"></img>
      <img class="chat_icon" src="images/chats/default.png"></img>
      <div class="chat_title"> <!-- 24 chars at max -->
        <p>{title}</p>
        {group_participants}
        <!--<p class="persons">Person-1, Person-2, Person-3, Perso...</p>-->
      </div>
      <img class="right_icons" src="images/menu.png"></img>
    </div>"""
color_template = '.%s{\n    color:%s;\n}\n'
name_tag = '<p class="name {}" >{}</p>'
name_alt_tag = '<p class="name {}">{}<span> ~{}</span></p>'
message_bubble = """<div class="bubble {alt}">
          <div class="txt">
            {}
            <p class="message">{message_content}</p>
          </div>
          <span class="timestamp">{time}</span>
          <div class="bubble-arrow {alt}"></div>
        </div>
        """
