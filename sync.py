from chain import Chain
from config import *
from block import Block

import os
import json
import requests
import glob

def sync_local():
  blocks = []
  #We're assuming that the folder and at least initial block exists
  if os.path.exists(CHAINDATA_DIR):
    for filepath in glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
      with open(filepath, 'r') as block_file:
        try:
          block_info = json.load(block_file)
        except:
          print filepath
        local_block = Block(block_info)
        blocks.append(local_block)
  blocks.sort(key=lambda block: block.index)
  local_chain = Chain(blocks)
  return local_chain

def sync_overall(save=False):
  best_chain = sync_local()
  for peer in PEERS:
    #try to connect to peer
    peer_blockchain_url = peer + 'blockchain.json'
    try:
      r = requests.get(peer_blockchain_url)
      peer_blockchain_dict = r.json()
      peer_blocks = [Block(bdict) for bdict in peer_blockchain_dict]
      peer_chain = Chain(peer_blocks)

      print peer_chain.is_valid()
      if peer_chain.is_valid() and len(peer_chain) > len(best_chain):
        best_chain = peer_chain

    except requests.exceptions.ConnectionError:
      print "Peer at %s not running. Continuing to next peer." % peer
    else:
      print "Peer at %s is running. Gathered their blochchain for analysis." % peer
  print "Longest blockchain is %s blocks" % len(best_chain)
  #for now, save the new blockchain over whatever was there
  if save:
    best_chain.self_save()
  return best_chain

def sync(save=False):
  return sync_overall(save=save)

