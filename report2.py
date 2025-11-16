import sys, copy, random
input = sys.stdin.readline

def check_reflexive(W):
    for i in range(N):
        if W[i][i] != 1:
            return False
    return True

def check_symmetric(W):
    for i in range(N):
        for j in range(i+1, N):
            if W[i][j] != W[j][i]:
                return False
    return True

def check_transitive(W):
    origin = copy.deepcopy(W)
    for _ in range(N):
        Wn = [[0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    Wn[i][j] += W[i][k]*W[k][j]
                Wn[i][j] = min(1, Wn[i][j])
        W = copy.deepcopy(Wn)
    
    for i in range(N):
        for j in range(N):
            if W[i][j] != origin[i][j]:
                return False
    return True

def reflexive_closure(W):
    Wn = copy.deepcopy(W)
    for i in range(N):
        Wn[i][i] = 1
    return Wn

def symmetric_closure(W):
    Wn = copy.deepcopy(W)
    for i in range(N):
        for j in range(N):
            if Wn[i][j] == 1:
                Wn[j][i] = 1
    return Wn

def transitive_closure(W):
    Wn = copy.deepcopy(W)
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if Wn[i][k] == 1 and Wn[k][j] == 1:
                    Wn[i][j] = 1
    return Wn

def out(W, meg):
    print(meg)
    for x in W:
        print(*x)
    print()
    
class unionfind:
    def __init__(self):
        self.disjoint = [i for i in range(N)] 
    
    def find(self, x):
        stack = [x]
        while self.disjoint[stack[-1]] != stack[-1]:
            stack.append(self.disjoint[stack[-1]])
        top = stack[-1]
        for i in range(len(stack)-1):
            self.disjoint[stack[i]] = top
        return self.disjoint[x]

    def union(self, x, y):
        if self.find(x) != self.find(y):
            self.disjoint[self.find(x)] = self.find(y)

    def union_find(self):
        for i in range(N):
            for j in range(i+1, N):
                if rel[i][j]: self.union(i, j)
        return self.out()

    def out(self):
        arr = []
        dist = {}
        for i in range(N):
            if self.find(i) in dist:
                dist[self.find(i)].append(i)
            else:
                dist[self.find(i)] = [i]
                arr.append(self.find(i))
        return arr, dist
#입력
N = 5
rel = [list(map(int, input().split())) for _ in range(N)]

#동치관계 판별
ref = check_reflexive(rel); sym = check_symmetric(rel); tran = check_transitive(rel)
print(f"반사관계 : {ref}")
print(f"대칭관계 : {sym}")
print(f"추이관계 : {tran}", end="\n\n")

if ref and sym and tran:
    #동치류 찾기
    UF = unionfind()
    root, dist = UF.union_find()
    print("동치류 찾기(대표원소=그 집합에 속하는 원소) : ")
    print(dist, end="\n\n")
    
    #추가 기능 : 랜덤한 2개의 동치류를 합쳤을 경우
    if len(root) >=2:
        a, b = random.sample(root, 2)
        UF.union(a, b)
        after_root, after_dist = UF.out()
        print("유니온 이후 결과 : ")
        print(after_dist)
else:
    #폐포 찾기
    if not ref:
        out(reflexive_closure(rel), "반사폐포 : ")
    if not sym:
        out(symmetric_closure(rel), "대칭폐포 : ")
    if not tran:
        out(transitive_closure(rel), "추이폐포 : ")
