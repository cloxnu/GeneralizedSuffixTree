import random
import time
from Application import *
from dp import *

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()[]{}`~;':\",./<>?"

def random_str(length_range, common_length_range, k):
    length = random.randint(length_range[0], length_range[1])
    common_length = random.randint(common_length_range[0], common_length_range[1])
    common = ''.join(random.choices(chars, k=common_length))
    res = []
    for _ in range(k):
        insert_idx = random.randint(0, length)
        s_l = ''.join(random.choices(chars, k=insert_idx))
        s_r = ''.join(random.choices(chars, k=length - insert_idx))
        res.append(s_l + common + s_r)
    return res

s = random_str((10000, 20000), (500, 1000), 2)

s1, s2 = s[0], s[1]

print("random string has been generated")

t1 = time.time()

gst_res = lcs2(s1, s2)

t2 = time.time()

dp_res = lcs_in_dp(s1, s2)

t3 = time.time()

print("gst_res: {}\ndp_res: {}\n\ngst_time: {} ms\ndp_time: {} ms".format(gst_res, dp_res, (t2 - t1) * 1000, (t3 - t2) * 1000))

