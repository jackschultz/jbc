from config import *
import datetime
import block

def is_valid_chain():
  '''
    We need to check to see if the entire chain is valid.
    To do this, we check if each block in order is valid.
    The is_valid() function in the Block class handles the
    hash connection between the previous and current block.
  '''
  for b in blockchain:
    if not b.is_valid():
      return False
  return True

def dict_from_block_attributes(**kwargs):
  info = {}
  for key in kwargs:
    if key in BLOCK_VAR_CONVERSIONS:
      info[key] = BLOCK_VAR_CONVERSIONS[key](kwargs[key])
    else:
      info[key] = kwargs[key]
  return info

def create_new_block_from_prev(prev_block=None, data=None, timestamp=None):
  if not prev_block:
    # index zero and arbitrary previous hash
    index = 0
    prev_hash = ''
  else:
    index = int(prev_block.index) + 1
    prev_hash = prev_block.hash

  if not data:
    filename = '%sdata.txt' % (CHAINDATA_DIR)
    with open(filename, 'r') as data_file:
      data = data_file.read()

  if not timestamp:
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

  nonce = 0
  block_info_dict = dict_from_block_attributes(index=index, timestamp=timestamp, data=data, prev_hash=prev_hash, nonce=nonce)
  new_block = block.Block(block_info_dict)
  return new_block

def find_valid_nonce(find_block, data=None):
  find_block.nonce = 0
  find_block.update_self_hash()#calculate_hash(index, prev_hash, data, timestamp, nonce)
  if not find_block.data:
    find_block.data = data
  while str(find_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
    find_block.nonce += 1
    find_block.update_self_hash()
  assert find_block.is_valid()
  return find_block
