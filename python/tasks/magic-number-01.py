import sys

def sum_sq_calc(num):
    series = []
    for i in str(num):
        series.append(int(i)*int(i))
    return int(sum(series))

seen = []
count = 0

def magic(num):
    global count
    seen.append(num)
    new_num = sum_sq_calc(num)
    count += 1
    print('=>', new_num)
    if new_num == 1:
        return True
    if new_num not in seen:
        state = magic(new_num)
    else:
        return False
    return state
    
print(magic(sys.argv[1]), count)
