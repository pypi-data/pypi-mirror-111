import logging
from logging.handlers import TimedRotatingFileHandler

from sqlalchemy.orm import Session

from .base import BaseNetworkClient


# from vc.
from vc.client.soldo import user, wallets, card, group, order
from vc.models.soldo import WalletSo, CardSo
from vc.settings import Settings
from .soldo_event import EventMixer
from vc.libs.utils import set_config

logger = logging.getLogger(__name__)


class SoldoException(Exception):

    def __init__(self, msg: str, response_data: dict):
        self.msg = msg
        self.response_data = response_data

    def __str__(self):
        return f"{self.msg}, {str(self.response_data)}"


class Soldo(EventMixer, BaseNetworkClient):
    settings = Settings({
        "ACCESS_TOKEN": "9xD6LYeAF0ddKRcuChVBQyTtLy04QpIm",
    })
    event_list = ["new_user", "wallet_created"]

    def __init__(self, name, uri,
                 api_url: str,
                 client_id: str,
                 client_secret: str,
                 group_id: str,
                 token: str,
                 filepath_private_pem: str,log_file: str = None, currency="USD", user_model=None, **config):
        data = dict(name=name, currency = currency,
                                     CLIENT_ID=client_id,
                                     CLIENT_SECRET=client_secret,
                                     API_URL=api_url,
                                     TOKEN=token,
                                     USER_MODEL=user_model,
                                    LOG_FILE=log_file,
                                     PATH_RSA_PRIVATE=filepath_private_pem,
                                     GROUP_ID = group_id, **config)
        set_config(logger, filename=Soldo.settings.LOG_FILE)
        Soldo.settings.update_config(**data)
        super().__init__(uri, user_model=user_model, **config)

    def oauth_authorize(self):
        return user.oauth_authorize()

    def whoami(self):
        return user.whoami()

    def user_update(self, id, **kwargs):
        return user.update(id, **kwargs)

    def get_wallets(self,  **kwargs):
        response_data = wallets.search(**kwargs)
        print(response_data)
        return response_data

    def create_wallet(self, db: Session, id: int, name: str = None, owner_type="company"):
        wallet = db.query(WalletSo).filter(WalletSo.id == id).first()
        if not name:
            name = wallet.user.email

        response_data = wallets.create(owner_type, self.settings.currency, name)
        order = response_data.data
        if not order.is_valid or order.status != "PLACED":
            raise SoldoException("Error create_wallet", response_data.dict())

        if order.items:
            wallet.search_id = order.items[0].id
            self.save_obj(db, wallet)

        return wallet

    def create_user(self, db: Session, id: int):
        u = db.query(self._user).filter(self._user.id==id).first()

        response_data = user.create(u.email, u.first_name, u.last_name, u.id, u.job_title)
        if response_data.data.status != "PLACED" or not response_data.data.is_valid:
            raise SoldoException("Error create_user", response_data.dict())
        return u

    def get_card(self, card_id: str, showSensitiveData: str = None):
        return card.get(card_id, showSensitiveData)

    def create_card(self, db: Session, user_id: int,
                    name: str = None, emboss_line4: str=None, type="VIRTUAL", card_label=None):
        wallet = db.query(WalletSo).filter(WalletSo.user_id == user_id).first()
        user = wallet.user

        if not card_label:
            card_label = self.settings.name

        if not name:
            name = user.email
        print(user.soldo_id)
        print(wallet.search_id)
        response_data = card.create(owner_public_id=user.soldo_id,
            wallet_id=wallet.search_id,
            name=name,
            emboss_line4=emboss_line4,
            type=type,
            card_label=card_label)
        order = response_data.data

        if not order.is_valid or order.status != "PLACED":
            raise SoldoException("Error create_card", response_data.dict())
        card_so = CardSo(search_id=order.id, wallet_id=wallet.id)

        self.save_obj(db, card_so)
        return card_so

    def add_item_to_group(self, id: str, type="WALLET",  groupId: str = None):
        if not groupId:
            groupId = self.settings.GROUP_ID
        return group.group_write(groupId, id, type)

    def get_order(self, order_id: str):
        return order.get(order_id)
