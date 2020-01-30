import parser
from copy import deepcopy

TRANSACTION = {}

TRACKS = {
    "S": 0,
    "H": 0,
    "N": 0
}

THREATS = []
PROJECTS = []

RESOURCES = {
    "C": 0,
    "U": 0,
    "R": 0
}

STASHED_ACTIONS = {

}


def accelerate_threat():
    if len(THREATS) > 0:
        t = THREATS.pop()
        for l in t[3]:
            getattr(parser, l)(t[0])

def add_threat(threat):
    if len(THREATS) >= 3:
        t = THREATS.pop()
        for l in t[3]:
            getattr(parser, l)(t[0])

    THREATS.append(threat)
    return True


def remove_threat(n=None):
    if (len(THREATS) > 0):
        if n is None:
            THREATS.pop()
        else:
            del THREATS[n]
    return True


def add_project(project):
    if len(PROJECTS) >= 3:
        PROJECTS.pop()
    PROJECTS.append(project)
    return True


def remove_project(n=None):
    if (len(PROJECTS) > 0):
        if n is None:
            PROJECTS.pop()
        else:
            del PROJECTS[n]
    return True


def gain(resource, amount):
    RESOURCES[resource] += amount
    would_be_negative = RESOURCES[resource] < 0
    if would_be_negative:
        RESOURCES[resource] = 0
        return False
    return True


def can_afford(resource, amount=1):
    return RESOURCES[resource] >= amount


def bump_track(track, amount):
    TRACKS[track] += amount
    return True


def as_str():
    return "C:{} U:{} R:{}  S:{} H:{} U:{}".format(
        RESOURCES['C'], RESOURCES['U'], RESOURCES['R'],
        TRACKS['S'], TRACKS['H'], TRACKS['N']
    )

def p_t_as_str():
    return "P:[{}] T:[{}]".format(
        ", ".join([str(p[0]) for p in PROJECTS]),
        ", ".join([str(p[0]) for p in THREATS])
    )

def begin():
    global TRANSACTION
    TRANSACTION = {
        "RESOURCES": deepcopy(RESOURCES),
        "TRACKS": deepcopy(TRACKS),
        "THREATS": deepcopy(THREATS),
        "PROJECTS": deepcopy(PROJECTS)
    }

def commit():
    global TRANSACTION
    TRANSACTION = {}

def rollback():
    global TRANSACTION, RESOURCES, TRACKS, THREATS, PROJECTS
    RESOURCES = deepcopy(TRANSACTION["RESOURCES"])
    TRACKS = deepcopy(TRANSACTION["TRACKS"])
    THREATS = deepcopy(TRANSACTION["THREATS"])
    PROJECTS = deepcopy(TRANSACTION["PROJECTS"])
    TRANSACTION = {}