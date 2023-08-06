# -*- coding: utf-8 -*-
'''
RandomAgent class
=================

An agent that randomly chooses an action
'''

import random
from typing import Any, Optional, Tuple

from reil.agents.no_learn_agent import NoLearnAgent
from reil.datatypes.feature import FeatureArray


class RandomAgent(NoLearnAgent):
    '''
    An agent that acts randomly.
    '''

    def __init__(self,
                 default_actions: Tuple[FeatureArray, ...] = (),
                 **kwargs: Any):
        super().__init__(default_actions=default_actions, **kwargs)

    def act(self,
            state: FeatureArray,
            subject_id: int,
            actions: Optional[Tuple[FeatureArray, ...]] = None,
            iteration: int = 0) -> FeatureArray:
        '''
        Return a random action.

        Arguments
        ---------
        state:
            The state for which the action should be returned.

        actions:
            The set of possible actions to choose from.

        iteration:
            The iteration in which the agent is acting.

        Returns
        -------
        :
            The action
        '''
        return random.choice(actions or self._default_actions)
