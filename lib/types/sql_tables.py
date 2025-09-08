__all__ = [
    "User",
    "Guild",
    "Member",
    "PspsChannel"
]


type CaughtPeeps = int | None
type ChannelId = int
type GuildId  = int
type LastPeep = str
type LogChannelId = int | None
type NoPeepMessage = str
type ReceivedPeeps = int
type ScratchMessage = str
type SentPeeps = int
type StolenPeeps = int | None
type SuccessMessage = str
type Tries = int
type UserId = int

type User = tuple[
    UserId,
    StolenPeeps
]
type Guild = tuple[
    GuildId,
    SuccessMessage,
    ScratchMessage,
    NoPeepMessage,
    LastPeep,
    LogChannelId
]
type Member = tuple[
    UserId,
    GuildId,
    LastPeep,
    CaughtPeeps,
    Tries,
    SentPeeps,
    ReceivedPeeps
]
type PspsChannel = tuple[
    ChannelId,
    GuildId
]