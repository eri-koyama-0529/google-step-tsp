// #include <iostream>
// #include <vector>
// #include <string>
// #include <fstream>
// #include <cmath>
// #include <set>
// #include <algorithm>
// #include <random>
// #include <cassert>
// #include <iomanip>

// // 都市の構造体：(x, y) 座標を持つ
// struct Point {
//     double x;
//     double y;
// };

// // インデックス付き都市の構造体
// struct IndexedCity {
//     int index;
//     Point pos;
// };

// // 1行の文字列をカンマやスペースで分割する補助関数（CSV等読み込み用）
// std::vector<std::string> split(const std::string& str) {
//     std::vector<std::string> result;
//     std::string current = "";
//     for (char c : str) {
//         if (c == ',' || c == ' ' || c == '\t' || c == '\n' || c == '\r') {
//             if (!current.empty()) {
//                 result.push_back(current);
//                 current = "";
//             }
//         } else {
//             current += c;
//         }
//     }
//     if (!current.empty()) result.push_back(current);
//     return result;
// }

// // 疑似 read_input: ファイルから都市の座標を読み込む
// std::vector<Point> read_input(const std::string& filename) {
//     std::ifstream ifs(filename);
//     if (!ifs.is_open()) {
//         std::cerr << "Error: Cannot open input file " << filename << std::endl;
//         std::exit(1);
//     }
//     std::vector<Point> cities;
//     std::string line;
//     // 最初の1行目がヘッダー（"x,y" など）の場合はスキップする処理
//     if (std::getline(ifs, line)) {
//         auto tokens = split(line);
//         if (!tokens.empty()) {
//             // 1行目が数値でない（ヘッダーである）場合は飛ばす
//             try {
//                 std::stod(tokens[0]);
//                 // 数値に変換できたらデータなので処理する
//                 cities.push_back({std::stod(tokens[0]), std::stod(tokens[1])});
//             } catch (...) {
//                 // ヘッダーだった場合は何もしない（次の行から読み込む）
//             }
//         }
//     }
//     while (std::getline(ifs, line)) {
//         auto tokens = split(line);
//         if (tokens.size() >= 2) {
//             cities.push_back({std::stod(tokens[0]), std::stod(tokens[1])});
//         }
//     }
//     return cities;
// }

// // 疑似 format_tour: 経路のインデックスを文字列（改行区切り）にする
// std::string format_tour(const std::vector<int>& tour) {
//     std::string result = "index\n"; // ヘッダー
//     for (int idx : tour) {
//         result += std::to_string(idx) + "\n";
//     }
//     return result;
// }

// // citiesの各位置情報にインデックスを付与する関数
// std::vector<IndexedCity> give_index_cities(const std::vector<Point>& cities) {
//     std::vector<IndexedCity> index_cities;
//     index_cities.reserve(cities.size());
//     for (size_t i = 0; i < cities.size(); ++i) {
//         index_cities.push_back({static_cast<int>(i), cities[i]});
//     }
//     return index_cities;
// }

// // 2点間のユークリッド距離を求める関数
// double calurate_euclidean_distance(const Point& city1, const Point& city2) {
//     return std::sqrt(std::pow(city1.x - city2.x, 2) + std::pow(city1.y - city2.y, 2));
// }

// // 各都市の距離を求める関数（距離行列の作成）
// std::vector<std::vector<double>> calcurate_distance(const std::vector<Point>& cities) {
//     size_t num_cities = cities.size();
//     std::vector<std::vector<double>> distance_matrix(num_cities, std::vector<double>(num_cities, 0.0));

//     for (size_t i = 0; i < num_cities; ++i) {
//         for (size_t j = i + 1; j < num_cities; ++j) {
//             double distance = calurate_euclidean_distance(cities[i], cities[j]);
//             distance_matrix[i][j] = distance_matrix[j][i] = distance;
//         }
//     }
//     return distance_matrix;
// }

// // 貪欲法で初期経路を求める関数
// std::vector<IndexedCity> greedy(const std::vector<Point>& cities, 
//                                 const std::vector<std::vector<double>>& dist, 
//                                 const std::vector<IndexedCity>& index_cities) {
//     int current_city = 0;
//     std::set<int> unvisited;
//     for (size_t i = 1; i < cities.size(); ++i) {
//         unvisited.insert(static_cast<int>(i));
//     }
    
//     std::vector<IndexedCity> path;
//     path.push_back(index_cities[0]);

//     while (!unvisited.empty()) {
//         // Pythonの min(unvisited, key=...) を再現
//         int next_city = -1;
//         double min_dist = std::numeric_limits<double>::max();
//         for (int city : unvisited) {
//             if (dist[current_city][city] < min_dist) {
//                 min_dist = dist[current_city][city];
//                 next_city = city;
//             }
//         }
//         unvisited.erase(next_city);
//         path.push_back(index_cities[next_city]);
//         current_city = next_city;
//     }

//     return path;
// }

// // 現在の経路の総距離を計算する関数（評価関数）
// double get_total_distance(const std::vector<IndexedCity>& path, const std::vector<std::vector<double>>& dist) {
//     double total = 0.0;
//     size_t num_cities = path.size();
//     for (size_t i = 0; i < num_cities; ++i) {
//         int c1 = path[i].index;
//         int c2 = path[(i + 1) % num_cities].index;
//         total += dist[c1][c2];
//     }
//     return total;
// }

// // 焼きなまし法（Simulated Annealing）
// std::vector<IndexedCity> simulated_annealing(const std::vector<IndexedCity>& init_path, 
//                                              const std::vector<std::vector<double>>& dist, 
//                                              int steps = 100000, 
//                                              double init_temp = 100.0, 
//                                              double cool_rate = 0.9999) {
//     std::vector<IndexedCity> current_path = init_path;
//     double current_dist = get_total_distance(current_path, dist);
    
//     std::vector<IndexedCity> best_path = current_path;
//     double best_dist = current_dist;
    
//     int num_cities = static_cast<int>(current_path.size());
//     double T = init_temp;

//     // 高速なメルセンヌ・ツイスター乱数生成器 (Pythonのrandomとほぼ同等)
//     std::random_device rd;
//     std::mt19937 g(rd());
//     std::uniform_real_distribution<double> rand_double(0.0, 1.0);

//     for (int step = 0; step < steps; ++step) {
//         // 2-opt近傍のインデックスをランダムに選択
//         std::uniform_int_distribution<int> rand_i(0, num_cities - 2);
//         int i = rand_i(g);
//         std::uniform_int_distribution<int> rand_j(i + 1, num_cities - 1);
//         int j = rand_j(g);
        
//         if (i == 0 && j == num_cities - 1) {
//             continue;
//         }

//         int c_i = current_path[i].index;
//         int c_i1 = current_path[i+1].index;
//         int c_j = current_path[j].index;
//         int c_j1 = current_path[(j+1) % num_cities].index;

//         double before = dist[c_i][c_i1] + dist[c_j][c_j1];
//         double after = dist[c_i][c_j] + dist[c_i1][c_j1];
        
//         double diff = after - before;
        
//         if (diff < 0 || rand_double(g) < std::exp(-diff / T)) {
//             // Pythonの current_path[i+1:j+1] = reversed(...) を再現
//             std::reverse(current_path.begin() + (i + 1), current_path.begin() + (j + 1));
//             current_dist += diff;
            
//             if (current_dist < best_dist) {
//                 best_dist = current_dist;
//                 best_path = current_path;
//             }
//         }
//         T *= cool_rate;
//     }

//     // 小数点以下2桁で出力
//     std::cout << "Initial Distance (Greedy): " << std::fixed << std::setprecision(2) << get_total_distance(init_path, dist) << std::endl;
//     std::cout << "Optimized Distance (SA): " << std::fixed << std::setprecision(2) << best_dist << std::endl;
//     return best_path;
// }

// // TSPを解くメイン関数
// std::vector<int> solve_tsp(const std::vector<Point>& cities) {
//     auto dist = calcurate_distance(cities);
//     auto index_cities = give_index_cities(cities);
    
//     auto init_path = greedy(cities, dist, index_cities);
    
//     // Pythonコードの引数指定（steps=200000, init_temp=50.0, cool_rate=0.99995）に合わせる
//     auto optimized_cities = simulated_annealing(init_path, dist, 10000000, 100.0, 0.99999);

//     std::vector<int> path;
//     path.reserve(optimized_cities.size());
//     for (const auto& c : optimized_cities) {
//         path.push_back(c.index);
//     }
//     return path;
// }

// int main(int argc, char* argv[]) {
//     assert(argc > 1);
    
//     std::string input_filename = argv[1];
//     auto cities = read_input(input_filename);
//     auto tour = solve_tsp(cities);

//     // Pythonの `.replace("input", "output")` を再現
//     std::string output_filename = input_filename;
//     size_t pos = output_filename.find("input");
//     if (pos != std::string::npos) {
//         output_filename.replace(pos, 5, "output");
//     } else {
//         output_filename += ".output"; // "input" という文字列がなければ末尾に付与
//     }

//     std::ofstream ofs(output_filename);
//     if (ofs.is_open()) {
//         ofs << format_tour(tour);
//     }
    
//     std::cout << "Done" << std::endl;
//     return 0;
// }

