from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


class TransactionType(str, enum.Enum):
    SUBSCRIPTION = "subscription"
    RENEWAL = "renewal"
    CANCELLATION = "cancellation"
    REFUND = "refund"


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    subscription_id = Column(Integer, index=True, nullable=True)
    # ID da transação no gateway
    transaction_id = Column(String, index=True, unique=True)
    payment_gateway = Column(String, index=True)  # stripe, hotmart
    # subscription, renewal, cancellation, refund
    transaction_type = Column(String)
    amount = Column(Float)
    currency = Column(String, default="BRL")
    status = Column(String, default=TransactionStatus.PENDING)
    error_message = Column(Text, nullable=True)
    # Dados adicionais da transação
    transaction_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<PaymentTransaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, status={self.status})>"
