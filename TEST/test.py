from collections import deque

length = int(input())
n = int(input())
right = deque(sorted(map(int, input().split())))
m = int(input())
left = deque(sorted(map(int, input().split())))
addLeft, addRight = 0, 0

INF = 2*10**9
ans = 0
while right or left:
    L = left[0] + addLeft if left else INF
    R = length - (right[-1] + addRight) if right else INF
    m = min(L, R)
    ans += m
    addLeft -= m
    addRight += m
    if L < R:
        left.popleft()
        left, addLeft, right, addRight = right, addRight, left, addLeft
    elif L == R:
        left.popleft()
        right.pop()
    else:
        right.pop()
        left, addLeft, right, addRight = right, addRight, left, addLeft
print (ans)