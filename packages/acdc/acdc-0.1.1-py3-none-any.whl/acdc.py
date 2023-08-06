import array
from collections import namedtuple


IState = namedtuple(
    'IState',
    ('uid', 'parent', 'byte', 'transitions', 'longest_strict_suffix', 'match')
)

def make_state_factory():
    UID = 0
    def make_state(parent, byte):
        nonlocal UID
        uid = UID
        UID += 1
        return IState(uid, parent, byte, {}, [None], [None])
    return make_state


def make(iterable):
    make_state = make_state_factory()

    # first step: basic state machine...
    zero = make_state(None, None)
    states = [zero]
    for item in iterable:
        current = zero
        bytes = item.encode('utf8')
        for byte in bytes:
            try:
                candidate = current.transitions[byte]
            except KeyError:
                next = make_state(current, byte)
                states.append(next)
                current.transitions[byte] = next
                current = next
            else:
                current = candidate
        current.match[0] = item

    # second step: finalize state machine...
    zero.longest_strict_suffix[0] = zero

    for state in states:
        for child in state.transitions.values():
            _finalize(zero, child)

    # last step: freeze!
    out = []
    for istate in states:
        transitions = [None] * 255
        for byte, state in istate.transitions.items():
            transitions[byte] = state.uid
        fstate = FState(
            istate.byte,
            istate.match[0],
            istate.longest_strict_suffix[0].uid,
            tuple(transitions)
        )
        out.append(fstate)
    return tuple(out)


def _finalize(zero, state):
    traversed = state.parent.longest_strict_suffix[0]
    while True:
        if traversed is zero:
            state.longest_strict_suffix[0] = suffix = zero
            break
        try:
            suffix = traversed.transitions[state.byte]

        except KeyError:
            pass
        else:
            if suffix is not state:
                state.longest_strict_suffix[0] = suffix
                break

        traversed = traversed.longest_strict_suffix[0]

    if suffix is zero:
        return

    for byte, next in suffix.transitions.items():
        try:
            state.transitions[byte]
        except KeyError:
            state.transitions[byte] = next


FState = namedtuple('FState', ('byte', 'match', 'longest_strict_suffix', 'transitions'))


def search(machine, iterable):
    current = zero = machine[0]
    for byte in iterable:
        index = current.transitions[byte] or zero.transitions[byte] or 0
        current = state = machine[index]
        while state is not zero:
            if state.match:
                yield state.match
            state = machine[state.longest_strict_suffix]
