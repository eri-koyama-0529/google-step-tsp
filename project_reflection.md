# greedy_2opt.pyを実装に関して

### うまくいった点

- 今見ている点から最近の点を次に訪問する点として選択できた。（`greedy`メソッド）
- 2本で交差している点は改善できた。(`two_opt`メソッド)
    - `two_opt`メソッドを1回実行するだけではなく、3回もしくは5回と実行数を増やすとNが大きい時に改善が見られた

### うまくいかなかった点
- 2-optなので、3本以上交差している点において解決できなかった。
    - スタートの点とゴールの点をつなぐ際に、交差が発生するが、2-optはここを確認できていない。　

#### 参考にしたサイト
- [巡回セールスマン問題をいろんな近似解法で解く（その1: 総当たり法とグリーディ法）](https://qiita.com/take314/items/dc2e6cf6d97889923c8b)
- [C言語で2-opt法を実装してみた](https://withcation.com/2019/05/23/post-555)

# solver_annealing.pyについて

```
Challenge 0
output          :    3291.62
sample/random   :    3862.20
sample/sa       :    3291.62

Challenge 1
output          :    3778.72
sample/random   :    6101.57
sample/sa       :    3778.72

Challenge 2
output          :    4494.42
sample/random   :   13479.25
sample/sa       :    4494.42

Challenge 3
output          :    8209.33
sample/random   :   47521.08
sample/sa       :    8150.91

Challenge 4
output          :   11094.30
sample/random   :   92719.14
sample/sa       :   10675.29

Challenge 5
output          :   22347.45
sample/random   :  347392.97
sample/sa       :   21119.55

Challenge 6
output          :   49820.85
sample/random   : 1374393.14
sample/sa       :   44393.89
```

# C++にしてみた結果
```
Challenge 0
output          :    3291.62
sample/random   :    3862.20
sample/sa       :    3291.62

Challenge 1
output          :    3778.72
sample/random   :    6101.57
sample/sa       :    3778.72

Challenge 2
output          :    4494.42
sample/random   :   13479.25
sample/sa       :    4494.42

Challenge 3
output          :    8138.76
sample/random   :   47521.08
sample/sa       :    8150.91

Challenge 4
output          :   10825.62
sample/random   :   92719.14
sample/sa       :   10675.29

Challenge 5
output          :   22373.04
sample/random   :  347392.97
sample/sa       :   21119.55

Challenge 6
output          :   45167.28
sample/random   : 1374393.14
sample/sa       :   44393.89
```