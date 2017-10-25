
def is_valid_chain():
  '''
    We need to check to see if the entire chain is valid.
    To do this, we check if each block in order is valid.
    The is_valid() function in the Block class handles the
    hash connection between the previous and current block.
  '''
  for b in blockchain:
    if not b.is_valid():
      return False
  return True

