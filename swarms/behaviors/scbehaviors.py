"""Defines all the composite behaviors for the agents.

This file name is scbehaviors coz `s` stands for swarms and
`c` stands for composite behaviors.
These composite behaviors are designed so that the algorithms
would find the collective behaviors with ease. Also it will help the
human designers to effectively design new behaviors. It provides
flexibility for the user to use the primitive behaviors along with
feature rich behaviors.
"""

from py_trees import Behaviour, Blackboard
from py_trees.composites import Sequence, Selector
from py_trees.trees import BehaviourTree
from swarms.behaviors.sbehaviors import (
    GoTo, Towards, Move, Away,
    IsCarryable, IsSingleCarry, SingleCarry,
    IsMultipleCarry, IsInPartialAttached, IsEnoughStrengthToCarry,
    InitiateMultipleCarry, IsCarrying, Drop, RandomWalk, DropPartial,
    SignalDoesNotExists, SendSignal, NeighbourObjects, ReceiveSignal,
    CueDoesNotExists, DropCue, PickCue
    )

# Start of mid-level behaviors. These behaviors are the
# combination of primitive behaviors. There are behaviors which can
# make use of mid-level behavior to form highlevel behaviors.

# Every direction chaning command needs to follow move. So we will combine
# them into a single behaviors with sequence and call it MoveTowards


class MoveTowards(Behaviour):
    """MoveTowards behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors GoTo, Towards and Move. This
    allows agents actually to move towards the object of interest.
    """

    def __init__(self, name):
        """Init method for the MoveTowards behavior."""
        super(MoveTowards, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item
        # Define goto primitive behavior
        goto = GoTo('MT_GOTO_1')
        goto.setup(0, self.agent, self.item)

        # Define towards behavior
        towards = Towards('MT_TOWARDS_2')
        towards.setup(0, self.agent)

        # Define move behavior
        move = Move('MT_MOVE_3')
        move.setup(0, self.agent)

        # Define a sequence to combine the primitive behavior
        mt_sequence = Sequence('MT_SEQUENCE')
        mt_sequence.add_children([goto, towards, move])

        self.behaviour_tree = BehaviourTree(mt_sequence)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


class MoveAway(Behaviour):
    """MoveAway behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors GoTo, Away and Move. This
    allows agents actually to move away the object of interest.
    """

    def __init__(self, name):
        """Init method for the MoveAway behavior."""
        super(MoveAway, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item
        # Define goto primitive behavior
        goto = GoTo('MA_GOTO_1')
        goto.setup(0, self.agent, self.item)

        # Define away behavior
        away = Away('MA_Away_2')
        away.setup(0, self.agent)

        # Define move behavior
        move = Move('MA_MOVE_3')
        move.setup(0, self.agent)

        # Define a sequence to combine the primitive behavior
        mt_sequence = Sequence('MA_SEQUENCE')
        mt_sequence.add_children([goto, away, move])

        self.behaviour_tree = BehaviourTree(mt_sequence)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


class CompositeSingleCarry(Behaviour):
    """CompositeSingleCarry behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors to succesfully carry any
    carryable object. It combines IsCarrable, IsSingleCarry and SingleCarry
    primitive behaviors.
    """

    def __init__(self, name):
        """Init method for the CompositeSingleCarry behavior."""
        super(CompositeSingleCarry, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item

        # First check if the item is carrable?
        carryable = IsCarryable('SC_IsCarryable_1')
        carryable.setup(0, self.agent, self.item)

        # Then check if the item can be carried by a single agent
        issinglecarry = IsSingleCarry('SC_IsSingleCarry_2')
        issinglecarry.setup(0, self.agent, self.item)

        # Finally, carry the object
        singlecarry = SingleCarry('SC_SingleCarry_3')
        singlecarry.setup(0, self.agent, self.item)

        # Define a sequence to combine the primitive behavior
        sc_sequence = Sequence('SC_SEQUENCE')
        sc_sequence.add_children([carryable, issinglecarry, singlecarry])

        self.behaviour_tree = BehaviourTree(sc_sequence)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


class CompositeMultipleCarry(Behaviour):
    """CompositeMultipleCarry behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors to succesfully carry any heavy
    carryable object. It combines IsCarrable, IsMultipleCarry
    and InitiateMultipleCarry primitive behaviors.
    """

    def __init__(self, name):
        """Init method for the CompositeSingleCarry behavior."""
        super(CompositeMultipleCarry, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item

        # Root node from the multiple carry behavior tree
        root = Sequence("MC_Sequence")

        # Conditional behavior to check if the sensed object is carrable or not
        carryable = IsCarryable('MC_IsCarryable')
        carryable.setup(0, self.agent, self.item)

        # Conditional behavior to check if the object is too heavy
        # for single carry
        is_mc = IsMultipleCarry('MC_IsMultipleCarry')
        is_mc.setup(0, self.agent, self.item)

        # Check if the object is alread attached to the object
        partial_attached = IsInPartialAttached('MC_IsPartialAttached')
        partial_attached.setup(0, self.agent, self.item)

        # Initiate multiple carry process
        initiate_mc_b = InitiateMultipleCarry('MC_InitiateMultipleCarry')
        initiate_mc_b.setup(0, self.agent, self.item)

        # Selector to select between intiate
        # multiple carry and checking strength
        initial_mc_sel = Selector("MC_Selector")
        initial_mc_sel.add_children([partial_attached, initiate_mc_b])

        strength = IsEnoughStrengthToCarry('MC_EnoughStrength')
        strength.setup(0, self.agent, self.item)

        strength_seq = Sequence("MC_StrenghtSeq")

        strength_seq.add_children([strength])

        # Main sequence branch where all the multiple carry logic takes place
        sequence_branch = Sequence("MC_Sequence_branch")
        sequence_branch.add_children([is_mc, initial_mc_sel, strength_seq])

        # Main logic behind this composite multiple carry BT
        """
        First check if the object is carryable or not. If the object is
        carryable then execute the sequence branch. In the sequence branch,
        check is the object needs multiple agents to carry. If yes, execute
        the initiate multiple carry sequence branch only if it has not been
        attached before. Finally, check if there are enought agents/strenght
        to lift the object up.
        """
        root.add_children([carryable, sequence_branch])
        self.behaviour_tree = BehaviourTree(root)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


class CompositeDrop(Behaviour):
    """CompositeDrop behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors to succesfully drop any
    carrying object fon to a dropable surface. It combines IsDropable,
    IsCarrying and Drop primitive behaviors.
    """

    def __init__(self, name):
        """Init method for the CompositeDrop behavior."""
        super(CompositeDrop, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item

        dropseq = Sequence('CD_Sequence')

        iscarrying = IsCarrying('CD_IsCarrying')
        iscarrying.setup(0, self.agent, self.item)

        drop = Drop('CD_Drop')
        drop.setup(0, self.agent, self.item)

        dropseq.add_children([iscarrying, drop])

        self.behaviour_tree = BehaviourTree(dropseq)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


class CompositeDropPartial(Behaviour):
    """CompositeDropPartial behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors to succesfully drop any
    objects carried with cooperation to a dropable surface. It
    combines IsDropable, IsCarrying and DropPartial primitive behaviors.
    """

    def __init__(self, name):
        """Init method for the CompositeDrop behavior."""
        super(CompositeDropPartial, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item

        dropseq = Sequence('CDP_Sequence')

        iscarrying = IsInPartialAttached('CDP_IsInPartial')
        iscarrying.setup(0, self.agent, self.item)

        drop = DropPartial('CDP_DropPartial')
        drop.setup(0, self.agent, self.item)

        dropseq.add_children([iscarrying, drop])

        self.behaviour_tree = BehaviourTree(dropseq)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


class Explore(Behaviour):
    """Explore behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors to succesfully explore the
    environment. It combines Randomwalk and Move behaviors.
    """

    def __init__(self, name):
        """Init method for the Explore behavior."""
        super(Explore, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item=None):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item

        # Define the root for the BT
        root = Sequence("Ex_Sequence")

        low = RandomWalk('Ex_RandomWalk')
        low.setup(0, self.agent)

        high = Move('Ex_Move')
        high.setup(0, self.agent)

        root.add_children([low, high])

        self.behaviour_tree = BehaviourTree(root)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


# Communication composite behaviors
class CompositeSendSignal(Behaviour):
    """Send signal behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors to succesfully send signals
    in the environment. It combines SignalDoesNotExists and SendSignal
    behaviors.
    """

    def __init__(self, name):
        """Init method for the SendSignal behavior."""
        super(CompositeSendSignal, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item=None):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item

        # Define the root for the BT
        root = Sequence('CSS_Sequence')

        s1 = SignalDoesNotExists('CSS_SignalDoesNotExists')
        s1.setup(0, self.agent, self.item)

        s2 = SendSignal('CSS_SendSignal')
        s2.setup(0, self.agent, self.item)

        root.add_children([s1, s2])

        self.behaviour_tree = BehaviourTree(root)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


class CompositeReceiveSignal(Behaviour):
    """Receive signal behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors to succesfully receive signals
    in the environment. It combines Neighbour and ReceiveSignal behaviors.
    """

    def __init__(self, name):
        """Init method for the SendSignal behavior."""
        super(CompositeReceiveSignal, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item=None):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item

        # Define the root for the BT
        root = Sequence('CRS_Sequence')

        s1 = NeighbourObjects('CRS_NeighbourObjects')
        s1.setup(0, self.agent, 'Signal')

        s2 = ReceiveSignal('CRS_ReceiveSignal')
        s2.setup(0, self.agent, 'Signal')

        root.add_children([s1, s2])

        self.behaviour_tree = BehaviourTree(root)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


class CompositeDropCue(Behaviour):
    """Drop cue behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors to succesfully drop cue
    in the environment. It combines CueDoesNotExists and DropCue behaviors.
    """

    def __init__(self, name):
        """Init method for the SendSignal behavior."""
        super(CompositeDropCue, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item=None):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item

        # Define the root for the BT
        root = Sequence('CDC_Sequence')

        c1 = CueDoesNotExists('CDC_CueDoesNotExists')
        c1.setup(0, self.agent, self.item)

        c2 = DropCue('CDC_DropCue')
        c2.setup(0, self.agent, self.item)

        root.add_children([c1, c2])

        self.behaviour_tree = BehaviourTree(root)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status


class CompositePickCue(Behaviour):
    """Pick cue behavior for the agents.

    Inherits the Behaviors class from py_trees. This
    behavior combines the privitive behaviors to succesfully pick cue
    from the environment. It combines NeighbourObjects and PickCue behaviors.
    """

    def __init__(self, name):
        """Init method for the SendSignal behavior."""
        super(CompositePickCue, self).__init__(name)
        self.blackboard = Blackboard()
        self.blackboard.shared_content = dict()

    def setup(self, timeout, agent, item=None):
        """Have defined the setup method.

        This method defines the other objects required for the
        behavior. Agent is the actor in the environment,
        item is the name of the item we are trying to find in the
        environment and timeout defines the execution time for the
        behavior.
        """
        self.agent = agent
        self.item = item

        # Define the root for the BT
        root = Sequence('CPC_Sequence')

        c1 = NeighbourObjects('CPS_SearchCue')
        c1.setup(0, self.agent, 'Cue')

        c2 = PickCue('CPS_PickCue')
        c2.setup(0, self.agent, 'Cue')

        root.add_children([c1, c2])

        self.behaviour_tree = BehaviourTree(root)

    def initialise(self):
        """Everytime initialization. Not required for now."""
        pass

    def update(self):
        """Just call the tick method for the sequence.

        This will execute the primitive behaviors defined in the sequence
        """
        self.behaviour_tree.tick()
        return self.behaviour_tree.root.status
