from typing import Literal


__all__ = [
    "LogType",
    "EventTrigger",
    "LogModule",
    "CommandType",
    "HelpType",
    "HelpSubType"
]


type LogType = Literal["info", "warn", "error", "fatal", "debug"]
type EventTrigger = Literal["setup", "loop", "event", "command"]
type LogModule = Literal["bot", "peep", "config", "eastregg", "mod", "help"]
type CommandType = Literal["developer", "admin", "manager", "member"]

type HelpType = Literal["dev", "config", "usage"]
type HelpSubType = Literal["peep", "assignable_roles"]
