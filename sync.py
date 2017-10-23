from block import Block
from config import *

import os
import json
import requests

def sync_local():
  node_blocks = []
  #We're assuming that the folder and at least initial block exists
  chaindata_dir = 'chaindata'
  if os.path.exists(chaindata_dir):
    for filename in os.listdir(chaindata_dir):
      if filename.endswith('.json'):
        filepath = '%s/%s' % (chaindata_dir, filename)
        with open(filepath, 'r') as block_file:
          block_info = json.load(block_file)
          block_object = Block(block_info)
          node_blocks.append(block_object)
  return node_blocks

def sync_overall():
  longest_blockchain = sync_local()
  for peer in PEERS:
    #try to connect to peer
    peer_blockchain_url = peer + 'blockchain.json'
    try:
      r = requests.get(peer_blockchain_url)
      blockchain = r.json()
      if len(blockchain) > len(longest_blockchain):
        longest_blockchain = blockchain
    except requests.exceptions.ConnectionError:
      print "Peer at %s not running. Continuing to next peer." % peer
  print "Longest blockchain is %s blocks" % len(longest_blockchain)
  #for now, save the new blockchain over whatever was there
  save_long_blockchain(longest_blockchain)
  return longest_blockchain

def save_long_blockchain(blockchain_data):
  '''
    Destroy the previous blockchian directory, and save each file
  '''
  for block_data in blockchain_data:
    block_data.self_save()

def sync():
  return sync_overall()
