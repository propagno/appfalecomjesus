from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.future import select
from typing import List, Optional, Dict
from datetime import datetime

from app.models import PaymentTransaction, TransactionStatus


class PaymentTransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: str, transaction_id: str, payment_gateway: str,
                     transaction_type: str, amount: float, currency: str = "BRL",
                     status: str = TransactionStatus.PENDING, subscription_id: Optional[int] = None,
                     metadata: Optional[Dict] = None) -> PaymentTransaction:
        """Cria uma nova transação de pagamento."""
        now = datetime.utcnow()

        transaction = PaymentTransaction(
            user_id=user_id,
            subscription_id=subscription_id,
            transaction_id=transaction_id,
            payment_gateway=payment_gateway,
            transaction_type=transaction_type,
            amount=amount,
            currency=currency,
            status=status,
            transaction_metadata=metadata or {},
            created_at=now,
            updated_at=now
        )

        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    async def get_by_id(self, transaction_id: int) -> Optional[PaymentTransaction]:
        """Busca uma transação pelo ID interno."""
        query = select(PaymentTransaction).where(
            PaymentTransaction.id == transaction_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_transaction_id(self, transaction_id: str) -> Optional[PaymentTransaction]:
        """Busca uma transação pelo ID da transação no gateway de pagamento."""
        query = select(PaymentTransaction).where(
            PaymentTransaction.transaction_id == transaction_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_user_id(self, user_id: str, limit: int = 10, offset: int = 0) -> List[PaymentTransaction]:
        """Retorna as transações de um usuário."""
        query = select(PaymentTransaction).where(PaymentTransaction.user_id == user_id) \
            .order_by(PaymentTransaction.created_at.desc()) \
            .limit(limit).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_subscription_id(self, subscription_id: int) -> List[PaymentTransaction]:
        """Retorna as transações associadas a uma assinatura."""
        query = select(PaymentTransaction).where(PaymentTransaction.subscription_id == subscription_id) \
            .order_by(PaymentTransaction.created_at.desc())

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_status(self, transaction_id: int, status: str,
                            error_message: Optional[str] = None,
                            metadata: Optional[Dict] = None) -> Optional[PaymentTransaction]:
        """Atualiza o status de uma transação."""
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }

        if error_message is not None:
            update_data["error_message"] = error_message

        if metadata is not None:
            # Precisamos mesclar os metadados existentes com os novos
            transaction = await self.get_by_id(transaction_id)
            if transaction and transaction.transaction_metadata:
                existing_metadata = transaction.transaction_metadata
                existing_metadata.update(metadata)
                update_data["transaction_metadata"] = existing_metadata
            else:
                update_data["transaction_metadata"] = metadata

        stmt = update(PaymentTransaction).where(
            PaymentTransaction.id == transaction_id).values(**update_data)
        await self.session.execute(stmt)
        await self.session.commit()

        return await self.get_by_id(transaction_id)

    async def find_successful_transaction(self, user_id: str, transaction_type: str) -> Optional[PaymentTransaction]:
        """Busca a transação bem-sucedida mais recente de um tipo específico."""
        query = select(PaymentTransaction).where(
            (PaymentTransaction.user_id == user_id) &
            (PaymentTransaction.transaction_type == transaction_type) &
            (PaymentTransaction.status == TransactionStatus.COMPLETED)
        ).order_by(PaymentTransaction.created_at.desc()).limit(1)

        result = await self.session.execute(query)
        return result.scalars().first()
