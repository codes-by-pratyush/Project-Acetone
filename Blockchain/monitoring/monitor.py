from Blockchain.providers.ethereum import (
    get_new_wallet_transfers,
    normalize_transfer,
)


class WalletMonitor:
    def __init__(self):
        self.watched_wallets = set()
        self.last_checked_blocks = {}

    def add_wallet(self, wallet_address, start_block=0):
        wallet_address = wallet_address.lower()

        self.watched_wallets.add(wallet_address)
        self.last_checked_blocks[wallet_address] = start_block

    def remove_wallet(self, wallet_address):
        wallet_address = wallet_address.lower()

        self.watched_wallets.discard(wallet_address)
        self.last_checked_blocks.pop(wallet_address, None)

    def is_watched(self, wallet_address):
        return wallet_address.lower() in self.watched_wallets

    def get_watched_wallets(self):
        return list(self.watched_wallets)

    def check_wallet(self, wallet_address):
        wallet_address = wallet_address.lower()

        if wallet_address not in self.watched_wallets:
            return [], None

        last_checked_block = self.last_checked_blocks[wallet_address]

        transfers, latest_block = get_new_wallet_transfers(
            wallet_address,
            last_checked_block
        )

        normalized_transfers = [
            normalize_transfer(transfer)
            for transfer in transfers
        ]

        relevant_transfers = []

        for transfer in normalized_transfers:
            watched_wallets = self.process_transfer(transfer)

            if watched_wallets:
                relevant_transfers.append(transfer)

        self.last_checked_blocks[wallet_address] = latest_block

        return relevant_transfers, latest_block

    def process_transfer(self, transfer):
        from_address = transfer.get("from_address")
        to_address = transfer.get("to_address")

        watched = []

        if from_address and self.is_watched(from_address):
            watched.append(from_address.lower())

        if to_address and self.is_watched(to_address):
            watched.append(to_address.lower())

        return watched