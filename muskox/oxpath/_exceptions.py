from muskox.exceptions import MuskoxException


class OxpathException(MuskoxException):
    pass


class OxpathNotFound(OxpathException):
    pass


class SpecificationMismatch(OxpathException):
    pass


class UnsupportedService(SpecificationMismatch):
    pass


class EmptyPath(SpecificationMismatch):
    pass


class EmptyService(SpecificationMismatch):
    pass


class EmptyUsername(SpecificationMismatch):
    pass


class EmptyRepository(SpecificationMismatch):
    pass
