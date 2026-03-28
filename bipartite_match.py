#!/usr/bin/env python3
"""bipartite_match - Maximum bipartite matching (Hopcroft-Karp)."""
import sys
from collections import deque
def hopcroft_karp(graph,n,m):
    match_l=[-1]*n;match_r=[-1]*m;INF=float('inf')
    def bfs():
        dist=[INF]*n;q=deque()
        for u in range(n):
            if match_l[u]==-1:dist[u]=0;q.append(u)
        found=False
        while q:
            u=q.popleft()
            for v in graph[u]:
                w=match_r[v]
                if w==-1:found=True
                elif dist[w]==INF:dist[w]=dist[u]+1;q.append(w)
        return found,dist
    def dfs(u,dist):
        for v in graph[u]:
            w=match_r[v]
            if w==-1 or(dist[w]==dist[u]+1 and dfs(w,dist)):
                match_l[u]=v;match_r[v]=u;return True
        dist[u]=INF;return False
    matching=0
    while True:
        found,dist=bfs()
        if not found:break
        for u in range(n):
            if match_l[u]==-1 and dfs(u,dist):matching+=1
    return matching,[(u,match_l[u]) for u in range(n) if match_l[u]!=-1]
if __name__=="__main__":
    graph={0:[0,1],1:[0],2:[1,2],3:[2]}  # left→right adjacency
    matching,pairs=hopcroft_karp(graph,4,3)
    print(f"Max matching: {matching}");
    for u,v in pairs:print(f"  L{u} — R{v}")
