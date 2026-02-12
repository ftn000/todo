class DomainError(Exception):
    pass


class FocusAlreadySetError(DomainError):
    pass


class CannotFocusCompletedTaskError(DomainError):
    pass


class TaskNotFoundError(DomainError):
    pass