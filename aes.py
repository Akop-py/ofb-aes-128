from copy import copy

# Кол-во раундов
ROUND = 10

# Длина матрицы
WORD_LENGTH = 4

#  Наиболее часто используемые S_BOX
S_BOX = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

#  Наиболее часто используемые INVERSE_S_BOX
INVERSE_S_BOX = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

# R_CON используется для Key Expansion
R_CON = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)


# Сдвиг влево каждого элмента массива
def left_shift(arr):
    temp = arr[0]
    for i in range(len(arr) - 1):
        arr[i] = arr[i + 1]
    arr[len(arr) - 1] = temp
    return arr


# print(left_shift(['1', '5', '9', 'd']))
# Ввыод ['5', '9', 'd', '1']


# Сдвиг вправо каждого элемента массива
def right_sift(arr):
    temp = arr[WORD_LENGTH - 1]
    i = len(arr) - 1
    while i > 0:
        arr[i] = arr[i - 1]
        i = i - 1
    arr[0] = temp
    return arr


# print(right_sift(['1', '5', '9', 'd']))
# Ввыод ['d', '1', '5', '9']


# На вход подается значение основного ключа (страница 20)
# На выходе получеам массив 11 ключей
# Первый ключ является основным ключом, а остальные - сгенерированными ключами
def find_all_round_keys(main_key_val):
    # Создание массива из 44 [0,0,0,0]
    w = [[0 for x in range(WORD_LENGTH)] for y in range(44)]

    temp_arr = []

    # Добавление в временный массив основной ключ по 2 значения ['00', '01' ...
    for l in range(0, len(main_key_val), 2):
        temp_arr.append(main_key_val[l:l + 2])

    # Заполнение по 4 строчки матрицы w с временного массива temp
    for i in range(WORD_LENGTH):
        for j in range(WORD_LENGTH):
            w[i][j] = int(temp_arr[(i * WORD_LENGTH) + j], 16)

    temp_arr = []

    round_num = 0
    for word_num in range(WORD_LENGTH, WORD_LENGTH * (ROUND + 1)):

        if word_num % WORD_LENGTH == 0:
            round_num = round_num + 1
            temp_w = [0, 0, 0, 0]
            for i in range(4):
                temp_w[i] = w[word_num - 1][i]
            temp_w = left_shift(temp_w)

            s_box_arr = []

            for i in range(WORD_LENGTH):
                s_box_index = int(temp_w[i])
                s_box_arr.append(S_BOX[s_box_index])

            round_cont_arr = [0, 0, 0, 0]
            round_cont_arr[0] = round_cont_arr[0] + R_CON[round_num]
            for i in range(WORD_LENGTH):
                s_box_arr[i] = s_box_arr[i] ^ round_cont_arr[i]

            for i in range(WORD_LENGTH):
                int_val = int(w[word_num - 4][i])
                w[word_num][i] = int_val ^ s_box_arr[i]

        else:
            for i in range(WORD_LENGTH):
                int_val_minus_1 = int(w[word_num - 1][i])
                int_val_minus_4 = int(w[word_num - 4][i])
                w[word_num][i] = int_val_minus_1 ^ int_val_minus_4

    temp_round_keys_hex = []

    for i in range(WORD_LENGTH * (ROUND + 1)):
        for j in range(WORD_LENGTH):
            temp_round_keys_hex.append("{:02x}".format(w[i][j]))

    round_keys_in_hex = [temp_round_keys_hex[i * (WORD_LENGTH * WORD_LENGTH):(i + 1) * (WORD_LENGTH * WORD_LENGTH)]
                         for i in range(
            (len(temp_round_keys_hex) + (WORD_LENGTH * WORD_LENGTH) - 1) // (WORD_LENGTH * WORD_LENGTH))]

    return round_keys_in_hex


# print(find_all_round_keys("000102030405060708090a0b0c0d0e0f"))
# Вывод:
# [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f'],
# ['d6', 'aa', '74', 'fd', 'd2', 'af', '72', 'fa', 'da', 'a6', '78', 'f1', 'd6', 'ab', '76', 'fe'],
# ['b6', '92', 'cf', '0b', '64', '3d', 'bd', 'f1', 'be', '9b', 'c5', '00', '68', '30', 'b3', 'fe'],
# ['b6', 'ff', '74', '4e', 'd2', 'c2', 'c9', 'bf', '6c', '59', '0c', 'bf', '04', '69', 'bf', '41'],
# ['47', 'f7', 'f7', 'bc', '95', '35', '3e', '03', 'f9', '6c', '32', 'bc', 'fd', '05', '8d', 'fd'],
# ['3c', 'aa', 'a3', 'e8', 'a9', '9f', '9d', 'eb', '50', 'f3', 'af', '57', 'ad', 'f6', '22', 'aa'],
# ['5e', '39', '0f', '7d', 'f7', 'a6', '92', '96', 'a7', '55', '3d', 'c1', '0a', 'a3', '1f', '6b'],
# ['14', 'f9', '70', '1a', 'e3', '5f', 'e2', '8c', '44', '0a', 'df', '4d', '4e', 'a9', 'c0', '26'],
# ['47', '43', '87', '35', 'a4', '1c', '65', 'b9', 'e0', '16', 'ba', 'f4', 'ae', 'bf', '7a', 'd2'],
# ['54', '99', '32', 'd1', 'f0', '85', '57', '68', '10', '93', 'ed', '9c', 'be', '2c', '97', '4e'],
# ['13', '11', '1d', '7f', 'e3', '94', '4a', '17', 'f3', '07', 'a7', '8b', '4d', '2b', '30', 'c5']]

# На вход получаем шестнадцатеричный строковый массив и генерируем матрицу 4x4
def generate_4x4_matrix(hex_string):
    hex_string_arr = [hex_string[i:i + WORD_LENGTH] for i in range(0, len(hex_string), WORD_LENGTH)]
    matrix_4x4 = [['' for x in range(WORD_LENGTH)] for y in range(WORD_LENGTH)]
    for i in range(WORD_LENGTH):
        for j in range(WORD_LENGTH):
            matrix_4x4[i][j] = hex_string_arr[j][i]

    return matrix_4x4


# print(generate_4x4_matrix("0123456789abcdef"))
# Ввыод [['0', '4', '8', 'c'],
#       ['1', '5', '9', 'd'],
#       ['2', '6', 'a', 'e'],
#       ['3', '7', 'b', 'f']]


# На вход получаем целочисленный массив и преобразовываем в шестнадцатеричный
def make_int_arr_to_hex(int_arr):
    hex_arr = ['' for x in range(len(int_arr))]
    for i in range(len(int_arr)):
        hex_arr[i] = "{:02x}".format(int_arr[i])
    return hex_arr


# arr = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# print(make_int_arr_to_hex(arr))
# Вывод ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']

# На вход принимаем две шестнадцатеричные строки матрицы 4x4
# Преобразовываем матрицу в целочисленную версию матрицы и выполняем XOR для них
# Преобразовываем результаты XOR в шестнадцатеричную строку матрицы 4x4
def add_round_key(m1_hex, m2_hex):
    matrix_4x4 = [['' for x in range(WORD_LENGTH)] for y in range(WORD_LENGTH)]

    for i in range(WORD_LENGTH):
        for j in range(WORD_LENGTH):
            val_1 = int(m1_hex[i][j], 16)
            val_2 = int(m2_hex[i][j], 16)
            res = val_1 ^ val_2
            matrix_4x4[i][j] = "{:02x}".format(res)

    return matrix_4x4


# arr_1 = [['0', '4', '8', 'c'], ['1', '5', '9', 'd'], ['2', '6', 'a', 'e'], ['3', '7', 'b', 'f']]
# arr_2 = [['1', '1', '8', 'c'], ['1', '5', '9', 'd'], ['2', '6', 'a', 'e'], ['3', '7', 'b', 'f']]
# print(add_round_key(arr_1, arr_2))
# Ввыод [['01', '05', '00', '00'],
#       ['00', '00', '00', '00'],
#       ['00', '00', '00', '00'],
#       ['00', '00', '00', '00']]


# Используется как для шифрования, так и для дешифрования
# Если normal_or_inv имеет значение True, то это для шифрования, если False, то это для дешифрования
# Для шифрования устанваливаем значение матрицы со значением S_BOX, для дешифрования INVERSE_S_BOX
def substitute_bytes(matrix, normal_or_inv):
    for i in range(WORD_LENGTH):
        for j in range(WORD_LENGTH):
            int_val = int(matrix[i][j], 16)
            if normal_or_inv:
                s_box_val_int = S_BOX[int_val]
            else:
                s_box_val_int = INVERSE_S_BOX[int_val]
            s_box_val_hex = "{:02x}".format(s_box_val_int)
            matrix[i][j] = s_box_val_hex
    return matrix


# arr_1 = [['0', '4', '8', 'c'], ['1', '5', '9', 'd'], ['2', '6', 'a', 'e'], ['3', '7', 'b', 'f']]
# print(substitute_bytes(arr_1, True))
# Ввыод [['63', 'f2', '30', 'fe'],
#        ['7c', '6b', '01', 'd7'],
#        ['77', '6f', '67', 'ab'],
#        ['7b', 'c5', '2b', '76']]


# Используется для шифрования
# Сдвигается влево от первой строки на  1
# Сдвигается влево от второй строки на  2
# Сдвигается влево от третьей строки на  3
def shift_row(matrix):
    matrix[1] = left_shift(matrix[1])

    matrix[2] = left_shift(matrix[2])
    matrix[2] = left_shift(matrix[2])

    matrix[3] = left_shift(matrix[3])
    matrix[3] = left_shift(matrix[3])
    matrix[3] = left_shift(matrix[3])

    return matrix


# arr_1 = [['0', '4', '8', 'c'], ['1', '5', '9', 'd'], ['2', '6', 'a', 'e'], ['3', '7', 'b', 'f']]
# print(shift_row(arr_1))
# Вывод [['0', '4', '8', 'c'],
#       ['5', '9', 'd', '1'],
#       ['a', 'e', '2', '6'],
#       ['f', '3', '7', 'b']]

# Используется для расшифровки
# Сдвигает вправо первую строку на  1
# Сдвигает вправо вторую строку на  2
# Сдвигает вправо третью строку на  3
def shift_row_inv(matrix):
    matrix[1] = right_sift(matrix[1])

    matrix[2] = right_sift(matrix[2])
    matrix[2] = right_sift(matrix[2])

    matrix[3] = right_sift(matrix[3])
    matrix[3] = right_sift(matrix[3])
    matrix[3] = right_sift(matrix[3])
    return matrix


# На вход принимаем шестнадцатеричный строковый массив и преобразовываем в целочисленный
def make_matrix_int(matrix):
    int_matrix = [[0 for x in range(WORD_LENGTH)] for y in range(WORD_LENGTH)]
    for i in range(WORD_LENGTH):
        for j in range(WORD_LENGTH):
            int_matrix[i][j] = int(matrix[i][j], 16)
    return int_matrix


# arr_1 = [['0', '4', '8', 'c'], ['1', '5', '9', 'd'], ['2', '6', 'a', 'e'], ['3', '7', 'b', 'f']]
# print(make_matrix_int(arr_1))
# Вывод [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]]

# Умножение Галуа
# x^8 + x^4 + x^3 + x + 1
def galois_multiplication(a, b):
    p = 0
    hi_bit_set = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set == 0x80:
            a ^= 0x11b
        b >>= 1
    return p % 256


# print(galois_multiplication(15,15))
# Вывод 85

# Используется для шифрования
# Каждый столбец и постоянные числа передаются в функцию умножения Галуа (страница 18)
def mix_column(column):
    temp = copy(column)
    column[0] = galois_multiplication(temp[0], 2) ^ galois_multiplication(temp[3], 1) ^ \
                galois_multiplication(temp[2], 1) ^ galois_multiplication(temp[1], 3)
    column[1] = galois_multiplication(temp[1], 2) ^ galois_multiplication(temp[0], 1) ^ \
                galois_multiplication(temp[3], 1) ^ galois_multiplication(temp[2], 3)
    column[2] = galois_multiplication(temp[2], 2) ^ galois_multiplication(temp[1], 1) ^ \
                galois_multiplication(temp[0], 1) ^ galois_multiplication(temp[3], 3)
    column[3] = galois_multiplication(temp[3], 2) ^ galois_multiplication(temp[2], 1) ^ \
                galois_multiplication(temp[1], 1) ^ galois_multiplication(temp[0], 3)

    return column


# column_1 = [0, 4, 8, 12]
# print(mix_column(column_1))
# Вывод [8, 28, 0, 20]

# Используется для расшифровки
# Каждый столбец и постоянные числа передаются в функцию умножения Галуа
def mix_column_inv(column):
    temp = copy(column)
    column[0] = galois_multiplication(temp[0], 14) ^ galois_multiplication(temp[3], 9) ^ \
                galois_multiplication(temp[2], 13) ^ galois_multiplication(temp[1], 11)
    column[1] = galois_multiplication(temp[1], 14) ^ galois_multiplication(temp[0], 9) ^ \
                galois_multiplication(temp[3], 13) ^ galois_multiplication(temp[2], 11)
    column[2] = galois_multiplication(temp[2], 14) ^ galois_multiplication(temp[1], 9) ^ \
                galois_multiplication(temp[0], 13) ^ galois_multiplication(temp[3], 11)
    column[3] = galois_multiplication(temp[3], 14) ^ galois_multiplication(temp[2], 9) ^ \
                galois_multiplication(temp[1], 13) ^ galois_multiplication(temp[0], 11)

    return column


# column_1 = [0, 4, 8, 12]
# print(mix_column_inv(column_1))
# Вывод [40, 60, 32, 52]

# Используется как для шифрования, так и для дешифрования
# Если normal_or_inv имеет значение True, то это для шифрования, если False, то это для дешифрования
# Принимает шестнадцатеричную строковую матрицу и преобразует ее в версию на основе столбцов и строк целочисл. матрицы
# Для шифрования он отправляет каждую строку целочисленной матрицы в mix_column
# Для расшифровки он отправляет каждую строку целочисленной матрицы в mix_column_inv
def mix_columns(matrix, normal_or_inv):
    int_matrix = make_matrix_int(matrix)
    col_based = [[0 for x in range(WORD_LENGTH)] for y in range(WORD_LENGTH)]

    for i in range(WORD_LENGTH):
        for j in range(WORD_LENGTH):
            col_based[i][j] = int_matrix[j][i]

    if normal_or_inv:
        for i in range(WORD_LENGTH):
            mix_column(col_based[i])

    else:
        for i in range(WORD_LENGTH):
            mix_column_inv(col_based[i])

    for i in range(WORD_LENGTH):
        for j in range(WORD_LENGTH):
            matrix[i][j] = "{:02x}".format(col_based[j][i])
            int_matrix[i][j] = col_based[j][i]

    return int_matrix


# arr_1 = [['0', '4', '8', 'c'], ['1', '5', '9', 'd'], ['2', '6', 'a', 'e'], ['3', '7', 'b', 'f']]
# print(mix_columns(arr_1, True))
# Вывод [[2, 6, 10, 14],
#       [7, 3, 15, 11],
#       [0, 4, 8, 12],
#       [5, 1, 13, 9]]


# Операция шифрования (страница 15)
# Принимает сообщение в виде массива шестнадцатеричных строк, а все ключи - в виде массива шестнадцатеричных строк
# В этом шифровании есть 4 основные операции
# 1) Байты подстановки, которые являются substitute_bytes (normal_or_inv должно быть True для шифрования)
# 2) Строка сдвига, которая является shift_row
# 3) Смешивание столбец, mix_columns (normal_or_inv должно быть True для шифрования)
# 4) Добавление ключа, который add_round_key
def encrypt(text_hex, all_round_keys):
    state_matrix = generate_4x4_matrix(text_hex)
    #print(state_matrix)
    round_N_matrix = generate_4x4_matrix(all_round_keys[0])
    #print(round_N_matrix)
    current_matrix = add_round_key(state_matrix, round_N_matrix)
    #print(current_matrix)

    for i in range(1, ROUND):
        substitute_bytes(current_matrix, True)
       # print(substitute_bytes(current_matrix, True))
        shift_row(current_matrix)
      #  print(shift_row(current_matrix))
        mix_columns(current_matrix, True)
      #  print(mix_columns(current_matrix, True))
        current_matrix = add_round_key(current_matrix, generate_4x4_matrix(all_round_keys[i]))
      #  print(current_matrix)

    substitute_bytes(current_matrix, True)
    shift_row(current_matrix)
    cipher_text_matrix = add_round_key(current_matrix, generate_4x4_matrix(all_round_keys[10]))

    cipher_text = []
    for i in range(WORD_LENGTH):
        for j in range(WORD_LENGTH):
            cipher_text.append(cipher_text_matrix[j][i])
            #print(cipher_text)

    return cipher_text


# Пример из 36 страницы
# text_1 = ["00", "11", "22", "33", "44", "55", "66", "77", "88", "99", "aa", "bb", "cc", "dd", "ee", "ff"]
# key = "000102030405060708090a0b0c0d0e0f"
# all_keys = find_all_round_keys(key)
# print(encrypt(text_1, all_keys))
# text_2 = encrypt(text_1, all_keys)


# Это операция дешифрования (страница 21)
# Принимает зашифрованное сообщение в виде массива шестнадцатеричных строк и все ключи
# В этом шифровании есть 4 основные операции
# 1) Обратная замена байтов substitute_bytes (normal_or_inv должно быть False для расшифровки)
# 2) Обратная смена строк  shift_row_inv
# 3) Смешивание столбец mix_columns (normal_or_inv должен быть False для расшифровки)
# 4) Добавление ключа, который add_round_key
def decryption(cipher_text, all_round_keys):
    state_matrix = generate_4x4_matrix(cipher_text)
    round_N_matrix = generate_4x4_matrix(all_round_keys[10])

    current_matrix = add_round_key(state_matrix, round_N_matrix)
    shift_row_inv(current_matrix)
    substitute_bytes(current_matrix, False)

    i = 9
    while i > 0:
        current_matrix = add_round_key(current_matrix, generate_4x4_matrix(all_round_keys[i]))
        mix_columns(current_matrix, False)
        shift_row_inv(current_matrix)
        substitute_bytes(current_matrix, False)
        i = i - 1

    plain_text_matrix = add_round_key(current_matrix, generate_4x4_matrix(all_round_keys[0]))

    plain_text = []
    for i in range(WORD_LENGTH):
        for j in range(WORD_LENGTH):
            plain_text.append(plain_text_matrix[j][i])

    return plain_text

# print(decryption(text_2,all_keys))
