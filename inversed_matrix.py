def gauss(matrix):
    start = time.time()
    rref = copy.deepcopy(matrix)
    
    #단위행렬 만들기
    inv = [[0.0] * n for _ in range(n)]  
    for i in range(n):
        inv[i][i] = 1.0

    #모든 행에 대해서 피봇이 1이 되도록 맞춰줌
    for i in range(n):
        mx = abs(rref[i][i])
        idx = i
        for j in range(i + 1, n):
            if abs(rref[j][i]) > mx:
                mx = abs(rref[j][i])
                idx = j
        
        # 가장 큰 절댓값을 가진 행과 교환
        if idx != i:
            rref[i], rref[idx] = rref[idx], rref[i]
            inv[i], inv[idx] = inv[idx], inv[i]
        if abs(rref[i][i]) < 10**-10:
            now = time.time()
            print(f"{now-start}초 경과")
            return None, now-start
            
        #피봇을 1로 만들기
        coeff = 1.0 / rref[i][i]
        for j in range(n):
            rref[i][j] *= coeff
            inv[i][j] *= coeff
        for j in range(n):
            if i == j:
                continue
            
            t = rref[j][i]
            for k in range(n):
                rref[j][k] -= rref[i][k] * t
                inv[j][k] -= inv[i][k] * t
    
    now = time.time()
    print(f"{now-start}초 경과")
    
    #역행렬을 구할 수 없어, rref가 단위행렬이 되지 않는 경우
    for i in range(n):
        for j in range(n):
            if i != j and abs(rref[i][j]) > 1e-9:
                return None, now-start
    return inv, now-start

def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[1][0]*matrix[0][1]
    if len(matrix) == 1:
        return matrix[0][0]
    
    det = 0
    sign = 1
    for i in range(len(matrix)):
        temp = copy.deepcopy(matrix)
        temp.pop(0)
        for j in range(len(temp)):
            temp[j].pop(i)
        
        if matrix[0][i] != 0:
            det += sign*matrix[0][i]*determinant(temp)
        sign = 1 if sign == -1 else -1
    return det

def use_det(matrix):
    start = time.time()
    det = determinant(matrix)
    if det == 0:
        return None, 0
    
    c_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            temp = copy.deepcopy(matrix)
            temp.pop(i)
            for k in range(len(temp)):
                temp[k].pop(j)
                
            if (i+j)%2 == 0:
                sign = 1
            else:
                sign = -1
            c_matrix[j][i] = sign*(1/det)*determinant(temp)
    
    now = time.time()
    print(f"{now-start}초 경과")
    return c_matrix, now-start

def compare(arr1, arr2, time1, time2):
    if time1 < time2:
        print("가우스 조던 소거법이 더 빠릅니다")
    else:
        print("행렬식 이용이 더 빠릅니다.")
    
    for i in range(n):
        for j in range(n):
            if abs(arr1[i][j] - arr2[i][j]) > 10**-9: #실수오차 보정함.
                return False
    return True

import sys, copy, time
sys.setrecursionlimit(10**9)
input = sys.stdin.readline

if __name__ == "__main__":
    n = int(input().strip())
    arr = [list(map(int, input().split())) for _ in range(n)]
    
    print("1. 가우스 조던 방법")
    inv, time_inv = gauss(arr)
    if inv:
        for i in range(n):
            print(*inv[i])
    else:
        print("기약행 사다리꼴을 만들 수 없습니다.")
    print()
    
    print("2. 행렬식 이용")
    c_matrix, time_c = use_det(arr)
    if c_matrix:
        for i in range(n):
            print(*c_matrix[i])
    else:
        print("행렬식이 0이라 역행렬이 존재하지 않습니다.")
    print()
    
    if inv and c_matrix:
        if compare(inv, c_matrix, time_inv, time_c):
            print("결과가 같습니다.")
        else:
            print("결과가 다릅니다.")
