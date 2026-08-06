from uuid import UUID, uuid4
from dataclasses import dataclass, field
from src.domain.enums.transaction_type import TransactionType
from src.domain.enums.transaction_status import TransactionStatus

@dataclass(kw_only=True)
class Transaction:
    id: UUID = field(default_factory=uuid4)
    sender_id: UUID
    receiver_id: UUID
    transaction_type: TransactionType
    status: TransactionStatus

    gold_amount: int = 0
    item_id: UUID | None = None