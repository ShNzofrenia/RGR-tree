class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
def exp(x, terms=10):
    result = 0
    for n in range(terms):
        result += x ** n / factorial(n)
    return result
def print_tree(root, prefix="", is_left=True):
    if root is None:
        return
    print(prefix, end="")
    print("|-- " if is_left else "`-- ", end="")
    print(root.value)
    print_tree(root.left, prefix + ("|   " if is_left else "    "), True)
    print_tree(root.right, prefix + ("|   " if is_left else "    "), False)
def round(n):
    if n - int(n) < 0.5:
        return int(n)
    else:
        return int(n) + 1
def defuzzification(min,max,x,gaus):
    num = 0
    denom = 0
    for x in range(min + 1, max):
        num += x * gaus
        denom += gaus
    return round(num / denom)
def gauss_function(mean, sigma):
    min = mean
    max = sigma
    for x in range(min + 1, max):
        tmp = 4 * (max - x) * (x - min)
        gaus = exp((tmp - (max - min) * (max - min)) / tmp)
    return defuzzification(min,max,x,gaus)
def generate_fuzzy_number(mean, sigma):
    return gauss_function(mean, sigma)
def generate_fuzzy_binary_tree(file_path):
    fuzzy_numbers = []
    with open(file_path, 'r') as file:
        for line in file:
            mean, sigma = map(int, line.strip().split())
            fuzzy_numbers.append(generate_fuzzy_number(mean, sigma))
    root = Node((fuzzy_numbers[0])+1)
    for i in range(1, len(fuzzy_numbers)):
        insert_node(root,(fuzzy_numbers[i]))
    return root
def insert_node(root, data):
    if root is None:
        root = Node(data)
    else:
        if data < root.value:
            if root.left is None:
                root.left = Node(data)
            else:
                insert_node(root.left, data)
        else:
            if root.right is None:
                root.right = Node(data)
            else:
                insert_node(root.right, data)
def delete_node(root, value):
    if root is None:
        return root
    if value < root.value:
        root.left = delete_node(root.left, value)
    elif value > root.value:
        root.right = delete_node(root.right, value)
    else:
        if root.left is None:
            temp = root.right
            root = None
            return temp
        elif root.right is None:
            temp = root.left
            root = None
            return temp
        temp = find_min_node(root.right)
        root.value = temp.value
        root.right = delete_node(root.right, temp.value)
    return root
def find_min_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current
file_path = "fuzzy_numbers.txt"
fuzzy_values = []
def delete_line_from_file(file_path, value_to_delete):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if value_to_delete not in line:
                lines.append(line)
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)
with open(file_path, 'r') as file:
    lines = file.readlines()
    if len(lines) < 7:
        print("Ошибка: Количество входных данных должно быть больше 7.")
    else:
        try:
            for line in lines:
                mean, sigma = map(int, line.strip().split())
                fuzzy_values.append((mean, sigma))
        except ValueError:
            print("Ошибка: Все входные данные должны быть числами.")
            exit()

if len(fuzzy_values) >= 7:
    print("\nНечеткие числа:")
    for mean, sigma in fuzzy_values:
        fuzzy_number = generate_fuzzy_number(mean, sigma)
        print(f"Первое значение: {mean} | Второе значение: {sigma} ")

    root = generate_fuzzy_binary_tree(file_path)
    while root is not None:
        print("\nСгенерированное бинарное дерево:")
        print_tree(root)
        valuedel = input("Введите значение узла для удаления или введите 'exit' для завершения: ")
        if valuedel.lower() == 'exit':
            break
        mean1, sigma1 = map(int, valuedel.strip().split())
        value_to_delete = generate_fuzzy_number(mean1, sigma1)
        if value_to_delete==7: value_to_delete+=1
        try:
            value_to_delete = int(value_to_delete)
            root = delete_node(root, value_to_delete)
            print(f"Бинарное дерево после удаления узла со значением {value_to_delete}:")
        except ValueError:
            print("Ошибка: Введите целочисленное значение или 'exit' для завершения.")

    print("Удаление узлов завершено или введен триггер 'exit'.")