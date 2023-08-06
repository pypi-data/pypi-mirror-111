

class EventBase(object):
    event_name: str

    def run(self, **data):
        pass


class WalletCreateEvent(EventBase):
    event_name = "wallet_created"
    event_type = "Wallet"

    def run(self, **data):
        pass
