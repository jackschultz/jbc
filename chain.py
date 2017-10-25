from block import Block

class Chain(object):

  def __init__(self, blocks=[]):
    self.blocks = blocks

  def is_valid(self):
    '''
      Is a valid blockchain if
      1) Each block is indexed one after the other
      2) Each block's prev hash is the hash of the prev block
      3) The block's hash is valid for the number of zeros
    '''
    for index, cur_block in enumerate(self.blocks[1:]):
      prev_block = self.blocks[index]
      if prev_block.index+1 != cur_block.index:
        return False
      if not cur_block.is_valid(): #checks the hash
        return False
      if prev_block.hash != cur_block.prev_hash:
        return False
    return True

  def __len__(self):
    return len(self.blocks)

  def __eq__(self, other):
    if len(self) != len(other):
      return False
    for sasdf, oasdf in zip(self.blocks, other.blocks):
      if sasdf != oasdf:
        return False
    return True

  def __ne__(self, other):
    return not self.__eq__(other)

  def max_index(self):
    pass

  def add_block(self, new_block):
    '''
      Put the new block into the index that the block is asking.
      That is, if the index is of one that currently exists, the new block
      would take it's place. Then we want to see if that block is valid.
      If it isn't, then we ditch the new block and return False.
    '''
    '''
      When we add a block, we want to find the block with the same index,
      remove the current block and the rest of the blocks with higher index,
      and
    '''
    if new_block.index > len(self):
      pass

    self.blocks.append(new_block)

    return True
