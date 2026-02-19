import re

print("===============================================")
print("Nombre: Jose Rossa")
print("Carnet: 0909-23-8514")
print("Curso: Compiladores")
print("Tarea 1")
print("===============================================\n")


KEYWORDS = {"if", "let"}
TYPES = {"int"}

SPECS = [
    ("WS", r"[ \t]+"),
    ("NL", r"\n"),

    ("STRING_LITERAL", r'"([^"\\]|\\.)*"'),
    ("INT_LITERAL", r"\d+"),

    ("LE_OP", r"<="),
    ("NE_OP", r"!="),
    ("EQ_OP", r"=="),
    ("AND_OP", r"&&"),

    ("ASSIGN_OP", r"="),
    ("PLUS_OP", r"\+"),
    ("COLON", r":"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SEMICOLON", r";"),

    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("MISMATCH", r"."),
]

MASTER = re.compile("|".join(f"(?P<{n}>{p})" for n, p in SPECS))


def tokenize(code: str):
    tokens = []
    line, col = 1, 1

    for m in MASTER.finditer(code):
        kind = m.lastgroup
        lex = m.group()

        if kind == "WS":
            col += len(lex)
            continue

        if kind == "NL":
            line += 1
            col = 1
            continue

        if kind == "ID":
            if lex in KEYWORDS:
                kind = "KEYWORD"
            elif lex in TYPES:
                kind = "TYPE"

        if kind == "MISMATCH":
            raise SyntaxError(f"Error léxico: carácter inesperado '{lex}' en línea {line}, columna {col}.")

        tokens.append((lex, kind, line, col))
        col += len(lex)

    return tokens


def print_list(tokens):
    for i, (lex, kind, *_pos) in enumerate(tokens, 1):
        print(f"{i}. {lex} -> {kind}")


def ejercicio_1():
    code = "let x:int = 25;"
    print("EJERCICIO 1")
    print("Entrada:", code)
    print("\n1) Liste todos los tokens en orden:")
    print_list(tokenize(code))
    print("\n2) Indique el tipo de cada token: (ya aparece en la lista)")
    print("\n-----------------------------------------------\n")


def ejercicio_2():
    code = "if iffy let letter"
    print("EJERCICIO 2")
    print("Entrada:", code)

    print("\n1) Clasifique cada palabra como KEYWORD o ID:")
    for w in code.split():
        t = tokenize(w)[0]
        cls = "KEYWORD" if t[1] == "KEYWORD" else "ID"
        print(f"- {w} -> {cls}")

    print("\n2) Justifique brevemente cada decisión:")
    print("- if -> KEYWORD porque es palabra reservada.")
    print("- iffy -> ID porque no es exactamente 'if'.")
    print("- let -> KEYWORD porque es palabra reservada.")
    print("- letter -> ID porque no es palabra reservada.")

    print("\n-----------------------------------------------\n")


def ejercicio_3():
    code = "total = price + 10;"
    toks = tokenize(code)

    ids = [lex for (lex, kind, *_ ) in toks if kind == "ID"]
    lits = [lex for (lex, kind, *_ ) in toks if kind in ("INT_LITERAL", "STRING_LITERAL")]
    ops = [lex for (lex, kind, *_ ) in toks if kind.endswith("_OP")]
    syms = [lex for (lex, kind, *_ ) in toks if kind in ("COLON", "LPAREN", "RPAREN", "SEMICOLON")]

    print("EJERCICIO 3")
    print("Entrada:", code)

    print("\nIdentificadores:", ", ".join(ids))
    print("Literales:", ", ".join(lits))
    print("Operadores:", ", ".join(ops))
    print("Símbolos:", ", ".join(syms))
    print("(No interpreto significado, solo clasifico tipos de token.)")

    print("\n-----------------------------------------------\n")


def ejercicio_4():
    code = "x==y"
    print("EJERCICIO 4")
    print("Entrada:", code)

    print("\n1) Liste los tokens correctos:")
    print_list(tokenize(code))

    print("\n2) Error de un lexer mal diseñado:")
    print("Podría dividir '==' en '=' y '=' como dos tokens separados.")

    print("\n3) Cómo la regla maximal munch evita ese error:")
    print("El lexer toma el token más largo posible, entonces reconoce '==' completo.")

    print("\n-----------------------------------------------\n")


def ejercicio_5():
    code = "let\nx\n=\n10\n;\n"
    print("EJERCICIO 5")
    print("Entrada:")
    print(code)

    print("1) Liste los tokens generados:")
    print_list(tokenize(code))

    print("\n2) Por qué los saltos de línea no generan tokens:")
    print("Porque el lexer los trata como espacios en blanco (whitespace).")

    print("\n3) Qué información sí debe conservar el lexer:")
    print("Debe guardar línea y columna para reportar errores.")

    print("\n-----------------------------------------------\n")


def ejercicio_6():
    code = 'if (a <= 10 && b != 20) print("ok");'
    toks = tokenize(code)

    comp_ops = [lex for (lex, _kind, *_ ) in toks if lex in ("<=", "&&", "!=", "==")]

    print("EJERCICIO 6")
    print("Entrada:", code)

    print("\nListe los tokens en orden:")
    print_list(toks)

    print("\nOperadores compuestos encontrados:")
    print(", ".join(comp_ops))

    print("\nPor qué && no se tokeniza como dos &:")
    print("Porque '&&' es un operador completo y es más largo,")
    print("y el lexer siempre toma el token más largo posible.")

    print("\n-----------------------------------------------\n")


def ejercicio_7():
    code = "let x:int = 10 $ 5;"
    print("EJERCICIO 7")
    print("Entrada:", code)

    print("\nIdentifique el error léxico:")
    print("El símbolo '$' no está definido como token válido.")

    print("\nIndique en qué token ocurre:")
    print("Ocurre cuando el lexer encuentra '$'.")

    print("\nMensaje de error que debería producir el lexer:")
    try:
        tokenize(code)
    except SyntaxError as e:
        print(e)

    print("\n-----------------------------------------------\n")


def main():
    ejercicio_1()
    ejercicio_2()
    ejercicio_3()
    ejercicio_4()
    ejercicio_5()
    ejercicio_6()
    ejercicio_7()


if __name__ == "__main__":
    main()
