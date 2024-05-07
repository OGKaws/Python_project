from random import randint
# Актуальная версия 2.2

#---------------------------------------  описание данных (глобальные переменные)

CELL_X = 1              #2 константы - состояния клетки
CELL_0 = 0
CELL_EMPTY = 2
FSIZE = 3
field = [[ CELL_EMPTY for m in range(FSIZE) ] for n in range(FSIZE)]
field_corners = (
        (0,0) ,
        (0,FSIZE-1) ,
        (FSIZE-1,0) ,
        (FSIZE-1,FSIZE-1) )
#while_count = 10         #-- переменная для цикла While и хода в рандомную клетку


#FSIZE строк, и в каждой FSIZE ячеек
# [
#     [CELL_EMPTY,CELL_EMPTY,CELL_EMPTY],     #0
#     [CELL_EMPTY,CELL_EMPTY,CELL_EMPTY],     #1
#     [CELL_EMPTY,CELL_EMPTY,CELL_EMPTY],     #2
# ]   #0          1          2

move_count = 0
active_player = CELL_X



def game_lev_gen() :
    if game_level == 1 :    #jun
        return randint (1,3) == 1
    elif game_level == 2 :  #mid
        return randint (1,2) == 1
    return True             #senior

def print_field() :
    for line in field :
        for cell in line :
            if cell == CELL_EMPTY : print(".",end='')
            elif cell == CELL_X : print("X",end='')
            elif cell == CELL_0 : print("0",end='')
        print()
    print()         #печать пустой строки после печати ВСЕГО поля

def make_human_move( act_player ) :       #сделать ход ФИШКА
    while True :
        try :   
            line_numb = int (input(f'Введите номер строки (1..{FSIZE}) : ')) - 1
            cell_numb = int (input(f'Введите номер клетки (1..{FSIZE}) : ')) - 1
        except : 
            print('Некорректные координаты, координаты должны быть целыми числами')
            continue
        if  0 <= line_numb < FSIZE and 0 <= cell_numb < FSIZE :
            if field[line_numb][cell_numb] == CELL_EMPTY :
                field[line_numb][cell_numb] = act_player
                return
            else :
                print ('Клетка уже занята')
        else :
            print ('Клетка за пределами поля')
        print_field()

def check_attack_n_defence_move ( act_player ) :

    def check_line(n,act_player,move_player) :
        opponent_player = CELL_0 if act_player == CELL_X else CELL_X            #!!!!!!!!!      
    #    print(opponent_player)#--------------------------------------------------------------- ОТЛАДОЧНЫЙ PRINT!!!!!!!!!!
        act_cell_q = 0
        empty_cell_q = 0
        idx = 0
        empty_idx = 0
        for cell in field[n] :  
            if cell == opponent_player : break                                  
            if cell == act_player : act_cell_q += 1
            if cell == CELL_EMPTY : 
                empty_cell_q += 1
                empty_idx = idx
            idx += 1
    
        if act_cell_q + empty_cell_q == FSIZE and empty_cell_q == 1 and game_lev_gen():
            field[n][empty_idx]=move_player
            return True
        return False
    
    def check_column(n,act_player,move_player) :        
        opponent_player = CELL_0 if act_player == CELL_X else CELL_X
    #    print(opponent_player)#--------------------------------------------------------------- ОТЛАДОЧНЫЙ PRINT!!!!!!!!!!
        act_cell_q = 0
        empty_cell_q = 0
        empty_idx = 0
        for cell_idx in range(FSIZE) :
            if field[cell_idx][n] == opponent_player : break
            if field[cell_idx][n] == act_player : act_cell_q += 1
            if field[cell_idx][n] == CELL_EMPTY :
                empty_cell_q += 1 
                empty_idx = cell_idx
                
        if act_cell_q + empty_cell_q == FSIZE and empty_cell_q == 1  and game_lev_gen():
            field[empty_idx][n] = move_player
            return True
        return False
    
    def check_diag(n,act_player,move_player) :
        opponent_player = CELL_0 if act_player == CELL_X else CELL_X
    #    print(opponent_player)#--------------------------------------------------------------- ОТЛАДОЧНЫЙ PRINT!!!!!!!!!!
        act_cell = 0
        empty_cell = 0
        empty_line_idx = 0
        if n == 1 :
            for line_idx in range(FSIZE) :              #проверка диагонали №1 атакуем
                if field[line_idx][line_idx] == opponent_player : break
                if field[line_idx][line_idx] == act_player : 
                    act_cell += 1
                if field[line_idx][line_idx] == CELL_EMPTY :
                    empty_cell += 1
                    empty_line_idx = line_idx
    
            if act_cell + empty_cell == FSIZE and empty_cell == 1 and game_lev_gen(): 
                field[empty_line_idx][empty_line_idx] = move_player
                return True
        else :      
            for line_idx in range(FSIZE) :              #проверка диагонали №2 атакуем
                if field[line_idx][FSIZE-1-line_idx] == opponent_player : break
                if field[line_idx][FSIZE-1-line_idx] == act_player : 
                    act_cell += 1
                if field[line_idx][line_idx] == CELL_EMPTY :
                    empty_cell += 1
                    empty_line_idx = line_idx 
    
            if act_cell + empty_cell == FSIZE and empty_cell == 1 and game_lev_gen(): 
                field[empty_line_idx][FSIZE-1-empty_line_idx] = move_player
                return True
        return False
    
    
    opponent_player = CELL_0 if act_player == CELL_X else CELL_X 

    for line_n in range(FSIZE) :                                       #атакуем. проверка строк
        if check_line(line_n,act_player,act_player) : return True

    for column_n in range(FSIZE) :                                     #атакуем. проверка колонок
        if check_column(column_n,act_player,act_player) : return True

    for diag_n in range(2) :
        if check_diag(diag_n,act_player,act_player) : return True

    for line_n in range(FSIZE) :                                      #проверка строк. защита
        if check_line(line_n,opponent_player,act_player) : return True

    for column_n in range(FSIZE) :                                     #проверка колонок. защита
        if check_column(column_n,opponent_player,act_player) : return True

    for diag_n in range(2) :
        if check_diag(diag_n,opponent_player,act_player) : return True

    return False

def make_comp_move( act_player ) :
    print("компьютер думает...")
    
    #       1) проверка - если свободна центральня клетка, то ход сделать туда
    if field[FSIZE//2][FSIZE//2] == CELL_EMPTY :
        field[FSIZE//2][FSIZE//2] = act_player
        return
    
    #       2) если есть ход, который приведет к победе - сделать его (АТАКА)
    #       3) если есть ход у противника, который приведет к победе - занять клетку, заблокировав ему этот ход (ЗАЩИТА)
    if check_attack_n_defence_move(act_player) : return
    
    #       4) если свободны углы - поставить в произвольный свободный угол ---- выходит из цикла если рандомные индексы оказались заняты и ставит случайную цифру из While в 164 строке

    #подсчет кол-ва свободных углов

    empty_corners = []                      # Массив пустых углов ( поскольку в этом блоке мы проходим по всем углам основного массива сбираем все пустые углы в этот массив что бы не проходить второй раз )
    for corner in field_corners :           # Пробегаемся с помощью for по массиву углов ( задан в описании данных )
        if field[corner[0]][corner[1]] == CELL_EMPTY :          # Если в поле [ в квадратных скобках даем координаты углов, параметр corener по очереди принимает значения из массива всех углов, если угол пустой] то --
            empty_corners.append( corner )                      # -- и с помощью команды .append(corner) добавляем текущий пустой угол в массив empty_corners        

    if len(empty_corners) != 0 :                                    # Проверяем условие ЕСЛИ количество пустых углов НЕ РАВНО 0 --
        corner_to_move = randint(0,len(empty_corners)-1)            #0 лев/верх 1 прав/верх 2 лев/низ 3 прав/низ -- ТО генерируем через randint рандомной число в диапазоне от 0 до значения параметра empty_corner_q

        field[empty_corners[corner_to_move][0]][empty_corners[corner_to_move][1]] = act_player          #   ПОЛЕПОЛЕ[из массива пустых углов[сгенерированное значение пустого угла][0 элемент из массива пустых углов]]
        return                                                                                                       # ПОЛЕ[из массива пустых углов[сгенерированное значение пустого угла][1 элемент из массива пустых углов]] 
    #       5) любая случайная незанятая клетка

    empty_cells = []                    # Массив пустых ячеек 

    line_idx = 0                        # Счетчик ай ди линии, используется для занесения ай ди линии в массив 
    for line in field :                 # Первый фор бежит по линиям в массиве field 
        cell_idx = 0                        # Счетчик ай ди ячейки, используется для занесения ай ди в массив
        for cell in line :              # Второй for бежит по ячейкам в линии
            if cell == CELL_EMPTY :     # Проверяем ячейку на содержимое, если пустая ТО --
                empty_cells.append( (line_idx, cell_idx) )      # добавляем в список координаты ПУСТОЙ клетки
            cell_idx += 1                    # Прибавляем +1 в счетчик idx каждую иттерацию
        line_idx += 1                   # Прибавляем в счетчик line_idx +1 каждую иттерацию ( речь о цикле который бежит по линиям массива field )

        if len(empty_cells) != 0 :              # Проверяем ЕСЛИ счетчик пустых ячеек НЕ = 0 ТО -- 
            cell_to_move = randint(0, len(empty_cells)-1)     # Генерируем рандомное число в диапазоне от 0 до колличества свободных ячеек 
            field[empty_cells[cell_to_move][0]][empty_cells[cell_to_move][1]] = active_player   # Ставим фишку в массив, в координатах задано [из массива пустых ячеек[сгенерированное число][0 / 1(первый ИЛИ второй элемент из массива пустых)]]
            return
        
def check_winner( act_player ) :             # функция проверки победителя, перебирает кололнки, строки и дикагонали.  Возвращает True если был выявлен победитель и False если никто не выиграл
    '''                                               
    + проверка 3-х строк
    + проверка 3-х колонок
    + проверка 2-х диагоналей
    '''
    
    for line in field : 
        cell_count = 0
        for cell in line : 
            if cell ==  act_player : cell_count +=1 
        if cell_count == FSIZE : return True

    
    for column_idx in range(FSIZE) :
        cell_count = 0
        for cell_idx in range(FSIZE) :
            if field[cell_idx][column_idx] ==  act_player : cell_count +=1 
        if cell_count == FSIZE : return True
            
    # первая диагональ
    cell_count = 0
    for cell_idx in range(FSIZE) :
        if field[cell_idx][cell_idx] == act_player : cell_count+=1
    if cell_count == FSIZE : return True
    
    # вторая диагональ
    cell_count = 0
    for cell_idx in range(FSIZE) :
        if field[cell_idx][ FSIZE-1-cell_idx] == act_player : cell_count+=1
    if cell_count == FSIZE : return True
    
    return False

#----------------------------------------------  ОСНОВНОЙ ПОТОК . отсюда стартует программа

while True :
    try :
        game_level = int (input('Выберите сложность игры 1...3 : '))
    except ValueError:
        print("ввели что-то отличное от чисел")
        continue
    if 1 <= game_level <=3 :
        break


while True :
    #x = input("Кем будете играть X/0 ")
    x = str(input("Кем будете играть X/0 "))
    poss_user_val = ('Х','х','X','x','О','о','O','o','0')
    if x in poss_user_val :
        human_player = CELL_X if x=="X" or x=="x" or x=="Х" or x=="х" else CELL_0
        break
    #if x=="X" or x=="x" or x=="Х" or x=="х" or x=="0" or x=="o" or x=="O" or x=="О" or x=="о" :
        #human_player = CELL_X if x=="X" or x=="x" or x=="Х" or x=="х" else CELL_0
        #break
    print("Введите либо X либо 0")

while True :
    print_field()
    print("Ход " + ("крестиков" if active_player == CELL_X else "ноликов") )
    
    if human_player == active_player :
        make_human_move(active_player)
    else :
        make_comp_move(active_player)

    move_count += 1
    
    if move_count == FSIZE*FSIZE or check_winner(active_player) : break 
    
    if (active_player == CELL_0) :
        active_player = CELL_X
    else :
        active_player = CELL_0
    
print_field()
if move_count == FSIZE * FSIZE and not check_winner(active_player) :
    print("ничья") 
else :
    if active_player == CELL_0 :
        print("выиграл нолики")
    else : 
        print("выиграл крестики")

















