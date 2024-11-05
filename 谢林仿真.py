import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# np.random.seed(198108)

N = 50
threshold = 0.7
figsize=(12,12)

x = np.arange(N)
y = np.arange(N)
X, Y = np.meshgrid(x, y)
# Z = np.random.rand(N, N)
status = ["C1", "C4", 'white']
prob = [0.4, 0.4, 0.2]

def init_z():
    Z = np.random.choice(a=status, size=(N**2), p=prob)
    Z.shape = (N, N)
    return Z

Z = init_z()


#往上是初始化部分

def get_null_cells(Z):
    """获取空白格子的位置
    Z:np.array, N*N
    return:list of cells position
    """
    if not Z.shape == (N, N):
        Z.shape = (N, N)
    cells = np.where(Z == "white")
    return cells

def get_cell_happiness(Z, row, col):
    """获取每个单元格的满意程度阈值
    Z: N*N np.array
    row: int, col:int
    return: happiness:int
    """
    if not Z.shape == (N, N):
        Z.shape = (N, N)
    if Z[row, col] == "white":
        return np.NaN
    same, count = 0, 0
    left = 0 if col==0 else col-1
    right = Z.shape[1] if col==Z.shape[1]-1 else col+2
    top = 0 if row==0 else row-1
    bottom = Z.shape[0] if row==Z.shape[0]-1 else row+2
    # print(top, bottom, left, right)
    for i in range(top, bottom):
        for j in range(left, right):
            # print(list(range(left, right)))
            if (i, j) == (row, col) or Z[i,j] == "white":
                continue
            # print(Z[i,j], i, j)
            elif Z[i, j] == Z[row, col]:
                same += 1
                count += 1
            else:
                count += 1
    # print('in',same,count)
    if not count == 0:
        happiness = same / count
    else:
        happiness = 0
    return happiness

def get_all_happiness(Z):
    """得到所有格子的满意度
    return: np.array N*N
    """
    hap_scores = []
    for row in range(Z.shape[0]):
        for col in range(Z.shape[1]):
            # print(row, col)
            hap_scores.append(get_cell_happiness(Z, row, col))
    hap_scores = np.array(hap_scores)
    hap_scores.shape = Z.shape
    return hap_scores

def hap_mean(Z):
    """所有格子的平均满意度
    return: res -> int
    """
    hap_scores = get_all_happiness(Z)
    res = hap_scores[np.where(hap_scores>=0)].mean()
    return res

def get_unhap_cells(Z=Z, threshold=threshold):
    """得到不满意的格子
    return: tuple 2 items
    """
    hap_scores = get_all_happiness(Z)
    res = np.where(hap_scores < threshold)
    return res

def unhap_ratio(Z):
    hap_scores = get_all_happiness(Z)
    res = np.sum(hap_scores<threshold) / np.sum(hap_scores>=0)
    # unhap_count = len(get_unhap_cells()[0])
    # print(unhap_count)
    # res = unhap_count / len(Z[np.where(Z!="white")])
    return res

def move(Z):
    unhap_cells = get_unhap_cells()
    for i in range(len(unhap_cells[0])):
        blank_cells = get_null_cells(Z)
        unhap_row = unhap_cells[0][i]
        unhap_col = unhap_cells[1][i]
        j = np.random.choice(range(len(blank_cells[0])))
        blank_row = blank_cells[0][j]
        blank_col = blank_cells[1][j]
        Z[unhap_row, unhap_col], Z[blank_row, blank_row] = Z[blank_row, blank_row], Z[unhap_row, unhap_col]
