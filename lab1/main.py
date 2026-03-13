from src.integercalculator import (int_to_direct_binary, bin_to_str, int_to_reverse_binary, 
    int_to_additional_binary, binary_add, direct_binary_to_int,
    binary_sub, binary_div, additional_binary_to_int, binary_comp, fixed_point_to_decimal
    )
from src.ieee7542008 import (
    from_float_to_ieee, from_ieee_to_float, add_ieee, sub_ieee,
    comp_ieee, div_ieee
)

from src.bcd5421 import (
    int_to_5421, add_5421_bcd, bcd_5421_to_int
)


def main():
    while True:
            print_menu()
            user_choice = input("Выбор: ")
            match user_choice:
                case "1":
                    a = int(input("Введите число: "))
                    print(f"Прямой код{bin_to_str(int_to_direct_binary(a))}")
                    print(f"Обратный код{bin_to_str(int_to_reverse_binary(a))}")
                    print(f"Дополнительный код{bin_to_str(int_to_additional_binary(a))}")
                case "2":
                    a = int(input("a = "))
                    b = int(input("b = "))
                    diff = binary_add(int_to_additional_binary(a), int_to_additional_binary(b))
                    print(f"a + b = {bin_to_str(diff)} (bin)")
                    print(f"a + b = {additional_binary_to_int(diff)} (dec)")
                case "3":
                    a = int(input("a = "))
                    b = int(input("b = "))
                    diff = binary_sub(int_to_additional_binary(a), int_to_additional_binary(b))
                    print(f"a - b = {bin_to_str(diff)} (bin)")
                    print(f"a - b = {additional_binary_to_int(diff)} (dec)")
                case "4":
                    a = int(input("a = "))
                    b = int(input("b = "))
                    comp = binary_comp(int_to_direct_binary(a), int_to_direct_binary(b))
                    print(f"a * b = {bin_to_str(comp)} (bin)")
                    print(f"a * b = {direct_binary_to_int(comp)} (dec)")
                case "5":
                    a = int(input("a = "))
                    b = int(input("b = "))
                    if b == 0:
                        print("Деление на ноль невозможно!!!")
                        continue
                    div = binary_div(int_to_direct_binary(a), int_to_direct_binary(b))
                    print(f"a / b = {bin_to_str(div)} (bin)")
                    print(f"a / b = {fixed_point_to_decimal(div)} (dec)")
                case "6":
                    a = float(input("a = "))
                    b = float(input("b = "))
                    a_ieee = from_float_to_ieee(a)
                    print(f"{bin_to_str(a_ieee)} (IEEE-754-2008)")
                    b_ieee = from_float_to_ieee(b)
                    print(f"{bin_to_str(b_ieee)} (IEEE-754-2008)")
                    diff = add_ieee(a_ieee, b_ieee)
                    print(f"a + b = {bin_to_str(diff)} (IEEE-754-2008)")
                    print(f"a + b = {from_ieee_to_float(diff)} (dec)")
                case "7":
                    a = float(input("a = "))
                    b = float(input("b = "))
                    a_ieee = from_float_to_ieee(a)
                    print(f"{bin_to_str(a_ieee)} (IEEE-754-2008)")
                    b_ieee = from_float_to_ieee(b)
                    print(f"{bin_to_str(b_ieee)} (IEEE-754-2008)")
                    diff = sub_ieee(a_ieee, b_ieee)
                    print(f"a - b = {bin_to_str(diff)} (IEEE-754-2008)")
                    print(f"a - b = {from_ieee_to_float(diff)} (dec)")
                case "8":
                    a = float(input("a = "))
                    b = float(input("b = "))
                    a_ieee = from_float_to_ieee(a)
                    print(f"{bin_to_str(a_ieee)} (IEEE-754-2008)")
                    b_ieee = from_float_to_ieee(b)
                    print(f"{bin_to_str(b_ieee)} (IEEE-754-2008)")
                    comp = comp_ieee(a_ieee, b_ieee)
                    print(f"a * b = {bin_to_str(comp)} (IEEE-754-2008)")
                    print(f"a * b = {from_ieee_to_float(comp)} (dec)")
                case "9":
                    a = float(input("a = "))
                    b = float(input("b = "))
                    if b == 0:
                        print("Деление на ноль невозможно!!!")
                        continue
                    a_ieee = from_float_to_ieee(a)
                    print(f"{bin_to_str(a_ieee)} (IEEE-754-2008)")
                    b_ieee = from_float_to_ieee(b)
                    print(f"{bin_to_str(b_ieee)} (IEEE-754-2008)")
                    div = div_ieee(a_ieee, b_ieee)
                    print(f"a / b = {bin_to_str(div)} (IEEE-754-2008)")
                    print(f"a / b = {from_ieee_to_float(div)} (dec)")
                case "10":
                    a = int(input("a = "))
                    b = int(input("b = "))
                    a_bcd = int_to_5421(a)
                    print(f"{bin_to_str(a_bcd)} (5421 BCD)")
                    b_bcd = int_to_5421(b)
                    sum_bcd = add_5421_bcd(a_bcd, b_bcd)
                    print(f"a + b = {bin_to_str(sum_bcd)} (5421 BCD)")
                    print(f"a + b = {bcd_5421_to_int(sum_bcd)} (dec)")
                case "0":
                    print("Выход из программы...")
                    break
                case _:
                    print("Неверный выбор.")

def print_menu():
    print("\n--- Меню ---")
    print("1  - Перевод числа из десятичного формата в двоичный в прямом, дополнительном и обратном кодах")
    print("2  - Сложение в дополнительном коде")
    print("3  - Вычитание в дополнительном коде")
    print("4  - Произведение в прямом коде")
    print("5  - Деление в прямом коде")
    print("6  - Сложение чисел с плавающей точкой по стандарту IEEE-754-2008")
    print("7  - Вычитание чисел с плавающей точкой по стандарту IEEE-754-2008")
    print("8  - Произведение чисел с плавающей точкой по стандарту IEEE-754-2008")
    print("9  - Деление чисел с плавающей точкой по стандарту IEEE-754-2008")
    print("10 - Сложение чисел в двоично-десятичный коде (5421 BCD):")
    print("0 - Выход")

if __name__ == "__main__":
    main()
