from analyser import Analyser

def main():
    # exp = input("Выражение: ")
    exp = "(a & b) -> (c | !a)"
    # exp = "(a & b) | ((c -> (!d)) | e)"
    # exp = "!(a~b)" 
    # exp = "a | !a"
    # exp = "(a&b)|((!b)&c)"
    # exp = "(!b & c) | (a & b)"
    analyser = Analyser()
    analyser.execute(exp)

if __name__ == "__main__":
    main()