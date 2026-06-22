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
#include <limits>

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

// 疑似 format_tour: 経路のインデックスを文字列（改行区切り）にする
std::string format_tour(const std::vector<int>& tour) {
    std::string result = "index\n";
    for (int idx : tour) {
        result += std::to_string(idx) + "\n";
    }
    return result;
}

// citiesの各位置情報にインデックスを付与する関数
std::vector<IndexedCity> give_index_cities(const std::vector<Point>& cities) {
    std::vector<IndexedCity> index_cities;
    index_cities.reserve(cities.size());
    for (size_t i = 0; i < cities.size(); ++i) {
        index_cities.push_back({static_cast<int>(i), cities[i]});
    }
    return index_cities;
}

// 2点間のユークリッド距離を求める関数
double calurate_euclidean_distance(const Point& city1, const Point& city2) {
    return std::sqrt(std::pow(city1.x - city2.x, 2) + std::pow(city1.y - city2.y, 2));
}

// 各都市の距離を求める関数（距離行列の作成）
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

// 現在の経路の総距離を計算する関数（評価関数）
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

// 【拡張】指定された都市からスタートする貪欲法
std::vector<IndexedCity> greedy_multi_start(const std::vector<Point>& cities, 
                                            const std::vector<std::vector<double>>& dist, 
                                            const std::vector<IndexedCity>& index_cities,
                                            int start_city) {
    int current_city = start_city;
    
    // 未訪問都市の管理（速度向上のため、std::setの代わりに配列/vectorでフラグ管理）
    std::vector<bool> visited(cities.size(), false);
    visited[start_city] = true;
    
    std::vector<IndexedCity> path;
    path.reserve(cities.size());
    path.push_back(index_cities[start_city]);

    for (size_t step = 1; step < cities.size(); ++step) {
        int next_city = -1;
        double min_dist = std::numeric_limits<double>::max();
        
        for (size_t city = 0; city < cities.size(); ++city) {
            if (!visited[city] && dist[current_city][city] < min_dist) {
                min_dist = dist[current_city][city];
                next_city = static_cast<int>(city);
            }
        }
        
        visited[next_city] = true;
        path.push_back(index_cities[next_city]);
        current_city = next_city;
    }

    return path;
}

// 焼きなまし法（Simulated Annealing）
std::vector<IndexedCity> simulated_annealing(const std::vector<IndexedCity>& init_path, 
                                             const std::vector<std::vector<double>>& dist, 
                                             int steps = 100000, 
                                             double init_temp = 100.0, 
                                             double cool_rate = 0.9999) {
    std::vector<IndexedCity> current_path = init_path;
    double current_dist = get_total_distance(current_path, dist);
    
    std::vector<IndexedCity> best_path = current_path;
    double best_dist = current_dist;
    
    int num_cities = static_cast<int>(current_path.size());
    double T = init_temp;

    std::random_device rd;
    std::mt19937 g(rd());
    std::uniform_real_distribution<double> rand_double(0.0, 1.0);

    for (int step = 0; step < steps; ++step) {
        std::uniform_int_distribution<int> rand_i(0, num_cities - 2);
        int i = rand_i(g);
        std::uniform_int_distribution<int> rand_j(i + 1, num_cities - 1);
        int j = rand_j(g);
        
        if (i == 0 && j == num_cities - 1) {
            continue;
        }

        int c_i = current_path[i].index;
        int c_i1 = current_path[i+1].index;
        int c_j = current_path[j].index;
        int c_j1 = current_path[(j+1) % num_cities].index;

        double before = dist[c_i][c_i1] + dist[c_j][c_j1];
        double after = dist[c_i][c_j] + dist[c_i1][c_j1];
        
        double diff = after - before;
        
        if (diff < 0 || rand_double(g) < std::exp(-diff / T)) {
            std::reverse(current_path.begin() + (i + 1), current_path.begin() + (j + 1));
            current_dist += diff;
            
            if (current_dist < best_dist) {
                best_dist = current_dist;
                best_path = current_path;
            }
        }
        T *= cool_rate;
    }

    std::cout << "Initial Distance (Best Greedy): " << std::fixed << std::setprecision(2) << get_total_distance(init_path, dist) << std::endl;
    std::cout << "Optimized Distance (SA): " << std::fixed << std::setprecision(2) << best_dist << std::endl;
    return best_path;
}

// TSPを解くメイン関数
std::vector<int> solve_tsp(const std::vector<Point>& cities) {
    auto dist = calcurate_distance(cities);
    auto index_cities = give_index_cities(cities);
    
    // ====================================================================
    // マルチスタート貪欲法の実装部分
    // ====================================================================
    std::vector<IndexedCity> best_init_path;
    double min_init_dist = std::numeric_limits<double>::max();
    
    int num_cities = static_cast<int>(cities.size());
    
    // 都市数が多い（Challenge 6のように2048など）場合は、最大でも全都市数分、
    // あるいは時間制限に合わせて試行回数を調整します。C++なら2048回でも一瞬です。
    int max_trials = std::min(num_cities, 2048); 
    
    for (int start = 0; start < max_trials; ++start) {
        auto trial_path = greedy_multi_start(cities, dist, index_cities, start);
        double trial_dist = get_total_distance(trial_path, dist);
        
        if (trial_dist < min_init_dist) {
            min_init_dist = trial_dist;
            best_init_path = std::move(trial_path);
        }
    }
    // ====================================================================
    
    // 最良の初期解を焼きなまし法に渡す
    auto optimized_cities = simulated_annealing(best_init_path, dist, 10000000, 100.0, 0.99999);

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