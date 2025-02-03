from collections import defaultdict
import math
from itertools import product
from functools import reduce

def get_distributions():
    sum_counts = defaultdict(int)
    product_counts = defaultdict(int)
    joint_counts = defaultdict(int)
    total = 36  # 6^2 для двух костей
    
    for dice in product(range(1,7), repeat=2):
        s = sum(dice)
        p = reduce(lambda x,y: x*y, dice)
        sum_counts[s] += 1
        product_counts[p] += 1
        joint_counts[(s,p)] += 1
    
    sum_dist = {k: v/total for k,v in sum_counts.items()}
    product_dist = {k: v/total for k,v in product_counts.items()}
    joint_dist = {k: v/total for k,v in joint_counts.items()}
    
    return sum_dist, product_dist, joint_dist

def entropy(prob_dict):
    return -sum(p * math.log2(p) for p in prob_dict.values())

def main():
    sum_p, prod_p, joint_p = get_distributions()
    
    h_ab = entropy(joint_p)
    h_a = entropy(sum_p)
    h_b = entropy(prod_p)
    ha_b = h_ab - h_a
    i_ab = h_b - ha_b
    
    return [round(x, 2) for x in (h_ab, h_a, h_b, ha_b, i_ab)]

if __name__ == "__main__":
    results = main()
    labels = [f"H(AB): {results[0]}", f"H(A): {results[1]}", f"H(B): {results[2]}", f"Ha(B): {results[3]}", f"I(A,B): {results[4]}"]
    
    for label in labels:
        print(label)
    print(results)