from block import Block
from chain import Chain

block_zero_dir = {"nonce": "631412", "index": "0", "hash": "000002f9c703dc80340c08462a0d6acdac9d0e10eb4190f6e57af6bb0850d03c", "timestamp": "1508895381", "prev_hash": "", "data": "First block data"}

block_one_dir = {"nonce": "1225518", "index": "1", "hash": "00000c575050241e0a4df1acd7e6fb90cc1f599e2cc2908ec8225e10915006cc", "timestamp": "1508895386", "prev_hash": "000002f9c703dc80340c08462a0d6acdac9d0e10eb4190f6e57af6bb0850d03c", "data": "I block #1"}

block_two_dir = {"nonce": "1315081", "index": "2", "hash": "000003cf81f6b17e60ef1e3d8d24793450aecaf65cbe95086a29c1e48a5043b1", "timestamp": "1508895393", "prev_hash": "00000c575050241e0a4df1acd7e6fb90cc1f599e2cc2908ec8225e10915006cc", "data": "I block #2"}

block_three_dir = {"nonce": "24959", "index": "3", "hash": "00000221653e89d7b04704d4690abcf83fdb144106bb0453683c8183253fabad", "timestamp": "1508895777", "prev_hash": "000003cf81f6b17e60ef1e3d8d24793450aecaf65cbe95086a29c1e48a5043b1", "data": "I block #3"}

block_three_later_in_time_dir = {"nonce": "46053", "index": "3", "hash": "000000257df186344486c2c3c1ebaa159e812ca1c5c29947651672e2588efe1e", "timestamp": "1508961173", "prev_hash": "000003cf81f6b17e60ef1e3d8d24793450aecaf65cbe95086a29c1e48a5043b1", "data": "I block #3"}

###########################
#
#  Block time
#
###########################

block_zero = Block(block_zero_dir)
another_block_zero = Block(block_zero_dir)
assert block_zero.is_valid()
assert block_zero == another_block_zero
assert not block_zero != another_block_zero

block_one = Block(block_one_dir)
another_block_one = Block(block_one_dir)
assert block_one.is_valid()
assert block_one == another_block_one

block_two = Block(block_two_dir)
another_block_two = Block(block_two_dir)
assert block_two.is_valid()
assert block_two == another_block_two

block_three = Block(block_three_dir)
another_block_three = Block(block_three_dir)
assert block_three.is_valid()
assert block_three == another_block_three

block_three_later_in_time = Block(block_three_later_in_time_dir)
assert block_three > block_three_later_in_time
assert not block_three < block_three_later_in_time

#incorrect prev_hash
block_one_dir_invalid = {"nonce": "1225518", "index": "1", "hash": "00000c575050241e0a4df1acd7e6fb90cc1f599e2cc2908ec8225e10915006cc", "timestamp": "1508895386", "prev_hash": "0000010101193736271818923939229219283747438293874548392789878987", "data": "I block #1"}
block_one_invalid_obj = Block(block_one_dir_invalid)
assert not block_one_invalid_obj.is_valid()
#nonce doesn't give it the correct hash
block_one_dir_invalid = {"nonce": "1000000", "index": "1", "hash": "00000c575050241e0a4df1acd7e6fb90cc1f599e2cc2908ec8225e10915006cc", "timestamp": "1508895386", "prev_hash": "000002f9c703dc80340c08462a0d6acdac9d0e10eb4190f6e57af6bb0850d03c", "data": "I block #1"}
block_one_invalid_obj = Block(block_one_dir_invalid)
assert not block_one_invalid_obj.is_valid()


#####################################
#
#  Bringing Chains into play
#
#####################################
blockchain = Chain([block_zero, block_one, block_two])
assert blockchain.is_valid()
assert len(blockchain) == 3

empty_chain = Chain([])
assert len(empty_chain) == 0
empty_chain.add_block(block_zero)
assert len(empty_chain) == 1
empty_chain = Chain([])
assert len(empty_chain) == 0

another_blockchain = Chain([another_block_zero, another_block_one, another_block_two])
assert another_blockchain.is_valid()
assert len(another_blockchain) == 3

assert blockchain == another_blockchain
assert not blockchain != another_blockchain
assert blockchain <= another_blockchain
assert blockchain >= another_blockchain
assert not blockchain > another_blockchain
assert not another_blockchain < blockchain

blockchain.add_block(block_three)
assert blockchain.is_valid()
assert len(blockchain) == 4
assert not blockchain == another_blockchain
assert blockchain != another_blockchain
assert not blockchain <= another_blockchain
assert blockchain >= another_blockchain
assert blockchain > another_blockchain
assert another_blockchain < blockchain


