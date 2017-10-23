import datetime as date
import time
import sync
import json
import hashlib
import requests
import os

from block import Block
from config import *

from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue

sched = BlockingScheduler()

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def run_mining():
  node_blocks = sync.sync() #gather last node
  prev_block = node_blocks[-1]
  new_block = mine_blocks(prev_block)
  broadcast_mined_block(new_block)
  new_block.self_save()
  #sched.add_job(run_mining, id='run_mining') #add the block again

def check_for_broadcasted_blocks():
  '''
    We need a way to check to see if someone's claimed they solved a block
  '''
  print "Checking for other node's blocks"
  if not os.listdir(BROADCASTED_BLOCK_DIR):
    print "No broadcasted blocks found"
    return
  print "Found broadcasted mined blocks"
  for filename in os.listdir(BROADCASTED_BLOCK_DIR):
    #first check to see if we've mined that block before
    bid = filename.split('_')[0]
    print "Possible new block index: %s" % bid
    index_string = str(bid).zfill(6)
    filepath = CHAINDATA_DIR + index_string + '.json'
    if os.path.exists(filepath):
      print "Block already exists in current chain. Ditching for now"
      #delete the possible new file
      os.remove(filename)
      continue #continue to the next possible blockfile
    #if that's the case, they we check to see who has the better timestamp
    new_block_filepath = '%s/%s' % (BROADCASTED_BLOCK_DIR, filename)
    with open(new_block_filepath, 'r') as block_file:
      block_info = json.load(block_file)
      block_object = Block(block_info)
      if not block_object.is_valid():
        print "Invalid block."
        continue
      print "Valid block number %s. Saving block." % bid
      block_object.self_save()

def broadcast_mined_block(block):
  '''
    We want to hit the other peers saying that we mined a block
  '''
  block_info_dict = block.to_dict()
  for peer in PEERS:
    #see if we can broadcast it
    try:
      r = requests.post(peer+'mined', json=block_info_dict)
    except requests.exceptions.ConnectionError:
      print "Peer %s not connected" % peer
      continue
  return True

def mine_blocks(last_block):
  index = int(last_block.index) + 1
  timestamp = date.datetime.now()
  data = "I block #%s" % (int(last_block.index) + 1) #random string for now, not transactions
  prev_hash = last_block.hash
  nonce = 0

  new_block = Block(index=index, timestamp=timestamp, data=data, prev_hash=prev_hash, nonce=nonce)

  print "mining for block %s" % index
  new_block.update_self_hash()#calculate_hash(index, prev_hash, data, timestamp, nonce)
  while str(new_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
    new_block.nonce += 1
    new_block.update_self_hash()

  print "block %s mined. Nonce: %s" % (index, nonce)

  '''
  #dictionary to create the new block object.
  block_data = {}
  block_data['index'] = index
  block_data['prev_hash'] = last_block.hash
  block_data['timestamp'] = timestamp
  block_data['data'] = "Gimme %s dollars" % index
  block_data['hash'] = block_hash
  block_data['nonce'] = nonce
  '''

  assert new_block.is_valid()
  return new_block #we mined the block. We're going to want to save it

  #return True

if __name__ == '__main__':

  #from worker import conn


  run_mining_job = sched.add_job(run_mining, id='run_mining')
  check_for_broadcasted_blocks_job = sched.add_job(check_for_broadcasted_blocks, 'interval', seconds=3)

  run_mining()


  sched.start()
