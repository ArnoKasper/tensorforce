# Copyright 2016 reinforce.io. All Rights Reserved.
# ==============================================================================

"""
Comment
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from collections import deque

import numpy as np

from tensorforce.preprocessing import Preprocessor


class Concat(Preprocessor):

    default_config = {
        'concat_length': 1,
        'dimension_position': 'prepend'
    }

    config_args = [
        'concat_length',
        'dimension_position'
    ]

    def __init__(self, config, *args, **kwargs):
        super(Concat, self).__init__(config, *args, **kwargs)

        self._queue = deque(maxlen=self.config.concat_length)

    def process(self, state):
        """
        Return full concatenated state including new state state.

        :param state: New state to be added
        :return: State tensor of shape (concat_length, state_shape)
        """
        self._queue.append(state)

        # If queue is too short, fill with current state.
        while len(self._queue) < self.config.concat_length:
            self._queue.append(state)

        if self.config.dimension_position == 'append':
            concatted = np.array(self._queue)
            return np.moveaxis(concatted, 0, -1)
        else:
            return np.array(self._queue)

    def shape(self, original_shape):
        if self.config.dimension_position == 'append':
            return list(original_shape) + [self.config.concat_length]
        else:
            return [self.config.concat_length] + list(original_shape)