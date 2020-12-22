def lcs_in_dp(string1, string2):
    dp = [[0 for _ in string2] for _ in string1]
    longest_count, longest_last_idx = 0, 0
    for i in range(1, len(string1)):
        for j in range(1, len(string2)):
            dp[i][j] = dp[i-1][j-1] + 1 if string1[i] == string2[j] else 0
            if longest_count < dp[i][j]:
                longest_count = dp[i][j]
                longest_last_idx = i
    return string1[longest_last_idx+1-longest_count : longest_last_idx+1] if longest_last_idx else ""
