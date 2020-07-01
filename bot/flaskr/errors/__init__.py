class DuplicateBookError(Exception):
    pass


class DuplicateUserError(Exception):
    pass


class DuplicateLibraryError(Exception):
    pass


class BookNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class IsbnNotFound(Exception):
    pass


class MetadataNotFound(Exception):
    pass
