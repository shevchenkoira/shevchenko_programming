def input_num():
    while True:
        try:
            new_num = int(input("Enter size of your array: "))
            return new_num
        except ValueError:
            print("Try again, because you didn't enter a number")


def fill_arr():
    size_n = input_num()
    while True:
        try:
            my_arr = [int(input("Enter" + " " + str(i) + " " + "number: ")) for i in range(size_n)]
            return my_arr
        except ValueError:
            print("Нou didn't enter a number, try again from the beginning")


def is_raising(arr_to_check: []):
    for i in range(len(arr_to_check) - 1):
        if arr_to_check[i] > arr_to_check[i+1]:
            break
    else:
        return True
    return False


def is_falling(arr_to_check: []):
    for i in range(len(arr_to_check) - 1):
        if arr_to_check[i] < arr_to_check[i+1]:
            break
    else:
        return True
    return False


def remove_if_multiple(arr_to_del: [], multiple_num: int):
    arr_to_return = [arr_to_del[i] for i in range(len(arr_to_del)) if (i % multiple_num != 0) or (i == 0)]
    return arr_to_return


new_arr = fill_arr()
if not (is_falling(new_arr) or is_raising(new_arr)):
    new_arr = remove_if_multiple(new_arr, 4)
print(new_arr)
