from web3 import Web3


def to_checksum(accountAddress):
    try:
        checksum_addr = Web3.toChecksumAddress(accountAddress)
        return checksum_addr
    except Exception:
        raise
