from itertools import accumulate


class State:
    def __init__(self, left=None, right=None, suffix_link=None):
        self.left = left
        self.right = right
        self.suffix_link = suffix_link
        self.transition = {}


class STree:
    def __init__(self):
        self.string = ""
        self.end_idxes = []
        self.auxiliary = State()  # the auxiliary state ⊥
        self.root = State(-1, -1, self.auxiliary)

    def build(self, string, end_idxes=None):
        self.string = string
        self.end_idxes = end_idxes if end_idxes else []
        self.auxiliary = State()  # the auxiliary state ⊥
        self.root = State(-1, -1, self.auxiliary)
        for char in self.string:
            self.auxiliary.transition[char] = self.root
        active_state = self.root
        left = 0
        for idx in range(len(self.string)):
            active_state, left = self._update(active_state, left, idx)
            active_state, left = self._canonize(active_state, left, idx)
        if self.end_idxes:
            self.root.transition['end{}'.format(self.end_idxes[-1])] = State(self.end_idxes[-1], float("inf"))

    def build_with_automatic_end(self, strings):
        string = '$'.join(strings) + '$'
        end_idxes = list(accumulate(strings, lambda x, y: x + len(y) + 1, initial=-1))[1:]
        self.build(string, end_idxes)

    # 打印后缀树
    def __repr__(self):
        def state_desc(state: State):
            if state.left is None: return "⊥"
            if state.left == -1: return self.string
            return (self.string[state.left:] if state.right == float('inf') else self.string[state.left:state.right + 1]) + (" (end)" if state.right == float("inf") else "")

        def suffix_link_desc(state: State, prefix=""):
            return prefix + state_desc(state.suffix_link) if state.suffix_link else ""

        def recur(state: State, level, res):
            res += state_desc(state) + suffix_link_desc(state, prefix=" ----> ") + "\n"
            for next_state in state.transition.values():
                res += "\t" * level
                res += recur(next_state, level + 1, "")
            return res

        return recur(self.root, 0, "")

    def _update(self, active_state, left, idx):
        old_active_point = self.root
        is_end_point, split_state = self._test_and_split(active_state, left, idx - 1, self.string[idx])
        while not is_end_point:
            new_state = State(idx, float('inf'))
            split_state.transition[self.string[idx] if idx not in self.end_idxes else 'end{}'.format(idx)] = new_state
            if old_active_point != self.root:
                old_active_point.suffix_link = split_state
            old_active_point = split_state
            active_state, left = self._canonize(active_state.suffix_link, left, idx - 1)
            is_end_point, split_state = self._test_and_split(active_state, left, idx - 1, self.string[idx])
        if old_active_point != self.root:
            old_active_point.suffix_link = active_state
        return active_state, left

    def _test_and_split(self, active_state, left, right, char):
        if left > right:
            return char in active_state.transition, active_state
        next_state = active_state.transition[self.string[left]]
        next_char_idx = next_state.left + right - left + 1
        if right + 1 not in self.end_idxes and char == self.string[next_char_idx]:
            return True, active_state
        split_state = State(next_state.left, next_char_idx - 1)
        active_state.transition[self.string[left]] = split_state
        next_state.left = next_char_idx
        split_state.transition[self.string[next_char_idx]] = next_state
        return False, split_state

    def _canonize(self, active_state, left, right):
        if left > right:
            return active_state, left
        next_state = active_state.transition[self.string[left]]
        while next_state.right - next_state.left <= right - left:
            left += next_state.right - next_state.left + 1
            active_state = next_state
            if left <= right:
                next_state = active_state.transition[self.string[left]]
        return active_state, left
