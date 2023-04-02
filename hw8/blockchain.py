from __future__ import annotations

import hashlib
import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from hw8.hashmap import CustomHashMap
else:
    from hashmap import CustomHashMap


@dataclass(frozen=True, slots=True)
class Transaction:
    sender: str
    receiver: str
    amount: int
    
    def __bytes__(self) -> bytes:
        return f"{self.sender}{self.receiver}{self.amount}".encode('ascii')
    
    def __str__(self) -> str:
        USER_LEN = 10 # noqa: N806
        
        if len(self.sender) > USER_LEN:
            sender_str = f"{self.sender[:USER_LEN-3]}..."
        else:
            sender_str = self.sender.ljust(USER_LEN)
        
        if len(self.receiver) > USER_LEN:
            receiver_str = f"{self.receiver[:USER_LEN-3]}..."
        else:
            receiver_str = self.receiver.ljust(USER_LEN)
        
        return f"{sender_str} -> {receiver_str}: {str(self.amount).zfill(5)} HSKYC"

class Block:
    transactions: list[Transaction]
    previous_block_hash: bytes
    
    def __init__(
        self,
        previous_block_hash: bytes,
        transactions: list[Transaction] = ...
    ) -> None:
        self.transactions = transactions if transactions is not ... else []
        self.previous_block_hash = previous_block_hash
    
    def __bytes__(self) -> bytes:
        # concatenate the previous block hash and all the transaction info
        return self.previous_block_hash + b"".join(bytes(t) for t in self.transactions)
    
    def __hash__(self) -> int:
        """Hash the block using SHA-256."""
        # take all the bytes of the block and hash them
        hash_bytes = hashlib.sha256(bytes(self), usedforsecurity=True).digest()
        return int.from_bytes(hash_bytes, byteorder='big')
    
    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
    
    def pretty_print(self) -> None:
        hash_str = hash(self).to_bytes(32).hex()
        prev_hash_str = self.previous_block_hash.hex().zfill(32)
        print(
            f"Current Block:  {hash_str}",
            f"Previous Block: {prev_hash_str}",
            "| " + " |\n| ".join(str(t) for t in self.transactions) + " |",
            sep='\n'
        )

class Ledger:
    _ledger_hashmap: CustomHashMap[str, int]
    
    def __init__(self, __map: CustomHashMap[str, int] = ...) -> None:
        self._ledger_hashmap = CustomHashMap() if __map is ... else __map
    
    def has_funds(self, user: str, amount: int) -> bool:
        """Check if the given user has at least the given amount of HuskyCoin."""
        balance = self._ledger_hashmap.get(user)
        
        if balance is None:
            return False
        
        return balance >= amount
    
    def deposit(self, user: str, amount: int) -> None:
        """Deposit the given amount of HuskyCoin to the given user."""
        if user not in self._ledger_hashmap:
            self._ledger_hashmap[user] = amount
        else:
            self._ledger_hashmap[user] += amount
    
    def withdraw(self, user: str, amount: int) -> None:
        """Withdraw the given amount of HuskyCoin from the given user.
        
        NOTE: according to the assignment, this method should be called "transfer",
        but that is incredibly confusing as it doesn't actually transfer money.
        """
        if user not in self._ledger_hashmap:
            raise ValueError(f"{user} does not have any HuskyCoin.")
        
        balance = self._ledger_hashmap.get(user)
        
        if balance is not None and balance < amount:
            raise ValueError(f"{user} does not have enough HuskyCoin.")
        
        self._ledger_hashmap[user] -= amount

class Blockchain:
    """Contains the chain of blocks."""
    
    _blockchain: list[Block]
    _bc_ledger: Ledger
    
    _ROOT_BC_USER = "ROOT"
    _BLOCK_REWARD = 1000
    _TOTAL_AVAILABLE_TOKENS = 999999
    
    def __init__(self) -> None:
        self._blockchain = []         # Use the Python List for the chain of blocks
        self._bc_ledger = Ledger()    # The ledger of HuskyCoin balances
        
        # Create the initial block0 of the blockchain, also called the "genesis block"
        self._create_genesis_block()
    
    # This method is complete. No additional code needed.
    def _create_genesis_block(self) -> None:
        """Create the initial block in the chain.
        
        This is NOT how a blockchain usually works, but it is a simple way to give the
        Root user HuskyCoin that can be subsequently given to other users.
        """
        trans0 = Transaction(
            self._ROOT_BC_USER,
            self._ROOT_BC_USER,
            self._TOTAL_AVAILABLE_TOKENS
        )
        block0 = Block(b"", [trans0])
        self._blockchain.append(block0)
        self._bc_ledger.deposit(
            self._ROOT_BC_USER,
            self._TOTAL_AVAILABLE_TOKENS
        )
    
    # This method is complete. No additional code needed.
    def distribute_mining_reward(self, user: str) -> None:
        """Give the given user `Blockchain._BLOCK_REWARD` HuskyCoin.
        
        You need to give HuskyCoin to some of your users before you can transfer
        HuskyCoin between users. Use this method to give your users an initial balance
        of HuskyCoin. (In the Bitcoin network, users compete to solve a meaningless
        mathmatical puzzle. Solving the puzzle takes a tremendious amount of copmputing
        power and consuming a lot of energy. The first node to solve the puzzle is given
        a certain amount of Bitcoin.) In this assigment, you do not need to understand
        "mining." Just use this method to provide initial balances to one or more users.
        """
        trans = Transaction(
            self._ROOT_BC_USER,
            user,
            self._BLOCK_REWARD
        )
        self.add_block([trans])
    
    # TODO - add the rest of the code for the class here
    def pretty_print(self) -> None:
        print(*self._blockchain, sep='\n')
    
    def add_block(self, transactions: list[Transaction]) -> None:
        """Add a block to the blockchain."""
        previous_block_hash = hash(self._blockchain[-1]).to_bytes(32)
        new_block = Block(previous_block_hash, transactions)
        
        # make a copy of the ledger to avoid modifying the original (verified) ledger
        new_ledger_map = Ledger(CustomHashMap(self._bc_ledger._ledger_hashmap)) # type: ignore # noqa: E501
        self._blockchain.append(new_block)
        
        for transaction in transactions:
            if new_ledger_map.has_funds(transaction.sender, transaction.amount):
                new_ledger_map.withdraw(transaction.sender, transaction.amount)
                new_ledger_map.deposit(transaction.receiver, transaction.amount)
            else:
                raise ValueError(
                    f"{transaction.sender} does not have enough HuskyCoin."
                )
        
        # if the ledger is valid, update the blockchain's ledger
        self._bc_ledger = new_ledger_map
    
    def validate_chain(self) -> list[Block]:
        """Return a list of blocks on the chain that have been modified."""
        return [
            block for i, block in enumerate(self._blockchain[:-1])
            if not self._is_valid_block(i)
        ]
    
    def _is_valid_block(self, block_idx: int) -> bool:
        """Return True if the block at the given index is valid."""
        block = self._blockchain[block_idx]
        next_block = self._blockchain[block_idx + 1]
        
        return hash(block).to_bytes(32) == next_block.previous_block_hash
