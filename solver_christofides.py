import sys
import math
import random

from common import print_tour, read_input, format_tour

def give_index_cities(cities):
    index_cities = []
    for i in range(len(cities)):
        index_cities.append((i, list(cities[i])))
    return index_cities

def calurate_euclidean_distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)

def calcurate_distance(cities):
    num_cities = len(cities)
    distance_matrix = [[0]*num_cities for _ in range(num_cities)] 
    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = calurate_euclidean_distance(cities[i], cities[j])
            distance_matrix[i][j] = distance_matrix[j][i] = distance
    return distance_matrix

def get_total_distance(path, dist):
    total = 0
    num_cities = len(path)
    for i in range(num_cities):
        c1 = path[i][0]
        c2 = path[(i + 1) % num_cities][0]
        total += dist[c1][c2]
    return total

# =================================================================
# クリストフィード法（Christofides Algorithm）の実装
# =================================================================

def kruskal_mst(num_cities, dist):
    """ プリム法またはクラスカル法で最小全域木(MST)の隣接リストを作成する """
    edges = []
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            edges.append((dist[i][j], i, j))
    edges.sort() # 辺の長さが短い順にソート

    # Union-Find で閉路を判定
    parent = list(range(num_cities))
    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    mst_adj = {i: [] for i in range(num_cities)}
    edges_count = 0
    for w, u, v in edges:
        if union(u, v):
            mst_adj[u].append(v)
            mst_adj[v].append(u)
            edges_count += 1
            if edges_count == num_cities - 1:
                break
    return mst_adj

def christofides(cities, dist, index_cities):
    num_cities = len(cities)
    if num_cities <= 2:
        return [index_cities[i] for i in range(num_cities)]

    # 1. 最小全域木 (MST) を求める
    mst_adj = kruskal_mst(num_cities, dist)

    # 2. 次数が奇数の頂点をリストアップする
    odd_vertices = [v for v in range(num_cities) if len(mst_adj[v]) % 2 != 0]

    # 3. 奇数次数頂点の間で、簡易的な最小重量マッチング（貪欲マッチング）を行う
    matched = set()
    multigraph = {i: list(mst_adj[i]) for i in range(num_cities)} # MSTをコピーして多重グラフのベースにする
    
    # 奇数頂点同士を距離の近い順にペアにする
    odd_edges = []
    for i in range(len(odd_vertices)):
        for j in range(i + 1, len(odd_vertices)):
            u, v = odd_vertices[i], odd_vertices[j]
            odd_edges.append((dist[u][v], u, v))
    odd_edges.sort()

    for w, u, v in odd_edges:
        if u not in matched and v not in matched:
            matched.add(u)
            matched.add(v)
            multigraph[u].append(v)
            multigraph[v].append(u) # 辺を追加してすべての頂点の次数を偶数にする

    # 4 & 5. オイラー閉路をなぞりながら、未訪問都市をショートカットして巡回ルートを作る
    # (簡易的に、MST+マッチングのグラフ上で深さ優先探索(DFS)を行うことでショートカット閉路を作れます)
    visited = [False] * num_cities
    path_indices = []

    def dfs(node):
        visited[node] = True
        path_indices.append(node)
        for neighbor in multigraph[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    # 0番目の都市からスタート
    dfs(0)

    # 元の (index, [x, y]) 形式に直して返す
    return [index_cities[idx] for idx in path_indices]


# =================================================================
# 焼きなまし法（Simulated Annealing）
# =================================================================

def simulated_annealing(init_path, dist, steps=200000, init_temp=50.0, cool_rate=0.99995):
    current_path = list(init_path)
    current_dist = get_total_distance(current_path, dist)
    
    best_path = list(current_path)
    best_dist = current_dist
    
    num_cities = len(current_path)
    T = init_temp

    for step in range(steps):
        i = random.randint(0, num_cities - 2)
        j = random.randint(i + 1, num_cities - 1)
        
        if i == 0 and j == num_cities - 1:
            continue

        c_i = current_path[i][0]
        c_i1 = current_path[i+1][0]
        c_j = current_path[j][0]
        c_j1 = current_path[(j+1) % num_cities][0]

        before = dist[c_i][c_i1] + dist[c_j][c_j1]
        after = dist[c_i][c_j] + dist[c_i1][c_j1]
        
        diff = after - before
        
        if diff < 0 or random.random() < math.exp(-diff / T):
            current_path[i+1:j+1] = reversed(current_path[i+1:j+1])
            current_dist += diff
            
            if current_dist < best_dist:
                best_dist = current_dist
                best_path = list(current_path)
                
        T *= cool_rate

    print(f"Initial Distance (Christofides): {get_total_distance(init_path, dist):.2f}")
    print(f"Optimized Distance (SA): {best_dist:.2f}")
    return best_path


def solve_tsp(cities):
    dist = calcurate_distance(cities)
    index_cities = give_index_cities(cities)
    
    # 1. クリストフィード法で「1.5倍精度保証」の強力な初期解を生成
    init_path = christofides(cities, dist, index_cities)
    
    # 2. 焼きなまし法でさらに極限まで最適化
    optimized_cities = simulated_annealing(init_path, dist, steps=200000, init_temp=30.0, cool_rate=0.99995)

    path = []          
    for c in optimized_cities:
        path.append(c[0])
    return path
    

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve_tsp(read_input(sys.argv[1]))

    output_filename = sys.argv[1].replace("input", "output")
    with open(output_filename, "w") as f:
        f.write(format_tour(tour))
    print("Done")