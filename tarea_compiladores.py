import re

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
    print("==================================================")
    print("EJERCICIO 1")
    print("Entrada:", code)
    toks = tokenize(code)
    print("\n1) Liste todos los tokens en orden:")
    print_list(toks)
    print("\n2) Indique el tipo de cada token: (ya va en la misma lista)")
    print("==================================================\n")


def ejercicio_2():
    code = "if iffy let letter"
    print("==================================================")
    print("EJERCICIO 2")
    print("Entrada:", code)

    print("\n1) Clasifique cada palabra como KEYWORD o ID:")
    for w in code.split():
        t = tokenize(w)[0]
        cls = "KEYWORD" if t[1] == "KEYWORD" else "ID"
        print(f"- {w} -> {cls}")

    print("\n2) Justifique brevemente cada decisión:")
    print("- if -> KEYWORD porque es palabra reservada.")
    print("- iffy -> ID porque no es exactamente 'if', solo se parece.")
    print("- let -> KEYWORD porque es palabra reservada.")
    print("- letter -> ID porque no es palabra reservada.")
    print("==================================================\n")


def ejercicio_3():
    code = "total = price + 10;"
    toks = tokenize(code)

    ids = [lex for (lex, kind, *_ ) in toks if kind == "ID"]
    lits = [lex for (lex, kind, *_ ) in toks if kind in ("INT_LITERAL", "STRING_LITERAL")]
    ops = [lex for (lex, kind, *_ ) in toks if kind.endswith("_OP")]
    syms = [lex for (lex, kind, *_ ) in toks if kind in ("COLON", "LPAREN", "RPAREN", "SEMICOLON")]

    print("==================================================")
    print("EJERCICIO 3")
    print("Entrada:", code)

    print("\nIdentifique identificadores, literales, operadores y símbolos:")
    print("Identificadores:", ", ".join(ids) if ids else "—")
    print("Literales:", ", ".join(lits) if lits else "—")
    print("Operadores:", ", ".join(ops) if ops else "—")
    print("Símbolos:", ", ".join(syms) if syms else "—")

    print("\n(No interpreto significado, solo digo qué tipo de token es cada cosa.)")
    print("==================================================\n")


def ejercicio_4():
    code = "x==y"
    toks = tokenize(code)

    print("==================================================")
    print("EJERCICIO 4")
    print("Entrada:", code)

    print("\n1) Liste los tokens correctos:")
    print_list(toks)

    print("\n2) Explique qué error cometería un lexer mal diseñado:")
    print("Un lexer mal hecho podría partir '==' en '=' y '=' como si fueran dos tokens separados.")
    print("Entonces saldría algo como: x, =, =, y (y eso está mal).")

    print("\n3) Explique cómo la regla maximal munch evita ese error:")
    print("Maximal munch es básicamente: 'agarra el token más largo que puedas'.")
    print("Como '==' existe, el lexer lo toma completo y no lo divide en dos '='.")
    print("==================================================\n")


def ejercicio_5():
    code = "let\nx\n=\n10\n;\n"
    toks = tokenize(code)

    print("==================================================")
    print("EJERCICIO 5")
    print("Entrada:")
    print(code)

    print("1) Liste los tokens generados:")
    print_list(toks)

    print("\n2) Explique por qué los saltos de línea no generan tokens:")
    print("Porque el lexer los trata como espacios (whitespace). Sirven para separar, pero no son tokens.")

    print("\n3) Indique qué información sí debe conservar el lexer:")
    print("La línea y columna de cada token, para poder decir exactamente dónde hay errores.")
    print("==================================================\n")


def ejercicio_6():
    code = 'if (a <= 10 && b != 20) print("ok");'
    toks = tokenize(code)

    comp_ops = [lex for (lex, _kind, *_ ) in toks if lex in ("<=", "&&", "!=", "==")]

    print("==================================================")
    print("EJERCICIO 6")
    print("Entrada:", code)

    print("\nListe los tokens en orden:")
    print_list(toks)

    print("\nIdentifique todos los operadores compuestos:")
    print(", ".join(comp_ops) if comp_ops else "—")

    print("\nExplique por qué && no se tokeniza como dos &:")
    print("Porque '&&' es un operador completo y es más largo.")
    print("Con maximal munch el lexer prefiere '&&' en vez de '&' + '&'.")
    print("==================================================\n")


def ejercicio_7():
    code = "let x:int = 10 $ 5;"
    print("==================================================")
    print("EJERCICIO 7")
    print("Entrada:", code)

    print("\nIdentifique el error léxico:")
    print("El símbolo '$' no está definido como token válido en este lenguaje, entonces es error.")

    print("\nIndique en qué token ocurre:")
    print("Ocurre justo cuando el lexer encuentra '$'.")

    print("\nMensaje de error que debería producir el lexer (con línea y columna):")
    try:
        tokenize(code)
        print("No debería llegar aquí.")
    except SyntaxError as e:
        print(e)

    print("==================================================\n")


def main():
    print("TAREA DE COMPILADORES (ANÁLISIS LÉXICO EN PYTHON)\n")
    ejercicio_1()
    ejercicio_2()
    ejercicio_3()
    ejercicio_4()
    ejercicio_5()
    ejercicio_6()
    ejercicio_7()


if __name__ == "__main__":
    main()