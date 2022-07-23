def fill_matrix():
    while True:
        try:
            size_matrix = int(input("Enter size of your matrix: "))
            if size_matrix <= 0:
                raise ValueError
            matrix = [[] for i in range(size_matrix)]
            for i in range(size_matrix):
                for j in range(len(matrix)):
                    matrix[i].append(int(input("a[" + str(i + 1) + "][" + str(j + 1) + "] = ")))
            return matrix
        except ValueError:
            print("You didn't enter a number, try again from the beginning")


def find_min(matrix):
    min_elements = []
    for i in range(len(matrix)):
        if matrix[i][i] < 0:
            for j in matrix[i]:
                if j < matrix[i][i]:
                    matrix[i][i] = j
            min_elements.append(matrix[i][i])
    if len(min_elements) == 0:
        print("Your matrix doesn`t have a negative element on the main diagonal, try to change your matrix")
        matrix_new = fill_matrix()
        min_elements = find_min(matrix_new)
    return min_elements


def the_biggest_min(min_elements: []):
        max_element = min_elements[0]
        for i in min_elements[1:]:
            if i > max_element:
                max_element = i
        return max_element


while True:
    print("Available commands: \n exit - finish work \n complete task - start doing task \n help - show menu of command")
    command_input = input()
    if command_input == "exit":
        break
    elif command_input == "complete task":
        matrix = fill_matrix()
        min_elements = find_min(matrix)
        print("The biggest minimum element is " + str(the_biggest_min(min_elements)))
        continue
    elif command_input == "help":
        print("Available commands: \n exit - finish work \n complete task - start doing task \n help - show menu of command")
        continue
    else:
        print("There is no such command, please, try again")
