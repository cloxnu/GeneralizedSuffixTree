from STree import *

# 两个字符串间的最长公共子串
def lcs2(string1, string2, debug=False):
    string = string1 + "$" + string2 + "$"
    tree = STree()
    tree.build_with_automatic_end([string1, string2])
    if debug:
        print(tree)

    def dfs(state: State):
        if state.right == float('inf'):
            return '', state.left >= len(string) - len(string2) - 1
        res, has_string1, has_string2 = [], False, False
        for s in state.transition.values():
            res_string, is_string2 = dfs(s)
            if len(res_string) > 0:
                res.append((string[state.left:state.right + 1] if state.left != -1 else "") + res_string)
            else:
                if is_string2:
                    has_string2 = True
                else:
                    has_string1 = True
        if has_string1 and has_string2:
            res.append(string[state.left:state.right + 1])
        return max(res, key=lambda x: len(x)) if res else '', is_string2

    return dfs(tree.root)[0]

# 最长公共子串
def lcs(strings, debug=False):
    string = '$'.join(strings) + '$'
    str_lens = list(accumulate(strings, lambda x, y: x + len(y) + 1, initial=0))
    tree = STree()
    tree.build_with_automatic_end(strings)
    if debug:
        print(tree)

    def dfs(state: State):
        if state.right == float('inf'):
            return '', {next(i for i in range(len(str_lens) - 1) if state.left < str_lens[i + 1])}
        res, string_set = [], set()
        for s in state.transition.values():
            res_string, string_idxes = dfs(s)
            if len(res_string) > 0:
                res.append((string[state.left:state.right + 1] if state.left != -1 else "") + res_string)
            else:
                string_set.update(string_idxes)
        if len(string_set) == len(strings):
            res.append(string[state.left:state.right + 1])
        return max(res, key=lambda x: len(x)) if res else '', string_set

    return dfs(tree.root)[0]


if __name__ == '__main__':
    tree = STree()
    tree.build_with_automatic_end(["abacdacdacdbc"])
    # tree.build_with_automatic_end(["cacaocac", "ccaooc"])
    # tree.build("1234332214$")
    # tree.build("asjknx")
    print(tree)

    # print(lcs2("12335665464566321", "12366546456653321"))
    # print(lcs2("abcd", "bcd", debug=True))
    # print(lcs(["abcdfds", "bfdbcdfew", "bcdrgde"], debug=True))
