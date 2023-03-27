# ruff: noqa: ANN201

import typing
import unittest

if typing.TYPE_CHECKING:
    from hw8.blockchain import Block, Blockchain, Ledger, Transaction
    from hw8.hashmap import CustomHashMap
    from hw8.hashmap_test import TestCustomHashMap
else:
    from blockchain import Block, Blockchain, Ledger, Transaction
    from hashmap import CustomHashMap
    from hashmap_test import TestCustomHashMap  # noqa: TCH002

class TestTransaction(unittest.TestCase):
    def test_transaction_init(self):
        transaction = Transaction("sender", "receiver", 123)
        self.assertEqual(transaction.sender, "sender")
        self.assertEqual(transaction.receiver, "receiver")
        self.assertEqual(transaction.amount, 123)
    
    def test_transaction_bytes(self):
        transaction = Transaction("sender", "receiver", 123)
        self.assertEqual(bytes(transaction), b"senderreceiver123")
    
    def test_transaction_str(self):
        transaction = Transaction("sender", "receiver", 123)
        self.assertEqual(str(transaction), "sender     -> receiver  : 00123 HSKYC")

class TestBlock(unittest.TestCase):
    def test_block_init(self):
        block = Block(b"previous_block_hash")
        self.assertEqual(block.transactions, [])
        self.assertEqual(block.previous_block_hash, b"previous_block_hash")
    
    def test_block_add_transaction(self):
        block = Block(b"previous_block_hash")
        transaction = Transaction("sender", "receiver", 123)
        block.add_transaction(transaction)
        self.assertEqual(block.transactions, [transaction])
    
    def test_block_bytes(self):
        block = Block(b"previous_block_hash")
        block.add_transaction(Transaction("sender", "receiver", 123))
        block.add_transaction(Transaction("receiver", "sender", 456))
        self.assertEqual(
            bytes(block),
            b"previous_block_hashsenderreceiver123receiversender456"
        )
    
    def test_block_hash(self):
        block = Block(b"previous_block_hash")
        transaction = Transaction("sender", "receiver", 123)
        block.add_transaction(transaction)
        block.add_transaction(transaction)
        
        # NOTE: this is the SHA-256 hash of
        # b"previous_block_hashsenderreceiver123senderreceiver123"
        expected = 0xb2aacbc7cb95b479b7194f8e22491f07aba7746decb1c165acb1763e4e676c93
        
        # NOTE: we cant use hash() because it is not guaranteed to be the same across
        # different runs of the program, so we have to directly call __hash__() instead.
        self.assertEqual(block.__hash__(), expected)

class TestLedger(unittest.TestCase):
    def test_ledger_init(self):
        ledger = Ledger()
        self.assertIsInstance(ledger._ledger_hashmap, CustomHashMap)
        self.assertEqual(ledger._ledger_hashmap, CustomHashMap())
    
    def test_ledger_deposit(self):
        ledger = Ledger()
        ledger.deposit('sender', 123)
        ledger.deposit('receiver', 456)
        self.assertEqual(ledger._ledger_hashmap, CustomHashMap({
            'sender': 123,
            'receiver': 456,
        }))
    
    def test_ledger_has_funds(self):
        ledger = Ledger()
        ledger.deposit('sender', 123)
        self.assertTrue(ledger.has_funds('sender', 123))
        self.assertFalse(ledger.has_funds('sender', 124))
    
    def test_ledger_withdraw(self):
        ledger = Ledger()
        ledger.deposit('sender', 123)
        ledger.withdraw('sender', 123)
        self.assertEqual(ledger._ledger_hashmap, CustomHashMap({
            'sender': 0,
        }))

class TestBlockchain(unittest.TestCase):
    def test_blockchain_init(self):
        blockchain = Blockchain()
        self.assertIsInstance(blockchain._bc_ledger, Ledger)
        self.assertIsInstance(blockchain._blockchain, list)
    
    def test_blockchain_create_genesis_block(self):
        # test to make sure _create_genesis_block is called on __init__
        blockchain = Blockchain()
        
        # check block attributes
        self.assertEqual(len(blockchain._blockchain), 1)
        self.assertIsInstance(blockchain._blockchain[0], Block)
        self.assertEqual(blockchain._blockchain[0].previous_block_hash, b"")
        
        # check ledger attributes
        self.assertEqual(blockchain._bc_ledger._ledger_hashmap, CustomHashMap({
            Blockchain._ROOT_BC_USER: Blockchain._TOTAL_AVAILABLE_TOKENS,
        }))
    
    def test_blockchain_distribute_mining_reward(self):
        blockchain = Blockchain()
        blockchain.distribute_mining_reward("sender")
        self.assertEqual(blockchain._bc_ledger._ledger_hashmap, CustomHashMap({
            Blockchain._ROOT_BC_USER:
                Blockchain._TOTAL_AVAILABLE_TOKENS - Blockchain._BLOCK_REWARD,
            "sender": Blockchain._BLOCK_REWARD,
        }))
    
    def test_blockchain_add_block(self):
        blockchain = Blockchain()
        blockchain.distribute_mining_reward("sender")
        transactions = [
            Transaction("sender", "receiver", 123)
        ]
        blockchain.add_block(transactions)
        self.assertEqual(len(blockchain._blockchain), 3)
        self.assertEqual(blockchain._blockchain[2].transactions, transactions)
    
    def test_blockchain_validate_chain(self):
        blockchain = Blockchain()
        blockchain.distribute_mining_reward("sender")
        transactions = [
            Transaction("sender", "receiver", 123)
        ]
        blockchain.add_block(transactions)
        self.assertEqual(blockchain.validate_chain(), [])
        
        # test for invalid block
        blockchain._blockchain[0].transactions.append(
            Transaction(Blockchain._ROOT_BC_USER, "bad_sender", 10000)
        )
        self.assertEqual(blockchain.validate_chain(), [blockchain._blockchain[0]])
        blockchain._blockchain[0].transactions.pop()
        self.assertEqual(blockchain.validate_chain(), [])
        
        # test for invalid hash
        blockchain._blockchain[1].previous_block_hash = b"invalid_hash"
        self.assertEqual(blockchain.validate_chain(), [
            blockchain._blockchain[0],
            blockchain._blockchain[1]
        ])
        blockchain._blockchain[1].previous_block_hash = \
            hash(blockchain._blockchain[0]).to_bytes(32)
        self.assertEqual(blockchain.validate_chain(), [])


if typing.TYPE_CHECKING:
    class TestHashMap(TestCustomHashMap):
        pass

if __name__ == "__main__":
    unittest.main()
