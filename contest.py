from collections import deque
import sys

def bfs(start, adj, n):
    dist = [-1] * (n + 1)
    parent = [-1] * (n + 1)
    q = deque([start])
    dist[start] = 0
    min_cycle = float('inf')

    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
            elif parent[u] != v:
                min_cycle = min(min_cycle, dist[u] + dist[v] + 1)
    return min_cycle

def main():
    input_data = sys.stdin.read().split()
    n, m = int(input_data[0]), int(input_data[1])
    adj = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        a, b = int(input_data[idx]), int(input_data[idx + 1])
        idx += 2
        adj[a].append(b)
        adj[b].append(a)

    ans = float('inf')
    for u in range(1, n + 1):
        ans = min(ans, bfs(u, adj, n))

    print(ans if ans != float('inf') else -1)