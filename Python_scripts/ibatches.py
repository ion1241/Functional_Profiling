# A very useful function. There's nothing quite like this in itertools
# written by Tim Booth https://gist.github.com/tbooth/7b762b7a345983dceff160954ecd4845
# If performance is critical there will be more efficient ways to loop through
# the list without copying it, but this robust and in most cases fast enough.

def ibatches(iter_in, batch_size, include_stub=True, slide=0):
    """
    Given a list (or indeed any iterable), split the list into batches
    If the last batch is too small, we can decide whether to yield this remaining stub.
    slide=0 means produce discrete chunks, slide>=1 gives you a sliding window.
    """    
    if slide == 0 or slide > batch_size:
        slide = batch_size
        
    this_batch = [] # accumulator for sub-lists
    stub = False    # is there a stub to return?
    for i in iter_in:
        this_batch.append(i)
        stub = True
        if len(this_batch) == batch_size:
            yield this_batch
            stub = False
            # I considered using a deque but we need to copy the list anyway
            this_batch = this_batch[slide:]
    if stub and include_stub:
        yield this_batch
        
def batches(*args, **kwargs):
    """Gather ibatches() results in an actual list.
    """
    return list(ibatches(*args, **kwargs))
        
# Look it works! Note that these assertions would normally go into a separate unit test file.
# See https://docs.python.org/3/library/unittest.html for details.
assert batches([],  1) == []

assert batches("ABCDEF",  3, include_stub=True ) == [['A','B','C'],['D','E','F']]
assert batches("ABCDEF",  3, include_stub=False) == [['A','B','C'],['D','E','F']]
assert batches("ABCDEFG", 3, include_stub=True ) == [['A','B','C'],['D','E','F'],['G']]
assert batches("ABCDEFG", 3, include_stub=False) == [['A','B','C'],['D','E','F']]
assert batches(range(3),  1, include_stub=True ) == [[0],[1],[2]]
assert batches(range(3),  1, include_stub=False) == [[0],[1],[2]]

assert batches("ABCDE",  3, include_stub=True,  slide=1) == [['A','B','C'],['B','C','D'],['C','D','E']]
assert batches("ABCDE",  3, include_stub=False, slide=1) == [['A','B','C'],['B','C','D'],['C','D','E']]
assert batches("ABC",    4, include_stub=True,  slide=1) == [['A','B','C']]
assert batches("ABC",    4, include_stub=False, slide=1) == []
assert batches(range(3), 1, include_stub=True,  slide=1) == [[0],[1],[2]]
assert batches(range(3), 1, include_stub=False, slide=1) == [[0],[1],[2]]

assert batches("ABCDE",  4, include_stub=True,  slide=3) == [['A','B','C','D'],['D','E']]
assert batches("ABCDE",  4, include_stub=False, slide=3) == [['A','B','C','D']]