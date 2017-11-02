import os
from config import *
import utils
import sync
import argparse

def mine_first_block():
  first_block = utils.create_new_block_from_prev(prev_block=None, data='First block.')
  first_block.update_self_hash()#calculate_hash(index, prev_hash, data, timestamp, nonce)
  while str(first_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
    first_block.nonce += 1
    first_block.update_self_hash()
  assert first_block.is_valid()
  return first_block

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Generating Blockchain')
  parser.add_argument('--first', '-f', dest='first', default=False, action='store_true', help='generate the first node ourselves')
  parser.add_argument('--port', '-p', default='5000',
                    help='what port we will run the node on')
  args = parser.parse_args()

  #check if dir is empty from just creation, or empty before
  if not os.path.exists(CHAINDATA_DIR):
    os.mkdir(CHAINDATA_DIR)

  if args.first: #if we want to mine the first block on our own
    #need to check to see if there are any blocks in this
    if os.listdir(CHAINDATA_DIR) == []:
      #create the first block
      first_block = mine_first_block()
      first_block.self_save()
      #need a data.txt to tell which port we're running on
      filename = "%s/data.txt" % CHAINDATA_DIR
      with open(filename, 'w') as data_file:
        data_file.write('Block mined by node on port %s' % args.port)
    else:
      print "Chaindata directory already has files. If you want to generate a first block, delete files and rerun"
  else:
    #this is the normal part, syncing from peers
    sync.sync(save=True)

