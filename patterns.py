import regex as re

valid_hex_color = lambda x: re.match(r"(^#[0-9A-F]{6}$)|(^#[0-9A-F]{3}$)", x, re.IGNORECASE)
is_phone_number = lambda x: re.match(r"^\+[\d\s]{11,19}$", x) # re.match(r"^\+[\d\s()-]{14,17}$"

split_pattern = re.compile(r"^(?:\d{1,2})/(?:\d{1,2})/(?:\d{1,2}), (?:\d{1,2}):(?:\d{1,2})(?: PM| AM)? - ")
p_added = re.compile(
    r"(?P<MAIN>.*)(?: added )(?<!.* (?:created group \"|removed |changed the subject from \").*)(?<!.*:.*)(?P<OTHER>.*)")
p_changed = re.compile(
    r"(?P<MAIN>.*)(?: changed to )(?<!.* (?:created group \"|removed |changed the subject from \"|added ).*)(?<!.*:.*)(?P<OTHER>.*)")
p_removed = re.compile(
    r"(?P<MAIN>.*)(?: removed )(?<!.* (?:created group \"|added |changed the subject from \").*)(?<!.*:.*)(?P<OTHER>.*)")
p_created = re.compile(
    r"(?P<MAIN>.*)(?: created group \")(?<!.* (?:added |removed |changed the subject from \").*)(?<!.*:.*)(?P<OTHER>.*)\"$")
p_left = re.compile(r"(?P<MAIN>.*)(?: left$)(?<!.* (?:created group \"|removed |added ).*)(?<!.*: .*)")
p_security = re.compile(
    r"(?P<MAIN>.*)(?:'s security code changed. Tap for more info.$)(?<!.* (?:created group \"|removed |added ).*)(?<!.*: .*)")
p_already_added = re.compile(
    r"(?P<MAIN>.*)(?<!.* (?:added ).*)(?: was added$)(?<!.* (?:created group \"|removed ).*)(?<!.*: .*)")
p_joined = re.compile(r"(?P<MAIN>.*)(?: joined using this group's invite link$)(?<!.*: .*)")
p_change_su = re.compile(r"(?P<MAIN>.*)(?: changed the subject from \")(?<!.*: .*)(?P<OTHER>.*)\" to \"(?P<OTHER2>.*)\"$")
p_change_se = re.compile(
    r"(?P<MAIN>.*)(?: changed this group's settings to allow only admins to edit this group's info$)(?<!.*: .*)")
p_change_i = re.compile(r"(?P<MAIN>.*)(?: changed this group's icon$)(?<!.*: .*)")
p_change_d = re.compile(r"(?P<MAIN>.*)(?: changed the group description$)(?<!.*: .*)")
p_message = re.compile(r"(?P<MAIN>.*): (.*)")
operations = {p_added: 'AddPerson', p_removed: 'RemovePerson', p_created: 'CreateGroup',
              p_left: 'LeftGroup', p_joined: 'JoinedGroup', p_change_se: "ChangeGroupSettings",
              p_change_i: 'ChangeGroupIcon', p_already_added: 'AlreadyAdded', p_message: "SendMessage",
              p_change_su: 'ChangeSubject', p_change_d: 'ChangeDescription',
              p_changed: 'ChangeNumber', p_security: 'SecurityCodeChanged'}