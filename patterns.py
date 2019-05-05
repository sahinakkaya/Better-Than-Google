"""Helper module for defining regex related constants and functions"""
import regex as re


def valid_hex_color(string):
    """Return true if given string is valid hex color, false otherwise"""
    return re.match(r"(^#[0-9A-F]{6}$)|(^#[0-9A-F]{3}$)", string, re.IGNORECASE)


def is_phone_number(string):
    """Return true if given string is possibly a phone number, false otherwise"""
    return re.match(r"^\+[\d\s]{11,19}$", string)  # re.match(r"^\+[\d\s()-]{14,17}$"


SPLIT_PATTERN = re.compile(r"^(?:\d{1,2})/(?:\d{1,2})/(?:\d{1,2}), (?:\d{1,2}):(?:\d{1,2})(?: PM| AM)? - ")
P_ADDED = re.compile(
    r"(?P<MAIN>.*)(?: added )(?<!.* (?:created group \"|removed |changed the subject from \").*)(?<!.*:.*)(?P<OTHER>.*)")
P_CHANGED = re.compile(
    r"(?P<MAIN>.*)(?: changed to )(?<!.* (?:created group \"|removed |changed the subject from \"|added ).*)(?<!.*:.*)(?P<OTHER>.*)")
P_REMOVED = re.compile(
    r"(?P<MAIN>.*)(?: removed )(?<!.* (?:created group \"|added |changed the subject from \").*)(?<!.*:.*)(?P<OTHER>.*)")
P_CREATED = re.compile(
    r"(?P<MAIN>.*)(?: created group \")(?<!.* (?:added |removed |changed the subject from \").*)(?<!.*:.*)(.*)\"$")
P_LEFT = re.compile(r"(?P<MAIN>.*)(?: left$)(?<!.* (?:created group \"|removed |added ).*)(?<!.*: .*)")
P_SECURITY = re.compile(
    r"(?P<MAIN>.*)(?:'s security code changed. Tap for more info.$)(?<!.* (?:created group \"|removed |added ).*)(?<!.*: .*)")
P_ALREADY_ADDED = re.compile(
    r"(?P<MAIN>.*)(?<!.* (?:added ).*)(?: was added$)(?<!.* (?:created group \"|removed ).*)(?<!.*: .*)")
P_JOINED = re.compile(r"(?P<MAIN>.*)(?: joined using this group's invite link$)(?<!.*: .*)")
P_CHANGE_SU = re.compile(r"(?P<MAIN>.*)(?: changed the subject from \")(?<!.*: .*)(.*)\" to \"(.*)\"$")
P_CHANGE_SE = re.compile(
    r"(?P<MAIN>.*)(?: changed this group's settings to allow only admins to edit this group's info$)(?<!.*: .*)")
P_CHANGE_I = re.compile(r"(?P<MAIN>.*)(?: changed this group's icon$)(?<!.*: .*)")
P_CHANGE_D = re.compile(r"(?P<MAIN>.*)(?: changed the group description$)(?<!.*: .*)")
P_MESSAGE = re.compile(r"(?P<MAIN>.*?): (.*)")
OPERATIONS = {P_ADDED: 'AddPerson', P_REMOVED: 'RemovePerson', P_CREATED: 'CreateGroup',
              P_LEFT: 'LeftGroup', P_JOINED: 'JoinedGroup', P_CHANGE_SE: "ChangeGroupSettings",
              P_CHANGE_I: 'ChangeGroupIcon', P_ALREADY_ADDED: 'AlreadyAdded', P_MESSAGE: "SendMessage",
              P_CHANGE_SU: 'ChangeSubject', P_CHANGE_D: 'ChangeDescription',
              P_CHANGED: 'ChangeNumber', P_SECURITY: 'SecurityCodeChanged'}
