#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
#include <set>
#include <algorithm>
#include <random>
#include <cassert>
#include <iomanip>

// 都市の構造体：(x, y) 座標を持つ
struct Point {
    double x;
    double y;
};

// インデックス付き都市の構造体
struct IndexedCity {
    int index;
    Point pos;
};

// 1行の文字列をカンマやスペースで分割する補助関数（CSV等読み込み用）
std::vector<std::string> split(const std::string& str) {
    std::vector<std::string> result;
    std::string current = "";
    for (char c : str) {
        if (c == ',' || c == ' ' || c == '\t' || c == '\n' || c == '\r') {
            if (!current.empty()) {
                result.push_back(current);
                current = "";
            }
        } else {
            current += c;
        }
    }
    if (!current.empty()) result.push_back(current);
    return result;
}

// 疑似 read_input: ファイルから都市の座標を読み込む
std::vector<Point> read_input(const std::string& filename) {
    std::ifstream ifs(filename);
    if (!ifs.is_open()) {
        std::cerr << "Error: Cannot open input file " << filename << std::endl;
        std::exit(1);
    }
    std::vector<Point> cities;
    std::string line;
    if (std::getline(ifs, line)) {
        auto tokens = split(line);
        if (!tokens.empty()) {
            try {
                std::stod(tokens[0]);
                cities.push_back({std::stod(tokens[0]), std::stod(tokens[1])});
            } catch (...) {
                // ヘッダーだった場合は飛ばす
            }
        }
    }
    while (std::getline(ifs, line)) {
        auto tokens = split(line);
        if (tokens.size() >= 2) {
            cities.push_back({std::stod(tokens[0]), std::stod(tokens[1])});
        }
    }
    return cities;
}

std::string format_tour(const std::vector<int>& tour) {
    std::string result = "index\n";
    for (int idx : tour) {
        result += std::to_string(idx) + "\n";
    }
    return result;
}

std::vector<IndexedCity> give_index_cities(const std::vector<Point>& cities) {
    std::vector<IndexedCity> index_cities;
    index_cities.reserve(cities.size());
    for (size_t i = 0; i < cities.size(); ++i) {
        index_cities.push_back({static_cast<int>(i), cities[i]});
    }
    return index_cities;
}

double calurate_euclidean_distance(const Point& city1, const Point& city2) {
    return std::sqrt(std::pow(city1.x - city2.x, 2) + std::pow(city1.y - city2.y, 2));
}

std::vector<std::vector<double>> calcurate_distance(const std::vector<Point>& cities) {
    size_t num_cities = cities.size();
    std::vector<std::vector<double>> distance_matrix(num_cities, std::vector<double>(num_cities, 0.0));

    for (size_t i = 0; i < num_cities; ++i) {
        for (size_t j = i + 1; j < num_cities; ++j) {
            double distance = calurate_euclidean_distance(cities[i], cities[j]);
            distance_matrix[i][j] = distance_matrix[j][i] = distance;
        }
    }
    return distance_matrix;
}

std::vector<IndexedCity> greedy(const std::vector<Point>& cities, 
                                const std::vector<std::vector<double>>& dist, 
                                const std::vector<IndexedCity>& index_cities) {
    int current_city = 0;
    std::set<int> unvisited;
    for (size_t i = 1; i < cities.size(); ++i) {
        unvisited.insert(static_cast<int>(i));
    }
    
    std::vector<IndexedCity> path;
    path.push_back(index_cities[0]);

    while (!unvisited.empty()) {
        int next_city = -1;
        double min_dist = std::numeric_limits<double>::max();
        for (int city : unvisited) {
            if (dist[current_city][city] < min_dist) {
                min_dist = dist[current_city][city];
                next_city = city;
            }
        }
        unvisited.erase(next_city);
        path.push_back(index_cities[next_city]);
        current_city = next_city;
    }

    return path;
}

double get_total_distance(const std::vector<IndexedCity>& path, const std::vector<std::vector<double>>& dist) {
    double total = 0.0;
    size_t num_cities = path.size();
    for (size_t i = 0; i < num_cities; ++i) {
        int c1 = path[i].index;
        int c2 = path[(i + 1) % num_cities].index;
        total += dist[c1][c2];
    }
    return total;
}

// ====================================================================
// 近傍限定 3-opt 組み込み焼きなまし法
// ====================================================================
std::vector<IndexedCity> simulated_annealing_3opt(const std::vector<IndexedCity>& init_path, 
                                                  const std::vector<std::vector<double>>& dist, 
                                                  int steps = 15000000, 
                                                  double init_temp = 30.0, 
                                                  double cool_rate = 0.9999996) {
    std::vector<IndexedCity> current_path = init_path;
    double current_dist = get_total_distance(current_path, dist);
    
    std::vector<IndexedCity> best_path = current_path;
    double best_dist = current_dist;
    
    int n = static_cast<int>(current_path.size());
    double T = init_temp;

    std::random_device rd;
    std::mt19937 g(rd());
    std::uniform_real_distribution<double> rand_double(0.0, 1.0);

    // 各都市の近くの都市のインデックスを保持する近傍リスト(上位25個)の作成
    int K = std::min(25, n - 1);
    std::vector<std::vector<int>> neighbor_cities(n);
    for (int i = 0; i < n; ++i) {
        std::vector<std::pair<double, int>> temp;
        for (int j = 0; j < n; ++j) {
            if (i != j) temp.push_back({dist[i][j], j});
        }
        std::sort(temp.begin(), temp.end());
        for (int k = 0; k < K; ++k) {
            neighbor_cities[i].push_back(temp[k].second);
        }
    }

    // パス上での各都市(index)の位置(パスの何番目か)を追跡する逆引き配列
    std::vector<int> pos(n);
    for (int i = 0; i < n; ++i) {
        pos[current_path[i].index] = i;
    }

    for (int step = 0; step < steps; ++step) {
        // 1. パス上からベースとなるエッジ (i, i+1) をランダムに選択
        std::uniform_int_distribution<int> rand_n(0, n - 1);
        int i = rand_n(g);
        int i1 = (i + 1) % n;

        int c_i = current_path[i].index;

        // 2. 都市 i の幾何的近傍リストからランダムに2つの都市を選択し、パス上の位置 j, k を得る
        if (neighbor_cities[c_i].size() < 2) continue;
        std::uniform_int_distribution<int> rand_k_idx(0, neighbor_cities[c_i].size() - 1);
        
        int n1 = neighbor_cities[c_i][rand_k_idx(g)];
        int n2 = neighbor_cities[c_i][rand_k_idx(g)];
        if (n1 == n2) continue;

        int j = pos[n1];
        int k = pos[n2];

        // i < j < k の順序にソートして位置関係を確定させる
        std::vector<int> idxs = {i, j, k};
        std::sort(idxs.begin(), idxs.end());
        i = idxs[0]; j = idxs[1]; k = idxs[2];

        // 各区間が有効（隣接しすぎていない）か確認
        if (j - i < 2 || k - j < 2 || (n - 1) - k + i < 1) continue;

        int j1 = j + 1;
        int k1 = (k + 1) % n;

        // 都市の実際のインデックスを取得
        int A = current_path[i].index;   int B = current_path[i1].index;
        int C = current_path[j].index;   int D = current_path[j1].index;
        int E = current_path[k].index;   int F = current_path[k1].index;

        // 現在の3本の辺の長さの合計
        double cur_edges_dist = dist[A][B] + dist[C][D] + dist[E][F];

        // 3-opt で代表的な「純粋な3辺繋ぎ替え（パスの部分反転では表せないパターン）」の距離を計算
        // A->C, B->E, D->F の接続を評価
        double new_edges_dist = dist[A][C] + dist[B][E] + dist[D][F];
        double diff = new_edges_dist - cur_edges_dist;

        if (diff < 0 || rand_double(g) < std::exp(-diff / T)) {
            // パス全体の再構築（Aの次からC、次にBからE、次にDからFへ）
            std::vector<IndexedCity> next_path;
            next_path.reserve(n);

            // 区間1: 0 から i まで
            for (int m = 0; m <= i; ++m) next_path.push_back(current_path[m]);
            // 区間2: j から i+1 まで（逆順に繋ぐ）
            for (int m = j; m >= i1; --m) next_path.push_back(current_path[m]);
            // 区間3: k から j1 まで（逆順に繋ぐ）
            for (int m = k; m >= j1; --m) next_path.push_back(current_path[m]);
            // 区間4: k1 から 最後まで
            for (int m = k1; m < n; ++m) next_path.push_back(current_path[m]);

            current_path = std::move(next_path);
            current_dist += diff;

            // 位置追跡配列の更新
            for (int m = 0; m < n; ++m) {
                pos[current_path[m].index] = m;
            }

            if (current_dist < best_dist) {
                best_dist = current_dist;
                best_path = current_path;
            }
        }
        T *= cool_rate;
    }

    std::cout << "Initial Distance (Greedy): " << std::fixed << std::setprecision(2) << get_total_distance(init_path, dist) << std::endl;
    std::cout << "Optimized Distance (SA with Neighbor 3-opt): " << std::fixed << std::setprecision(2) << best_dist << std::endl;
    return best_path;
}

std::vector<int> solve_tsp(const std::vector<Point>& cities) {
    auto dist = calcurate_distance(cities);
    auto index_cities = give_index_cities(cities);
    
    auto init_path = greedy(cities, dist, index_cities);
    
    // 3-optは強力なため、初期温度は少し低め(30.0)からじっくり冷やす設定がベスト
    auto optimized_cities = simulated_annealing_3opt(init_path, dist, 15000000, 30.0, 0.9999996);

    std::vector<int> path;
    path.reserve(optimized_cities.size());
    for (const auto& c : optimized_cities) {
        path.push_back(c.index);
    }
    return path;
}

int main(int argc, char* argv[]) {
    assert(argc > 1);
    
    std::string input_filename = argv[1];
    auto cities = read_input(input_filename);
    auto tour = solve_tsp(cities);

    std::string output_filename = input_filename;
    size_t pos = output_filename.find("input");
    if (pos != std::string::npos) {
        output_filename.replace(pos, 5, "output");
    } else {
        output_filename += ".output";
    }

    std::ofstream ofs(output_filename);
    if (ofs.is_open()) {
        ofs << format_tour(tour);
    }
    
    std::cout << "Done" << std::endl;
    return 0;
}