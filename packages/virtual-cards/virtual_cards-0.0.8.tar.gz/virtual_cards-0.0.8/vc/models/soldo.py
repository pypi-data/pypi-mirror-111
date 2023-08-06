from sqlalchemy import Column, Numeric, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import CardBase, WalletBase, DateFixedMixin, CardType, CardStatus
from vc.db.base_class import Base


class SoldoStatusToSystem(str.__class__):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> bool:
        if isinstance(v, str):
            if v == "Normal":
                return CardStatus.active.value
        return CardStatus.pending.value


class WalletSo(WalletBase, DateFixedMixin, Base):
    __tablename__ = "soldo_wallet"
    blocked_balance = Column(Numeric, default=0)
    user = relationship("UserBase", back_populates="wallet_soldo")


class CardSo(CardBase, DateFixedMixin, Base):
    __tablename__ = "soldo_card"
    wallet_id = Column(Integer, ForeignKey("soldo_wallet.id", ondelete="CASCADE"))
    wallet = relationship("WalletSo", backref="cards")
    blocked_balance = Column(Numeric, default=0)
    type = Column(String, default=CardType.virtual.value)
