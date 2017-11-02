from block import Block
from chain import Chain
import mine
import utils
import datetime
from freezegun import freeze_time

block_zero_dir = {"nonce": "631412", "index": "0", "hash": "000002f9c703dc80340c08462a0d6acdac9d0e10eb4190f6e57af6bb0850d03c", "timestamp": "1508895381", "prev_hash": "", "data": "First block data"}

block_one_dir = {"nonce": "1225518", "index": "1", "hash": "00000c575050241e0a4df1acd7e6fb90cc1f599e2cc2908ec8225e10915006cc", "timestamp": "1508895386", "prev_hash": "000002f9c703dc80340c08462a0d6acdac9d0e10eb4190f6e57af6bb0850d03c", "data": "I block #1"}

block_two_dir = {"nonce": "1315081", "index": "2", "hash": "000003cf81f6b17e60ef1e3d8d24793450aecaf65cbe95086a29c1e48a5043b1", "timestamp": "1508895393", "prev_hash": "00000c575050241e0a4df1acd7e6fb90cc1f599e2cc2908ec8225e10915006cc", "data": "I block #2"}

block_three_dir = {"nonce": "24959", "index": "3", "hash": "00000221653e89d7b04704d4690abcf83fdb144106bb0453683c8183253fabad", "timestamp": "1508895777", "prev_hash": "000003cf81f6b17e60ef1e3d8d24793450aecaf65cbe95086a29c1e48a5043b1", "data": "I block #3"}

block_three_later_in_time_dir = {"nonce": "46053", "index": "3", "hash": "000000257df186344486c2c3c1ebaa159e812ca1c5c29947651672e2588efe1e", "timestamp": "1508961173", "prev_hash": "000003cf81f6b17e60ef1e3d8d24793450aecaf65cbe95086a29c1e48a5043b1", "data": "I block #3"}

block_zero = Block(block_zero_dir)
block_one = Block(block_one_dir)
block_two = Block(block_two_dir)
block_three = Block(block_three_dir)

###########################
#
#  Block time
#
###########################

another_block_zero = Block(block_zero_dir)
assert block_zero.is_valid()
assert block_zero == another_block_zero
assert not block_zero != another_block_zero

another_block_one = Block(block_one_dir)
assert block_one.is_valid()
assert block_one == another_block_one

another_block_two = Block(block_two_dir)
assert block_two.is_valid()
assert block_two == another_block_two

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
'''

#####################################
#
#  Mining
#
#####################################

'''
with freeze_time(zt):
  poss_block_zero = utils.create_new_block_from_prev(data='Mine test block zero.')
  mine_test_block_zero = utils.find_valid_nonce(poss_block_zero)

with freeze_time(ft):
  poss_block_one = utils.create_new_block_from_prev(prev_block=mine_test_block_zero, data='Mine test block one.')
  mine_test_block_one = utils.find_valid_nonce(poss_block_one)

with freeze_time(st):
  poss_block_two = utils.create_new_block_from_prev(prev_block=mine_test_block_one, data='Mine test block two.')
  mine_test_block_two = utils.find_valid_nonce(poss_block_two)
with freeze_time(tt):
  poss_block_three = utils.create_new_block_from_prev(prev_block=mine_test_block_two, data='Mine test block three.')
  mine_test_block_three = utils.find_valid_nonce(poss_block_three)

print mine_test_block_three.__dict__

#times for mining zero, first, second, and third blocks
#freezegun generation
zt = "2012-11-01 12:00:01"
ft = "2012-11-02 12:00:01"
st = "2012-11-03 12:00:01"
tt = "2012-11-04 12:00:01"

mine_test_block_zero_dict = {'nonce': 1185358, 'index': 0, 'hash': '00000ff000e7c05047d0acdc8652f096db4115ed8882949a0dc0dbf21666fbec', 'timestamp': 20121101120001000000L, 'prev_hash': '', 'data': 'Mine test block zero.'}
mine_test_block_zero = Block(mine_test_block_zero_dict)

mine_test_block_one_dict = {'nonce': 1685195, 'index': 1, 'hash': '00000ff7cfc90b72c371afb451a4203ee194fed64574f4b99db9faf1722831ca', 'timestamp': 20121102120001000000L, 'prev_hash': '00000ff000e7c05047d0acdc8652f096db4115ed8882949a0dc0dbf21666fbec', 'data': 'Mine test block one.'}
mine_test_block_one = Block(mine_test_block_one_dict)

mine_test_block_two_dict = {'nonce': 366523, 'index': 2, 'hash': '000004f2294896ed248d112922e5a2b98596ddcaba5923d2917cb79650ffbc24', 'timestamp': 20121103120001000000L, 'prev_hash': '00000ff7cfc90b72c371afb451a4203ee194fed64574f4b99db9faf1722831ca', 'data': 'Mine test block two.'}
mine_test_block_two = Block(mine_test_block_two_dict)

mine_test_block_three_dict = {'nonce': 590929, 'index': 3, 'hash': '0000038edddd9610a4d5f11036dfa153ff678eba9b122e3e41dcc80eb247bfb4', 'timestamp': 20121104120001000000L, 'prev_hash': '000004f2294896ed248d112922e5a2b98596ddcaba5923d2917cb79650ffbc24', 'data': 'Mine test block three.'}
mine_test_block_three = Block(mine_test_block_three_dict)

mine_test_chain = Chain([mine_test_block_zero, mine_test_block_one, mine_test_block_two, mine_test_block_three])
assert mine_test_chain.is_valid()

mine_test_zero_chain = Chain([mine_test_block_zero])
assert mine_test_zero_chain.is_valid()

with freeze_time(ft):
  poss_block_one = utils.create_new_block_from_prev(prev_block=mine_test_block_zero, data='Mine test block one.')

  #mine_block(new_block, rounds=STANDARD_ROUNDS, start_nonce=0)
  new_block, rounds, start_nonce = mine.mine_block(poss_block_one, rounds=1000, start_nonce=0)
  assert not new_block
  assert rounds == 1000
  assert start_nonce == 0
  new_block, rounds, start_nonce = mine.mine_block(poss_block_one, rounds=1000, start_nonce=1685000)
  assert new_block == mine_test_block_one
  assert rounds == 1000
  assert start_nonce == 1685000

  #mine_from_prev_block(prev_block, rounds=STANDARD_ROUNDS, start_nonce=0)
  new_block, rounds, start_nonce = mine.mine_from_prev_block(mine_test_block_zero, rounds=1000, start_nonce=0)
  assert not new_block
  assert rounds == 1000
  assert start_nonce == 0
  new_block, rounds, start_nonce = mine.mine_from_prev_block(mine_test_block_zero, rounds=1000, start_nonce=1685000)
  assert new_block == mine_test_block_one
  assert rounds == 1000
  assert start_nonce == 1685000

  #mine_for_block(chain=None, rounds=STANDARD_ROUNDS, start_nonce=0)
  new_block, rounds, start_nonce = mine.mine_for_block(chain=mine_test_zero_chain, rounds=1000, start_nonce=0)
  assert not new_block
  assert rounds == 1000
  assert start_nonce == 0
  new_block, rounds, start_nonce = mine.mine_for_block(chain=mine_test_zero_chain, rounds=1000, start_nonce=1685000)
  assert new_block == mine_test_block_one
  assert rounds == 1000
  assert start_nonce == 1685000

