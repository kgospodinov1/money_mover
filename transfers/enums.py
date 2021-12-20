import enum


class MoneyTransferStatusEnum(enum.Enum):
    FAILED = -1
    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3
