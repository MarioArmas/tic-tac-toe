def check_end(tablero):
    # check filas y columnas
    i = 0
    for j in range(3):
        fila = tablero[0+i] + tablero[1+i] + tablero[2+i]
        if fila == "XXX": return "X"
        if fila == "OOO": return "O"

        columna = tablero[0+j] + tablero[3+j] + tablero[6+j]
        if columna == "XXX": return "X"
        if columna == "OOO": return "O"
        i += 3

    # check diagonales
    diagonal1 = tablero[0] + tablero[4] + tablero[8]
    if diagonal1 == "XXX": return "X"
    if diagonal1 == "OOO": return "O"

    diagonal2 = tablero[2] + tablero[4] + tablero[6]
    if diagonal2 == "XXX": return "X"
    if diagonal2 == "OOO": return "O"

    # empate
    movimientos = ""
    for i in tablero:
        movimientos += i
    movimientos = len(movimientos.replace(' ', ''))
    if movimientos == 9: return "Empate"

    return None

def make_move(tablero, player_move, num):
    if not(num >= 1 and num <= 9): return player_move
    num -= 1
    if tablero[num] != " ": return player_move
    if player_move:
        tablero[num] = "X"
        player_move = False
    else:
        tablero[num] = "O"
        player_move = True
    
    return player_move

def mostrar_tablero(tablero):
    print(" " + tablero[0] + " | " + tablero[1] + " | " + tablero[2] + "\n " + tablero[3] + " | " + tablero[4] + " | " + tablero[5] + "\n " + tablero[6] + " | " + tablero[7] + " | " + tablero[8])

def movimientosIA(tablero, primera_jugada, decision): # IA mueve con O
    # ganar si es posible o evitar victoria del rival en 1 movimiento
    text = "OO"
    for w in range(2):
        i = 0
        for j in range(3):
            # filas
            fila = str(tablero[0+i] + tablero[1+i] + tablero[2+i])
            if fila.replace(" ", "") == text:
                if tablero[0+i] == " ": tablero[0+i] = "O"
                if tablero[1+i] == " ": tablero[1+i] = "O"
                if tablero[2+i] == " ": tablero[2+i] = "O"
                return decision
        
            # columnas
            columna = str(tablero[0+j] + tablero[3+j] + tablero[6+j])
            if columna.replace(" ", "") == text:
                if tablero[0+j] == " ": tablero[0+j] = "O"
                if tablero[3+j] == " ": tablero[3+j] = "O"
                if tablero[6+j] == " ": tablero[6+j] = "O"
                return decision
            i += 3

        # diagonales
        diagonal1 = str(tablero[0] + tablero[4] + tablero[8])
        if diagonal1.replace(" ", "") == text:
            if tablero[0] == " ": tablero[0] = "O"
            if tablero[4] == " ": tablero[4] = "O"
            if tablero[8] == " ": tablero[8] = "O"
            return decision

        diagonal2 = str(tablero[2] + tablero[4] + tablero[6])
        if diagonal2.replace(" ", "") == text:
            if tablero[2] == " ": tablero[2] = "O"
            if tablero[4] == " ": tablero[4] = "O"
            if tablero[6] == " ": tablero[6] = "O"
            return decision

        text = "XX"
    
    # movimientos según quien empieza
    num_movimiento = ""
    for casilla in tablero:
        num_movimiento += casilla
    num_movimiento = len(num_movimiento.replace(' ', ''))

    if primera_jugada == "1": persona_juega_primero(tablero, num_movimiento)
    if primera_jugada == "2": decision = maquina_juega_primero(tablero, decision, num_movimiento)
    return decision

def persona_juega_primero(tablero, num_movimiento):
    # primer movimiento
    if num_movimiento == 1 and tablero[4] == " ":
        tablero[4] = "O"
        return
    elif num_movimiento == 1: tablero[6] = "O"; return # REVISAR SI ESTE ELSE ES CORRECTO ##############

    # buscar si en 2 turnos gana el jugador
    movimiento_encontrado = False
    for posible_IA in range(9):
        if movimiento_encontrado: break
        if tablero[posible_IA] == " ": tablero[posible_IA] = "O"
        else: continue
        resultados = ""
        respuesta_correcta = 0
        for posible_player in range(9):
            if movimiento_encontrado: break
            if tablero[posible_player] == " ": tablero[posible_player] = "X"
            else: continue
            for posible_IA_2 in range(9):
                if movimiento_encontrado: break
                if tablero[posible_IA_2] == " ": tablero[posible_IA_2] = "O"
                else: continue
                for posible_player_2 in range(9):
                    if movimiento_encontrado: break
                    if tablero[posible_player_2] == " ": tablero[posible_player_2] = "X"
                    else: continue
                    try: resultados += check_end(tablero)
                    except: pass
                    tablero[posible_player_2] = " "
                
                if "X" in resultados: respuesta_correcta += 1

                tablero[posible_IA_2] = " "
            tablero[posible_player] = " "

        # si se encontró un movimiento en el que no pierde -> romper bucle
        if respuesta_correcta >= 14: movimiento_encontrado = True # El 14 es por patrones segun las veces que sale en el ultimo for una "X"
        else: tablero[posible_IA] = " "

    # movimiento al azar si no hay peligro
    if not(movimiento_encontrado):
        for casilla in range(9):
            if tablero[casilla] == " ":
                tablero[casilla] = "O"
                break

def maquina_juega_primero(tablero, decision, num_movimiento):
    # primer movimiento
    if tablero[6] == " ":
        tablero[6] = "O"
        return decision

    # tercer movimiento
    if num_movimiento == 4:
        if decision == "E": # esquina
            if tablero[0] == " ": tablero[0] = "O"
            if tablero[2] == " ": tablero[2] = "O"
            if tablero[6] == " ": tablero[6] = "O"
            if tablero[8] == " ": tablero[8] = "O"
            return decision

        if decision == "L": # lateral
            tablero[4] = "O"
            return decision

    # segundo movimiento
    if num_movimiento == 2: # centro
        if tablero[4] == "X":
            tablero[2] = "O"
            decision = "C"
            return decision

        if tablero[0] == "X" or tablero[2] == "X" or tablero[6] == "X" or tablero[8] == "X": # esquina
            decision = "E"
            if tablero[0] == " ": tablero[0] = "O"; return decision
            if tablero[2] == " ": tablero[2] = "O"; return decision
            if tablero[6] == " ": tablero[6] = "O"; return decision
            if tablero[8] == " ": tablero[8] = "O"; return decision

        if tablero[1] == "X" or tablero[3] == "X" or tablero[5] == "X" or tablero[7] == "X": # lateral
            if tablero[1] == "X": tablero[0] = "O"
            if tablero[3] == "X": tablero[8] = "O"
            if tablero[5] == "X": tablero[0] = "O"
            if tablero[7] == "X": tablero[0] = "O"
            decision = "L"
            return decision

def main():
    num = 0
    player_move = True
    tablero = [" "," "," "," "," "," "," "," "," "]
    decision = ""

    while True:
        opcion = input("1. Jugar contra otro jugador\n2. Jugar contra la máquina\nPresione cualquier otra tecla para salir\n")

        # jugar PvP
        if opcion == "1":
            while(check_end(tablero) == None):
                try:
                    print("Seleccione un núemro 1-9")
                    if player_move: num = int(input("Player 1: "))
                    else: num = int(input("Player 2: "))
                    player_move = make_move(tablero, player_move, num)
                    mostrar_tablero(tablero)
                except: print("Se esperaba un valor numérico entero")

            print("Winner: " + check_end(tablero))

        # jugar contra la maquina
        elif opcion == "2":
            primer_movimiento = input("1. Jugar primer movimiento\n2. La máquina juega el primer movimiento\n")
            if primer_movimiento != "1" and primer_movimiento != "2": print("Valor ingresado no válido"); continue

            if primer_movimiento == "1": num_int = False
            if primer_movimiento == "2": num_int = True
            while(check_end(tablero) == None):
                try:
                    # La persona juega primero
                    if primer_movimiento == "1":
                        print("Seleccione un núemro 1-9")
                        num = int(input("Player: "))
                        player_move = make_move(tablero, True, num)

                        if not(player_move):
                            if check_end(tablero) != None: continue
                            decision = movimientosIA(tablero, primer_movimiento, decision)
                            mostrar_tablero(tablero)
                            if check_end(tablero) != None: continue
                            player_move = True

                    # La maquina juega primero
                    if primer_movimiento == "2":
                        if num_int:
                            if check_end(tablero) != None: continue
                            decision = movimientosIA(tablero, primer_movimiento, decision)
                            mostrar_tablero(tablero)
                            if check_end(tablero) != None: continue
                        
                        print("Seleccione un núemro 1-9")
                        num = int(input("Player: "))
                        num_int = make_move(tablero, True, num)
                        if num_int: num_int = False
                        elif not(num_int): num_int = True

                except: print("Se esperaba un valor numérico entero"); num_int = False; continue

            if check_end(tablero) == "O": print("\n----- Gana la maquina :3 -----\n")
            else: print("\n----- Empate -----\n")

        else:
            print("Bye")
            break
        tablero = [" "," "," "," "," "," "," "," "," "]

if __name__ == "__main__":
    main()