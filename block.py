import hashlib
import os
import json
import datetime as date

CHAINDATA_DIR = 'chaindata/'
BROADCASTED_BLOCK_DIR = CHAINDATA_DIR + 'bblocs/'

class Block(object):
  def __init__(self, dictionary):
    '''
      We're looking for index, timestamp, data, prev_hash, nonce
    '''
    for k, v in dictionary.items():
      setattr(self, k, v)

    if not hasattr(self, 'nonce'):
      #we're throwin this in for generation
      self.nonce = 'None'
    if not hasattr(self, 'hash'): #in creating the first block, needs to be removed in future
      self.hash = self.create_self_hash()

  def header_string(self):
    return str(self.index) + self.prev_hash + self.data + str(self.timestamp) + str(self.nonce)

  def create_self_hash(self):
    sha = hashlib.sha256()
    sha.update(self.header_string())
    return sha.hexdigest()

  def self_save(self):
    index_string = str(self.index).zfill(6) #front of zeros so they stay in numerical order
    filename = '%s/%s.json' % (CHAINDATA_DIR, index_string)
    with open(filename, 'w') as block_file:
      json.dump(self.to_dict(), block_file)

  def to_dict(self):
    info = {}
    info['index'] = str(self.index)
    info['timestamp'] = str(self.timestamp)
    info['prev_hash'] = str(self.prev_hash)
    info['hash'] = str(self.hash)
    info['data'] = str(self.data)
    info['nonce'] = str(self.nonce)
    return info

  def is_valid(self):
    return True

  def __str__(self):
    return "Block<prev_hash: %s,hash: %s>" % (self.prev_hash, self.hash)

def create_first_block():
  # index zero and arbitrary previous hash
  block_data = {}
  block_data['index'] = 0
  block_data['timestamp'] = date.datetime.now()
  block_data['data'] = 'First block data'
  block_data['prev_hash'] = ''
  block_data['nonce'] = 0 #starting it at 0
  return Block(block_data)

if __name__ == '__main__':
  #check if chaindata folder exists.
  if not os.path.exists(CHAINDATA_DIR):
    #make chaindata dir and broadcasted block dir
    os.mkdir(CHAINDATA_DIR)
    os.mkdir(BROADCASTED_BLOCK_DIR)
  #check if dir is empty from just creation, or empty before
  if os.listdir(CHAINDATA_DIR) == []:
    #create and save first block
    first_block = create_first_block()
    first_block.self_save()
  if not os.path.exists(BROADCASTED_BLOCK_DIR):
    #have to check to see if the broadcasted block dir exists as well
    os.mkdir(BROADCASTED_BLOCK_DIR)
