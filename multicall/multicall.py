from typing import List


from multicall import Call
from multicall.constants import MULTICALL_ADDRESSES


class Multicall:
    def __init__(self, calls: List[Call], _w3=None, block_id=None, chain_id=None):
        self.calls = calls
        self.block_id = block_id
        if _w3 is None:
            self.w3 = None
        else:
            self.w3 = _w3
        self.chainId = chain_id

    def __call__(self):
        aggregate = Call(
            MULTICALL_ADDRESSES[self.chainId],
            'aggregate((address,bytes)[])(uint256,bytes[])',
            returns=None,
            _w3=self.w3,
            block_id=self.block_id
        )
        args = [[[call.target, call.data] for call in self.calls]]
        block, outputs = aggregate(args)
        result = []
        for call, output in zip(self.calls, outputs):
            result.append(call.decode_output(output))
        return result
