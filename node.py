from block import Block
import mine
from flask import Flask, jsonify, request
import sync
import requests
import os
import json
import sys
import apscheduler

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
  valid = mine.validate_possible_block(sched, possible_block_dict)
  print valid
  return jsonify(confirmed=valid)

if __name__ == '__main__':

  if len(sys.argv) >= 2:
    port = sys.argv[1]
  else:
    port = 5000

  mine.sched = sched #to override the BlockingScheduler in the
  #in this case, sched is the background sched
  job = sched.add_job(mine.mine_for_block, id='mine_for_block')
  sched.add_listener(mine.mine_for_block_listener, apscheduler.events.EVENT_JOB_EXECUTED)
  sched.start()

  import time
  time.sleep(2)
  job.pause()
  time.sleep(3)
  job.resume()

  node.run(host='127.0.0.1', port=port)

