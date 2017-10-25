from block import Block
from config import *
from utils import is_valid_chain

import os
import json
import requests
import glob

def sync_local():
  node_blocks = []
  #We're assuming that the folder and at least initial block exists
  if os.path.exists(CHAINDATA_DIR):
    for filepath in glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
      with open(filepath, 'r') as block_file:
        try:
          block_info = json.load(block_file)
        except:
          print filepath
          import pdb;pdb.set_trace()
          asdf = 4
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
      if len(blockchain) > len(longest_blockchain) and blockchain.is_valid_chain():
        longest_blockchain = [Block(bc) for bc in blockchain]
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
