from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    if rules == ():
      return [hypothesis]    
    orNode = OR(hypothesis)    
    for rule in rules:      
      consequent = rule.consequent()[0]
      matchResult = match(consequent, hypothesis)
      if matchResult != None:        
        leafNode = ()
        antecedent = rule.antecedent
        if isinstance(antecedent, AND):          
          leafNode = AND()
          for exp in antecedent:
            currentHypothesis = populate(exp, matchResult)
            leafNode.append(simplify(backchain_to_goal_tree(rules, currentHypothesis)))
          orNode.append(leafNode)
        elif isinstance(antecedent, OR):
          leafNode = OR()
          for exp in antecedent:
            currentHypothesis = populate(exp, matchResult)
            leafNode.append(simplify(backchain_to_goal_tree(rules, currentHypothesis)))
          orNode.append(leafNode)
        else:
          exp = antecedent
          currentHypothesis = populate(exp, matchResult)
          orNode.append(simplify(backchain_to_goal_tree(rules, currentHypothesis)))                
    return simplify(orNode)
# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
