from block import Block
import mine
from flask import Flask, jsonify, request
import sync
import requests
import os
import json
import sys
import apscheduler
import argparse

import utils
from config import *

node = Flask(__name__)

sync.sync(save=True) #want to sync and save the overall "best" blockchain from peers

from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler(standalone=True)

@node.route('/blockchain.json', methods=['GET'])
def blockchain():
  '''
    Shoots back the blockchain, which in our case, is a json list of hashes
    with the block information which is:
    index
    timestamp
    data
    hash
    prev_hash
  '''
  local_chain = sync.sync_local() #update if they've changed
  # Convert our blocks into dictionaries
  # so we can send them as json objects later
  json_blocks = json.dumps(local_chain.block_list_dict())
  return json_blocks

@node.route('/mined', methods=['POST'])
def mined():
  possible_block_dict = request.get_json()
  print possible_block_dict
  print sched.get_jobs()
  print sched

  sched.add_job(mine.validate_possible_block, args=[possible_block_dict], id='validate_possible_block') #add the block again

  return jsonify(received=True)

if __name__ == '__main__':

  #args!
  parser = argparse.ArgumentParser(description='JBC Node')
  parser.add_argument('--port', '-p', default='5000',
                    help='what port we will run the node on')
  parser.add_argument('--mine', '-m', dest='mine', action='store_true')
  args = parser.parse_args()

  filename = '%sdata.txt' % (CHAINDATA_DIR)
  with open(filename, 'w') as data_file:
    data_file.write("Mined by node on port %s" % args.port)

  mine.sched = sched #to override the BlockingScheduler in the
  #only mine if we want to
  if args.mine:
    #in this case, sched is the background sched
    sched.add_job(mine.mine_for_block, kwargs={'rounds':STANDARD_ROUNDS, 'start_nonce':0}, id='mining') #add the block again
    sched.add_listener(mine.mine_for_block_listener, apscheduler.events.EVENT_JOB_EXECUTED)#, args=sched)

  sched.start() #want this to start so we can validate on the schedule and not rely on Flask

  #now we know what port to use
  node.run(host='127.0.0.1', port=args.port)

