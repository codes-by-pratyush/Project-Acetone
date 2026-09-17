class WalletMonitor:
    def __init__(self):
        self.watched_wallets = set()

    def add_wallet(self, wallet_address):
        self.watched_wallets.add(wallet_address.lower())

    def remove_wallet(self, wallet_address):
        self.watched_wallets.discard(wallet_address.lower())

    def is_watched(self, wallet_address):
        return wallet_address.lower() in self.watched_wallets

    def get_watched_wallets(self):
        return list(self.watched_wallets)