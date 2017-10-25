import datetime as date
import time
import sync
import json
import hashlib
import requests
import os
import glob

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
  #need to check to see if we've been broadcasted a block before this one
  if True:
    pass
  else:
    #if not, we broadcast ourselves and save if!
    broadcast_mined_block(new_block)
  new_block.self_save()
  #sched.add_job(run_mining, id='run_mining') #add the block again

def possible_block_analysis(block_filepath):
  print "Filepath: %s" % possible_block_filepath
  #filename here is the entire path to the *.json file
  #we need the block id we're dealing with
  #Load the file into a block
  with open(possible_block_filepath, 'r') as block_file:
    block_info = json.load(block_file)
    possible_block = Block(block_info)
    if not possible_block.is_valid():
      print "Invalid block."
      os.remove(possible_block_filepath)

  pbid = possible_block.index

  #want to see if we have a file that already exists for this block's index
  index_string = str(pbid).zfill(6)
  valid_indexed_block_filepath = CHAINDATA_DIR + index_string + '.json'

  if os.path.exists(valid_indexed_block_filepath):
    print "Block already exists in current chain. Ditching broadcasted for now"
    #delete the possible new file
    os.remove(possible_block_filepath)

  #if that's the case, they we check to see who has the better timestamp
  #TODO not this, cause that's a dumb way to know who's right in a blockchain!!

  #then we saving the new valid block into the chain, and then deleting
  #the possible block from the filepath
  with open(valid_indexed_block_filepath, 'w') as block_file:
    print "Valid block number %s. Saving block." % possible_block.index
    possible_block.self_save()

  #remove file from possible block object no matter what we go
  os.remove(possible_block_filepath)

def check_for_broadcasted_blocks():
  '''
    We need a way to check to see if someone's claimed they solved a block
  '''
  print "Checking for other node's blocks"
  if not os.listdir(BROADCASTED_BLOCK_DIR):
    print "No broadcasted blocks found"
    return
  print "Found broadcasted mined blocks"
  for possible_block_filepath in glob.glob(os.path.join(BROADCASTED_BLOCK_DIR, '*.json')):
    possible_block_analysis(possible_block_filepath)

  #stop current run_mining operation because we lost
  #the restart run_mining to attempt the next one.
  #sched.add_job(run_mining, id='run_mining') #add the block again

def broadcast_mined_block(new_block):
  '''
    We want to hit the other peers saying that we mined a block
  '''
  block_info_dict = new_block.to_dict()
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
  timestamp = date.datetime.now().strftime('%s')
  data = "I block #%s" % (int(last_block.index) + 1) #random string for now, not transactions
  prev_hash = last_block.hash
  nonce = 0

  new_block = Block(index=index, timestamp=timestamp, data=data, prev_hash=prev_hash, nonce=nonce)
  return find_valid_nonce(new_block)

def find_valid_nonce(new_block):
  print "mining for block %s" % new_block.index
  new_block.update_self_hash()#calculate_hash(index, prev_hash, data, timestamp, nonce)
  while str(new_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
    new_block.nonce += 1
    new_block.update_self_hash()

  print "block %s mined. Nonce: %s" % (new_block.index, new_block.nonce)

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

  #run_mining_job = sched.add_job(run_mining, id='run_mining')
  run_mining()
  #check_for_broadcasted_blocks_job = sched.add_job(check_for_broadcasted_blocks, 'interval', seconds=3)

  #sched.start()
