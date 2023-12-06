import aes


# Преобразование массива в строку
def translate_arr_to_str(arr):
    f_str = ''
    for i in range(len(arr)):
        f_str = f_str + str(arr[i])
    return f_str


# Преобразование строки в массив
def translate_str_to_arr_hex(str):
    arr = []
    for l in range(0, len(str), 2):
        arr.append(str[l:l + 2])
    return arr


# Преобразование из 16 в 2
def binary(string):
    binary_text = "{0:0>{1}b}".format(int(string, 16), len(string) * 4)
    return binary_text


# XOR двух строк
def XOR_strs(str1, str2):
    y = int(str1, 2) ^ int(str2, 2)
    ret = bin(y)[2:].zfill(len(str1))
    return ret


# Преобразование из 2 в 16
def hexadecimal(string):
    hexadecimal_text = hex(int(string, 2))[2:]
    return hexadecimal_text


# main ofb
# Входные тексты
Plain_text = ["6BC1BEE22E409F96E93D7E117393172A", "AE2D8A571E03AC9C9EB76FAC45AF8E51",
              "30C81C46A35CE411E5FBC1191A0A52EF", "F69F2445DF4F9B17AD2B417BE66C3710",
              "6BC1BEE22E409F96E93D7E117393172A", "AE2D8A571E03AC9C9EB76FAC45AF8E51"]

# Ключ
Key = "2B7E151628AED2A6ABF7158809CF4F3C"

# Вектор инициализации
IV = "000102030405060708090a0b0c0d0e0f"

# Все ключи
all_round_keys = aes.find_all_round_keys(Key)

# Используется как для шифрования, так и для дешифрования
# Первый входной блок
output_block_1 = aes.encrypt(translate_str_to_arr_hex(IV), all_round_keys)

count = len(Plain_text)


# Операция шифрования (страница 14)
# Принимает сообщение в виде массива шестнадцатеричных строк, а все ключи - в виде массива шестнадцатеричных строк


def ofb_encrypt(plain_text, all_round_keys):
    output_blocks = []
    input_blocks = []
    text_outs = []
    i = 0
    while i < len(plain_text):
        if i == 0:
            input_blocks.append(IV)
            output_blocks.append(translate_arr_to_str(output_block_1))
            text_outs.append(hexadecimal(
                XOR_strs(binary(translate_arr_to_str(output_block_1)), binary(translate_arr_to_str(Plain_text[i])))))
            i += 1
            print("Input_Block 1: ", input_blocks[0])
            print("Output_Block 1: ", output_blocks[0])
            print("Text_In 1: ", plain_text[0])
            print("Text_Out 1: ", text_outs[0])
        if i != 0:
            input_blocks.append(output_blocks[i - 1])
            output_blocks.append(translate_arr_to_str(
                aes.encrypt(translate_str_to_arr_hex(input_blocks[i]), all_round_keys)))
            text_outs.append(hexadecimal(
                XOR_strs(binary(output_blocks[i]), binary(translate_arr_to_str(Plain_text[i])))))
            print("Input_Block", i + 1, ": ", input_blocks[i])
            print("Output_Block", i + 1, ": ", output_blocks[i])
            print("Text_In", i + 1, ": ", plain_text[i])
            print("Text_Out", i + 1, ": ", text_outs[i])
            i += 1

    return text_outs


# Операция дешифрования (страница 14)
# Принимает сообщение в виде массива шестнадцатеричных строк, а все ключи - в виде массива шестнадцатеричных строк
def ofb_decrypt(cipher_text, all_round_keys):
    output_blocks = []
    input_blocks = []
    text_outs = []
    i = 0
    while i < len(cipher_text):
        if i == 0:
            input_blocks.append(IV)
            output_blocks.append(translate_arr_to_str(output_block_1))
            text_outs.append(hexadecimal(
                XOR_strs(binary(translate_arr_to_str(output_block_1)), binary(translate_arr_to_str(cipher_text[i])))))
            i += 1
            print("Input_Block 1: ", input_blocks[0])
            print("Output_Block 1: ", output_blocks[0])
            print("Text_In 1: ", cipher_text[0])
            print("Text_Out 1: ", text_outs[0])
        if i != 0:
            input_blocks.append(output_blocks[i - 1])
            output_blocks.append(translate_arr_to_str(
                aes.encrypt(translate_str_to_arr_hex(input_blocks[i]), all_round_keys)))
            text_outs.append(hexadecimal(
                XOR_strs(binary(output_blocks[i]), binary(translate_arr_to_str(cipher_text[i])))))
            print("Input_Block", i + 1, ": ", input_blocks[i])
            print("Output_Block", i + 1, ": ", output_blocks[i])
            print("Text_In", i + 1, ": ", cipher_text[i])
            print("Text_Out", i + 1, ": ", text_outs[i])
            i += 1

    return text_outs


CIPHERTEXT = ofb_encrypt(Plain_text, all_round_keys)
print(ofb_encrypt(Plain_text, all_round_keys))

print(ofb_decrypt(CIPHERTEXT, all_round_keys))
