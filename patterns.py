import regex as re

is_valid_hex = lambda x: re.match(r"(^#[0-9A-F]{6}$)|(^#[0-9A-F]{3}$)",x,re.IGNORECASE)
is_number = lambda x: re.match(r"^\+[\d\s]{11,19}$", x) # re.match(r"^\+[\d\s()-]{14,17}$"
split_pattern = re.compile(r"^(?:\d{1,2})/(?:\d{1,2})/(?:\d{1,2}), (?:\d{1,2}):(?:\d{1,2})(?: PM| AM)? - ")
p_added = re.compile(
    r"(.*)(?: added )(?<!.* (?:created group \"|removed |changed the subject from \").*)(?<!.*:.*)(.*)")
p_changed = re.compile(
    r"(.*)(?: changed to )(?<!.* (?:created group \"|removed |changed the subject from \"|added ).*)(?<!.*:.*)(.*)")
p_removed = re.compile(
    r"(.*)(?: removed )(?<!.* (?:created group \"|added |changed the subject from \").*)(?<!.*:.*)(.*)")
p_created = re.compile(
    r"(.*)(?: created group \")(?<!.* (?:added |removed |changed the subject from \").*)(?<!.*:.*)(.*\")")
p_left = re.compile(r"(.*)(?: left$)(?<!.* (?:created group \"|removed |added ).*)(?<!.*: .*)")
p_security = re.compile(
    r"(.*)(?:'s security code changed. Tap for more info.$)(?<!.* (?:created group \"|removed |added ).*)(?<!.*: .*)")
p_already_added = re.compile(
    r"(.*)(?<!.* (?:added ).*)(?: was added$)(?<!.* (?:created group \"|removed ).*)(?<!.*: .*)")
p_joined = re.compile(r"(.*)(?: joined using this group's invite link$)(?<!.*: .*)")
p_change_su = re.compile(r"(.*)(?: changed the subject from \")(?<!.*: .*)(.*)\" to \"(.*)\"$")
p_change_se = re.compile(
    r"(.*)(?: changed this group's settings to allow only admins to edit this group's info$)(?<!.*: .*)")
p_change_i = re.compile(r"(.*)(?: changed this group's icon$)(?<!.*: .*)")
p_change_d = re.compile(r"(.*)(?: changed the group description$)(?<!.*: .*)")
p_message = re.compile(r"(.*): (.*)")
regexes = {p_added: 'AddPerson', p_removed: 'RemovePerson', p_created: 'CreateGroup',
           p_left: 'LeftGroup', p_joined: 'JoinedGroup', p_change_se: "ChangeGroupSettings",
           p_change_i: 'ChangeGroupIcon', p_already_added: 'AlreadyAdded', p_message: "SendMessage",
           p_change_su: 'ChangeSubject', p_change_d: 'ChangeDescription',
           p_changed: 'ChangeNumber', p_security: 'SecurityCodeChanged'}