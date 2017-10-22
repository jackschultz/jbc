from block import Block
from flask import Flask, jsonify
from celery import Celery
import sync

import os
import json

node = Flask(__name__)
node.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
node.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(node.name, broker=node.config['CELERY_BROKER_URL'])
celery.conf.update(node.config)

node_blocks = sync.sync()

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
  node_blocks = sync.sync() #update if they've changed
  # Convert our blocks into dictionaries
  # so we can send them as json objects later
  python_blocks = []
  for block in node_blocks:
    python_blocks.append(block.__dict__())
  json_blocks = json.dumps(python_blocks)
  return json_blocks

@node.route('/mined', methods=['POST'])
def mined():
  possible_block_data = request.get_json()
  #validate possible_block
  possible_block = Block(possible_block_data)
  if possible_block.is_valid():
    #save to file to possible folder
    pass
    return jsonify(confirmed=True)
  else:
    #ditch it
    return jsonify(confirmed=False)

if __name__ == '__main__':
  node.run()
