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

def mine_for_block(chain=None, rounds=STANDARD_ROUNDS, start_nonce=0, timestamp=None):
  if not chain:
    chain = sync.sync_local() #gather last node

  prev_block = chain.most_recent_block()
  return mine_from_prev_block(prev_block, rounds=rounds, start_nonce=start_nonce, timestamp=timestamp)

def mine_from_prev_block(prev_block, rounds=STANDARD_ROUNDS, start_nonce=0, timestamp=None):
  #create new block with correct
  new_block = utils.create_new_block_from_prev(prev_block=prev_block, timestamp=timestamp)
  return mine_block(new_block, rounds=rounds, start_nonce=start_nonce)

def mine_block(new_block, rounds=STANDARD_ROUNDS, start_nonce=0):
  print "Mining for block %s. start_nonce: %s, rounds: %s" % (new_block.index, start_nonce, rounds)
  #Attempting to find a valid nonce to match the required difficulty
  #of leading zeros. We're only going to try 1000
  nonce_range = [i+start_nonce for i in range(rounds)]
  for nonce in nonce_range:
    new_block.nonce = nonce
    new_block.update_self_hash()
    if str(new_block.hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS:
      print "block %s mined. Nonce: %s" % (new_block.index, new_block.nonce)
      assert new_block.is_valid()
      return new_block, rounds, start_nonce, new_block.timestamp

  #couldn't find a hash to work with, return rounds and start_nonce
  #as well so we can know what we tried
  return None, rounds, start_nonce, new_block.timestamp

def mine_for_block_listener(event):
  #need to check if the finishing job is the mining
  if event.job_id == 'mining':
    new_block, rounds, start_nonce, timestamp = event.retval
    #if didn't mine, new_block is None
    #we'd use rounds and start_nonce to know what the next
    #mining task should use
    if new_block:
      print "Mined a new block"
      new_block.self_save()
      broadcast_mined_block(new_block)
      sched.add_job(mine_from_prev_block, args=[new_block], kwargs={'rounds':STANDARD_ROUNDS, 'start_nonce':0}, id='mining') #add the block again
    else:
      print event.retval
      sched.add_job(mine_for_block, kwargs={'rounds':rounds, 'start_nonce':start_nonce+rounds, 'timestamp': timestamp}, id='mining') #add the block again
      sched.print_jobs()

def broadcast_mined_block(new_block):
  #  We want to hit the other peers saying that we mined a block
  block_info_dict = new_block.__dict__
  for peer in PEERS:
    endpoint = "%s%s" % (peer[0], peer[1])
    #see if we can broadcast it
    try:
      r = requests.post(peer+'mined', json=block_info_dict)
    except requests.exceptions.ConnectionError:
      print "Peer %s not connected" % peer
      continue
  return True

def validate_possible_block(possible_block_dict):

  possible_block = Block(possible_block_dict)
  if possible_block.is_valid():
    possible_block.self_save()

    #we want to kill and restart the mining block so it knows it lost
    sched.print_jobs()
    try:
      sched.remove_job('mining')
      print "removed running mine job in validating possible block"
    except apscheduler.jobstores.base.JobLookupError:
      print "mining job didn't exist when validating possible block"

    print "readding mine for block validating_possible_block"
    print sched
    print sched.get_jobs()
    sched.add_job(mine_for_block, kwargs={'rounds':STANDARD_ROUNDS, 'start_nonce':0}, id='mining') #add the block again
    print sched.get_jobs()

    return True
  return False


if __name__ == '__main__':

  sched.add_job(mine_for_block, kwargs={'rounds':STANDARD_ROUNDS, 'start_nonce':0}, id='mining') #add the block again
  sched.add_listener(mine_for_block_listener, apscheduler.events.EVENT_JOB_EXECUTED)
  sched.start()

