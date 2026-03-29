#!/usr/bin/env python3
"""Maximum bipartite matching via Hopcroft-Karp algorithm."""
import sys
from collections import deque

def hopcroft_karp(n, m, adj):
    """n=left nodes, m=right nodes, adj[u]=[list of right nodes]"""
    match_l = [-1]*n; match_r = [-1]*m; INF = float('inf')
    def bfs():
        dist = [INF]*n; q = deque()
        for u in range(n):
            if match_l[u] == -1: dist[u] = 0; q.append(u)
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                w = match_r[v]
                if w == -1: found = True
                elif dist[w] == INF: dist[w] = dist[u]+1; q.append(w)
        return found, dist
    def dfs(u, dist):
        for v in adj[u]:
            w = match_r[v]
            if w == -1 or (dist[w] == dist[u]+1 and dfs(w, dist)):
                match_l[u] = v; match_r[v] = u; return True
        dist[u] = INF; return False
    matching = 0
    while True:
        found, dist = bfs()
        if not found: break
        for u in range(n):
            if match_l[u] == -1:
                if dfs(u, dist): matching += 1
    return matching, match_l, match_r

def main():
    adj = [[0,1],[0,2],[1],[2,3]]
    m, ml, mr = hopcroft_karp(4, 4, adj)
    print(f"Max matching: {m}")
    for u, v in enumerate(ml):
        if v >= 0: print(f"  L{u} -> R{v}")

if __name__ == "__main__": main()
