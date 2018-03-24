# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """

        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.qvalues = {}

        qvalues_temp = []

        states = mdp.getStates()

        for k in range(0, self.iterations):
            maxVal = {}

            for state in states:

                if mdp.isTerminal(state):
                    maxVal[state]=0
                    self.qvalues[state] = 0
                    continue
                else:
                    actions = mdp.getPossibleActions(state)
                    for action in actions:
                        qValue = self.getQValue(state, action)
                        qvalues_temp.append(qValue)
                    self.qvalues[state] = list(qvalues_temp)
                    maxVal[state] = max(self.qvalues[state])
                    qvalues_temp[:] = []

            #need to wait to update self.values until after each iteration or else you propogate values too soon.
            self.values=maxVal.copy()


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #
        chance_list = self.mdp.getTransitionStatesAndProbs(state, action)
        sum = 0
        for chance in chance_list:
            s_prime = chance[0]
            prob = chance[1]
            s_prime_value = float(self.values[s_prime])
            reward = self.mdp.getReward(state, action, s_prime)
            v_star = self.discount*s_prime_value
            chance_value = prob*(reward + v_star)
            sum+=chance_value

        return sum


        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.iterations == 0:
            return None

        #when state is terminal
        if self.mdp.isTerminal(state):
            return None

        #when only action is exit
        if len(self.qvalues[state]) == 1:
            return self.mdp.getPossibleActions(state)[0]

        #find max qvalue and return the action for it
        #plus a stupid hack for getting action variable
        highest_value = max(self.qvalues[state])
        index = self.qvalues[state].index(highest_value)
        if index == 0:
            return self.mdp.getPossibleActions(self.mdp.getStartState())[0]
        if index == 1:
            return self.mdp.getPossibleActions(self.mdp.getStartState())[1]
        if index == 2:
            return self.mdp.getPossibleActions(self.mdp.getStartState())[2]
        if index == 3:
            return self.mdp.getPossibleActions(self.mdp.getStartState())[3]

        return


        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
