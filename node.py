from block import Block
from flask import Flask, jsonify, request
import sync
import requests
import os
import json
import sys

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
  local_chain = sync.sync_local() #update if they've changed
  # Convert our blocks into dictionaries
  # so we can send them as json objects later
  json_blocks = json.dumps(local_chain.block_list_dict())
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

  if len(sys.argv) >= 2:
    port = sys.argv[1]
  else:
    port = 5000

  node.run(host='127.0.0.1', port=port)
