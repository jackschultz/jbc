from block import Block
from flask import Flask, jsonify, request
import sync
import requests
import os
import json

from config import *

node = Flask(__name__)

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
  print possible_block_data
  #validate possible_block
  possible_block = Block(possible_block_data)
  if possible_block.is_valid():
    #save to file to possible folder
    index = possible_block.index
    nonce = possible_block.nonce
    filename = BROADCASTED_BLOCK_DIR + '%s_%s.json' % (index, nonce)
    with open(filename, 'w') as block_file:
      json.dump(possible_block.to_dict(), block_file)
    return jsonify(confirmed=True)
  else:
    #ditch it
    return jsonify(confirmed=False)

if __name__ == '__main__':
  node.run()
