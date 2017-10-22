import datetime as date
import time
import sync
import json
import hashlib
import requests

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

def generate_header(index, prev_hash, data, timestamp, nonce):
  return str(index) + prev_hash + data + str(timestamp) + str(nonce)

def calculate_hash(index, prev_hash, data, timestamp, nonce):
  header_string = generate_header(index, prev_hash, data, timestamp, nonce)
  sha = hashlib.sha256()
  sha.update(header_string)
  return sha.hexdigest()

def check_for_broadcasted_blocks():
  '''
    We need a way to check to see if someone's claimed they solved a block
  '''
  print "checking for other node's blocks"
  print "no other blocks found"

def broadcast_mined_block(block):
  '''
    We want to hit the other peers saying that we mined a block
  '''
  block_info_dict = block.to_dict()
  for peer in PEERS:
    r = requests.post(peer+'/mined', json=block_info_dict)
  return True

def mine_blocks(last_block):
  index = int(last_block.index) + 1
  timestamp = date.datetime.now()
  data = "I block #%s" % (int(last_block.index) + 1) #random string for now, not transactions
  prev_hash = last_block.hash
  nonce = 0

  print "mining for block %s" % index
  block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)
  while str(block_hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
    nonce += 1
    block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)

  print "block %s mined. Nonce: %s" % (index, nonce)

  #dictionary to create the new block object.
  block_data = {}
  block_data['index'] = index
  block_data['prev_hash'] = last_block.hash
  block_data['timestamp'] = timestamp
  block_data['data'] = "Gimme %s dollars" % index
  block_data['hash'] = block_hash
  block_data['nonce'] = nonce

  new_block = Block(block_data)
  return new_block #we mined the block. We're going to want to save it

  #return True

if __name__ == '__main__':

  #from worker import conn


  run_mining_job = sched.add_job(run_mining, id='run_mining')
  check_for_broadcasted_blocks_job = sched.add_job(check_for_broadcasted_blocks, 'interval', seconds=3)

  run_mining()


  #sched.start()
