# 標準入力を読み込み、全て整数型に変化
def read_input():
    input_ = []
    for _ in range(6):
        read_line = input().split()
        input_.append([string for string in map(float, read_line)])
    return input_

# nCmの組み合わせを返す関数
def create_combolution(dim: int, choice_num: int):
    """
    dim C choice_num の組み合わせを計算
    return [
        [x_1, x_2, x_3, ... , x_choice_num],
        ...
        [x_(dim - choice_num + 1), x_2, x_3, ... , x_dim],
    ]
    shape: (dim, choice_num)
    """
    OUTPUT_FORMAT = "{:0" + str(dim) + "b}"
    combolution_set = list()
    for i in range(2 ** dim):
        output_string = OUTPUT_FORMAT.format(i)
        if output_string.count("1") == choice_num:
            output_list = list(output_string)
            chice_set = list()
            for i, bin_string in enumerate(output_list):
                if bin_string == "1":
                    chice_set.append(i)
            combolution_set.append(chice_set)
    return combolution_set

# none_index([0, 1]など)で指定した部分をnoneにする関数
def insert_none_into_assignment(assignment: list, none_index: list):
    inserted_none_assignment = list()
    if len(none_index) == 0:
        inserted_none_assignment = assignment
        return inserted_none_assignment
    elif len(none_index) == 1:
        for order in assignment:
            order[none_index[0]] = None
            inserted_none_assignment.append(order)
        return inserted_none_assignment
    elif len(none_index) == 2:
        for order in assignment:
            order[none_index[0]], order[none_index[1]] = None, None
            inserted_none_assignment.append(order)
        return inserted_none_assignment
    else:
        raise("the length of none_index should be less than 3")

# 順列を返す関数 nPn
def create_permutation_set(choice_dim_set: list, assignment: list):
    """
    choice_dim = [0, 1, 2, 3, 4, 5]
    choice_dim = [0, 1, 4, 5]...

    assignment = [
        [0, 1, 2, 3],
        [0, 1, 3, 2],
        ...
        ]
    """
    dim = len(choice_dim_set)
    assignment.append(choice_dim_set.copy())
    for i in reversed(range(dim)):
        if i == 0:
            return assignment
        elif choice_dim_set[i - 1] < choice_dim_set[i]:
            # i - 1 が入れ替えるべきindex
            for j in reversed(range(i, dim)):
                if choice_dim_set[i - 1] < choice_dim_set[j]:
                    # 値をスワップする
                    choice_dim_set[i - 1], choice_dim_set[j] = choice_dim_set[j], choice_dim_set[i - 1]
                    choice_dim_set[i:dim] = choice_dim_set[(dim - 1):(i - 1):-1]
                    return create_permutation_set(choice_dim_set, assignment)
                else:
                    continue
        else:
            continue

# queenをassignmentの座標においてみてスコアを計算する
def set_queen(assignment, score):
    """
    # ('fail', [0, 1]) の時のスキップ機構の実装はうまくいっていない
    # skip_flag = False
    # skip_order = list()
    """
    max_score = 0
    # ステータスを返す -> ("filled", None), ("vacant", None), ("fail", [0, 1, 2])
    for order in assignment:
        # ('fail', [0, 1]) の時のスキップ機構の実装はうまくいっていない
        # status, fail_assignmet = fill_area(order)
        status, _ = fill_area(order)
        if status == "filled":
            """
            ('filled', None)
            """
            # スコア計算
            temp_score = 0
            for row_index, column_index in enumerate(order):
                if column_index is not None:
                    temp_score += score[row_index][column_index]
            if max_score < temp_score:
                max_score = temp_score
        elif (status == "vacant") | (status == "fail"):
            """
            ('vacant', None)
            ('fail', [0, 1])
            ('fail', [0, 2, 4, None, 3, 5])
            ...
            """
            # 処理をせずにとばす
            continue
    return max_score

# コマを置いたマスと置けなくなったマスを更新
def fill_area(choice_position: list):
    """
    choice_positions = [0, 1, 2, 3, 4, 5]
    """

    # Noneがあるなら最後までおいてから探索
    if None in choice_position:
        # 全部埋められるなら(None, None), 埋められないなら(-1, -1)を返す
        return set_queen_with_none(choice_position)
    # Noneがないなら途中までおいてダメだったらやめる
    else:
        # おけるなら(None, None), 置けないなら(座標(2, 1)など)を返す
        return set_queen_without_none(choice_position)

# Noneがあるなら最後までおいてから探索
def set_queen_with_none(choice_position: list):
    DIM = len(choice_position)
    invaded_area = [[0] * DIM for _ in range(DIM)]
    for row_index, column_index in enumerate(choice_position):
        # Noneが入っている行を場合分けして探索
        if column_index is None:
            if row_index == (DIM - 1):
                if is_filled_in(invaded_area):
                    # return None, None
                    return "filled", None
                else:
                    # return -1, -1
                    return "vacant", None
            else:
                continue
        # Noneが入っていない行で置けない場合通常通りreturn
        elif invaded_area[row_index][column_index] == 1:
            # return row_index, column_index
            return "fail", choice_position[:(row_index + 1)]
        # Noneが入っていない行で置ける場合通常通り探索
        else:
            # マス目を埋める
            invaded_area = invade_area(invaded_area, row_index, column_index)
            # 最後の行までいったら充填されているか確認
            if row_index == (DIM - 1):
                if is_filled_in(invaded_area):
                    # return None, None
                    return "filled", None
                else:
                    # return -1, -1
                    return "vacant", None

# queenの攻撃範囲のマス目を埋める
def invade_area(invaded_area, row_index: int, column_index: int):
    for i in range(6):
        # 列、行を更新
        invaded_area[i][column_index] = 1
        invaded_area[row_index][i] = 1
        # 左から右斜め、右から左斜めを更新
        if 0 <=  - i + row_index + column_index < 6:
            invaded_area[i][- i + row_index + column_index] = 1
        if 0 <= i - row_index + column_index < 6:
            invaded_area[i][i - row_index + column_index] = 1
    return invaded_area

# Noneがないなら途中までおいてダメだったらやめる
def set_queen_without_none(choice_position: list):
    DIM = len(choice_position)
    invaded_area = [[0] * DIM for _ in range(DIM)]
    for row_index, column_index in enumerate(choice_position):
        if invaded_area[row_index][column_index] == 1:
            # return row_index, column_index
            return "fail", choice_position[:(row_index + 1)]
        else:
            # マス目を埋める
            invaded_area = invade_area(invaded_area, row_index, column_index)
            if row_index == (DIM - 1):
                # return None, None
                return "filled", None

# その座標が埋まっているかどうかを計算する
def is_filled_in(invaded_area):
    for row in invaded_area:
        if 0 in row:
            return False
        else:
            continue
    return True

# メインの処理
def main():
    DIM = 6 # 盤面の行数
    CHOICE_NUM_SET = [0, 1, 2] # 置かない行数の設定
    max_score = 0.0 # 最大値スコア
    temp_score = 0.0 # スワップ用のスコア
    assignment = list() # 割り当て方法
    none_index_set = list() # 置かないマス
    score = read_input() # 盤面のスコア標準入力

    # コマを置いて、逐次で最大値を比べる
    for choice_num in CHOICE_NUM_SET:
        """
        assignment計算し直さないやり方がメモリ参照の点で失敗
        assignment = create_permutation_set(list(range(DIM)), [])
        """
        none_index_set = create_combolution(DIM, choice_num)
        for none_index in none_index_set:
            """
            assignment計算し直さないやり方がメモリ参照の点で失敗
            現在逐次で計算
            """
            assignment = create_permutation_set(list(range(DIM)), [])
            assignment = insert_none_into_assignment(assignment, none_index)
            temp_score = set_queen(assignment, score)
            if max_score < temp_score:
                max_score = temp_score

    # 最大値出力
    print(max_score)

if __name__ == '__main__':
    main()