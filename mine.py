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

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

STANDARD_ROUNDS = 100000

def mine_for_block(chain=None, rounds=STANDARD_ROUNDS, start_nonce=0):
  if not chain:
    chain = sync.sync_local() #gather last node

  print rounds
  print start_nonce
  prev_block = chain.most_recent_block()
  return mine_from_prev_block(prev_block, rounds=rounds, start_nonce=start_nonce)

def mine_from_prev_block(prev_block, rounds=STANDARD_ROUNDS, start_nonce=0):
  #create new block with correct
  new_block = utils.create_new_block_from_prev(prev_block=prev_block)
  return mine_block(new_block, rounds=rounds, start_nonce=start_nonce)

def mine_block(new_block, rounds=STANDARD_ROUNDS, start_nonce=0):
  #Attempting to find a valid nonce to match the required difficulty
  #of leading zeros. We're only going to try 1000
  nonce_range = [i+start_nonce for i in range(rounds)]
  for nonce in nonce_range:
    new_block.nonce = nonce
    new_block.update_self_hash()
    if str(new_block.hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS:
      print "block %s mined. Nonce: %s" % (new_block.index, new_block.nonce)
      assert new_block.is_valid()
      return new_block, rounds, start_nonce

  #couldn't find a hash to work with, return rounds and start_nonce
  #as well so we can know what we tried
  return None, rounds, start_nonce

def mine_for_block_listener(event):
  new_block, rounds, start_nonce = event.retval
  #if didn't mine, new_block is None
  #we'd use rounds and start_nonce to know what the next
  #mining task should use
  if new_block:
    print "Mined a new block"
    new_block.self_save()
    sched.add_job(mine_from_prev_block, args=[new_block], kwargs={'rounds':STANDARD_ROUNDS, 'start_nonce':0}, id='mine_for_block') #add the block again
  else:
    #tell the world that you won!
    #broadcast_mined_block(new_block)
    print event.retval
    sched.add_job(mine_for_block, kwargs={'rounds':rounds, 'start_nonce':start_nonce+rounds}, id='mine_for_block') #add the block again
    sched.print_jobs()

if __name__ == '__main__':

  sched.add_job(mine_for_block, kwargs={'rounds':STANDARD_ROUNDS, 'start_nonce':0}, id='mine_for_block') #add the block again
  sched.add_listener(mine_for_block_listener, apscheduler.events.EVENT_JOB_EXECUTED)#, args=sched)
  sched.start()



