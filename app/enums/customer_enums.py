import enum


class LeadSource(str, enum.Enum):
    SCANNER = "scanner"
    PARTNER = "partner"
    MANUAL = "manual"


class LeadStage(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    TRANSFERRED = "transferred"
    LOST = "lost"


class BusinessDomain(str, enum.Enum):
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"


class SaleStage(str, enum.Enum):
    NEW = "new"
    KYC = "kyc"
    AGREEMENT = "agreement"
    PAID = "paid"
    LOST = "lost"
