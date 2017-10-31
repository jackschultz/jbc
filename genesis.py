import os
from config import *
from mine import find_valid_nonce
from block import Block
import datetime

def generate_first_block():
  # index zero and arbitrary previous hash
  block_data = {}
  block_data['index'] = 0
  block_data['timestamp'] = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
  block_data['data'] = 'First block data'
  block_data['prev_hash'] = ''
  block_data['nonce'] = 0 #starting it at 0
  return Block(block_data)

if __name__ == '__main__':
  #check if dir is empty from just creation, or empty before
  if not os.path.exists(CHAINDATA_DIR):
    #check if chaindata folder exists.
    os.mkdir(CHAINDATA_DIR)
    #create and save first block
  #if os.listdir(CHAINDATA_DIR) == []:
  first_block = generate_first_block()
  first_block = find_valid_nonce(first_block)
  first_block.self_save()

