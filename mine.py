import datetime
import time
import sync
import json
import hashlib
import requests
import os
import glob

from block import Block
from config import *
import utils

import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler

#if we're running mine.py, we don't want it in the background
#because the script would return after starting. So we want the
#BlockingScheduler to run the code.
sched = BlockingScheduler(standalone=True)
print sched

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def mine_for_block():
  print "mine for block sync"
  current_chain = sync.sync_local() #gather last node
  print "mine for block sync done"
  prev_block = current_chain.most_recent_block()
  new_block = mine_blocks(prev_block)
  new_block.self_save()

  #tell the world that you won!
  broadcast_mined_block(new_block)

  return new_block

def mine_blocks(last_block):
  index = int(last_block.index) + 1
  timestamp  = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
  data = "I block #%s." % (int(last_block.index) + 1) #random string for now, not transactions
  prev_hash = last_block.hash
  nonce = 0

  block_info_dict = utils.dict_from_block_attributes(index=index, timestamp=timestamp, data=data, prev_hash=prev_hash, nonce=nonce)
  print "ASDFASDFASDFASDFASDF"
  print block_info_dict
  new_block = Block(block_info_dict)
  return find_valid_nonce(new_block)

def find_valid_nonce(new_block):
  print "mining for block %s" % new_block.index
  new_block.update_self_hash()#calculate_hash(index, prev_hash, data, timestamp, nonce)
  while str(new_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
    new_block.nonce += 1
    new_block.update_self_hash()

  print "block %s mined. Nonce: %s" % (new_block.index, new_block.nonce)

  assert new_block.is_valid()
  return new_block #we mined the block. We're going to want to save it

def validate_possible_block(sched, possible_block_dir):
  possible_block = Block(possible_block_dir)
  if possible_block.is_valid():
    #check to see if the schedule is running a mine_for_block job
    sched.print_jobs()
    try:
      sched.remove_job('mine_for_block')
      print "removed running mine job in validating possible block"
    except apscheduler.jobstores.base.JobLookupError:
      print "mining job didn't exist when validating possible block"

    print "saving valid block validating possible block"
    possible_block.self_save()
    #now we want to kill and restart the mining block so it knows it lost

    print "readding mine for block validating_possible_block"
    print sched
    print sched.get_jobs()
    sched.add_job(mine_for_block, id='mine_for_block')
    print sched.get_jobs()

    return True

def broadcast_mined_block(new_block):
  '''
    We want to hit the other peers saying that we mined a block
  '''
  block_info_dict = new_block.to_dict()
  for peer in PEERS:
    endpoint = "%s%s" % (peer[0], peer[1])
    #see if we can broadcast it
    try:
      r = requests.post(peer+'mined', json=block_info_dict)
    except requests.exceptions.ConnectionError:
      print "Peer %s not connected" % peer
      continue
  return True

def mine_for_block_listener(event):
  print "I was listening and we mined a block"
  print sched
  print sched.get_jobs()
  sched.add_job(mine_for_block, id='mine_for_block') #add the block again
  print sched.get_jobs()

if __name__ == '__main__':

  sched.add_job(mine_for_block, id='mine_for_block') #add the block again
  sched.add_listener(mine_for_block_listener, apscheduler.events.EVENT_JOB_EXECUTED, args=sched)
  sched.start()

