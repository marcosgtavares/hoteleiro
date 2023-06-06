# Casos de Testes

## Lobosolitario - nao tem relacao com ninguem
- Relações amistosas tem mais prioridade do que relações de casal.
- Relações amistosas tem mais prioridade do que o menor preço.

## garanhao - tem afinidade alta com todos
- ERRO
```
python3 hoteleiro.py < garanhao.txt 

Traceback (most recent call last):
  File "/home/johan/Documentos/UnB/SEGUNDO SEMESTRE/Logica IA/hoteleiro/hoteleiro.py", line 165, in <module>
    del relationships_copy[person2][person]
KeyError: 'Casimiro'
```

## fedorento - ninguem gosta dele

## odiado - ele nao gosta de ninguem e vice-versa
- Se a pessoa não é satisfeita, tentar colocar no quarto mais barato.

## sem_casal

## mais_quarto_que_gente

## mais_gente_que_quarto

## sem_casal

## so_casal

## casal_brigado - É um casal, mas tem afinidade baixa.
- Mantém o casal junto no mesmo quarto

## so_F
- ERRO
```
python3 hoteleiro.py < so_F.txt 

Traceback (most recent call last):
  File "/home/johan/Documentos/UnB/SEGUNDO SEMESTRE/Logica IA/hoteleiro/hoteleiro.py", line 22, in <module>
    people[n_people[1]].append(tuple(input().split(" ")))
IndexError: list index out of range
```
## so_H
- ERRO
```
python3 hoteleiro.py < so_H.txt 

Traceback (most recent call last):
  File "/home/johan/Documentos/UnB/SEGUNDO SEMESTRE/Logica IA/hoteleiro/hoteleiro.py", line 22, in <module>
    people[n_people[1]].append(tuple(input().split(" ")))
IndexError: list index out of range
```