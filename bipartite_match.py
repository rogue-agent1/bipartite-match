#!/usr/bin/env python3
"""bipartite_match - Hungarian algorithm and Hopcroft-Karp matching."""
import sys, json
from collections import deque

def hopcroft_karp(adj, n_left, n_right):
    match_l = [-1]*n_left; match_r = [-1]*n_right
    
    def bfs():
        dist = [0]*n_left; queue = deque()
        for u in range(n_left):
            if match_l[u] == -1: dist[u] = 0; queue.append(u)
            else: dist[u] = float('inf')
        found = False
        while queue:
            u = queue.popleft()
            for v in adj.get(u, []):
                w = match_r[v]
                if w == -1: found = True
                elif dist[w] == float('inf'):
                    dist[w] = dist[u] + 1; queue.append(w)
        return found, dist
    
    def dfs(u, dist):
        for v in adj.get(u, []):
            w = match_r[v]
            if w == -1 or (dist[w] == dist[u]+1 and dfs(w, dist)):
                match_l[u] = v; match_r[v] = u; return True
        dist[u] = float('inf'); return False
    
    matching = 0
    while True:
        found, dist = bfs()
        if not found: break
        for u in range(n_left):
            if match_l[u] == -1:
                if dfs(u, dist): matching += 1
    return matching, list(zip(range(n_left), match_l))

def hungarian(cost):
    n = len(cost)
    u = [0]*(n+1); v = [0]*(n+1); p = [0]*(n+1); way = [0]*(n+1)
    for i in range(1, n+1):
        p[0] = i; j0 = 0
        minv = [float('inf')]*(n+1); used = [False]*(n+1)
        while True:
            used[j0] = True; i0 = p[j0]; delta = float('inf'); j1 = 0
            for j in range(1, n+1):
                if not used[j]:
                    cur = cost[i0-1][j-1] - u[i0] - v[j]
                    if cur < minv[j]: minv[j] = cur; way[j] = j0
                    if minv[j] < delta: delta = minv[j]; j1 = j
            for j in range(n+1):
                if used[j]: u[p[j]] += delta; v[j] -= delta
                else: minv[j] -= delta
            j0 = j1
            if p[j0] == 0: break
        while j0:
            p[j0] = p[way[j0]]; j0 = way[j0]
    assignment = [0]*n
    for j in range(1, n+1): assignment[p[j]-1] = j-1
    total = sum(cost[i][assignment[i]] for i in range(n))
    return total, assignment

def main():
    print("Bipartite matching demo\n")
    adj = {0:[0,1], 1:[0,2], 2:[1,2], 3:[2,3], 4:[3]}
    size, pairs = hopcroft_karp(adj, 5, 4)
    print(f"Hopcroft-Karp: {size} matches")
    for l, r in pairs:
        if r >= 0: print(f"  L{l} -> R{r}")
    cost = [[9,2,7,8],[6,4,3,7],[5,8,1,8],[7,6,9,4]]
    total, assign = hungarian(cost)
    print(f"\nHungarian (min cost): {total}")
    for i, j in enumerate(assign): print(f"  Worker {i} -> Job {j} (cost {cost[i][j]})")

if __name__ == "__main__":
    main()
