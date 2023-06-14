# Como usar
- Colocar arquivos de input na pasta inputs
- Executar `bash execute.sh`
- Resultados em results, clausulas geradas em clauses
## Exemplo executar 1 arquivo

`python3 hoteleiro.py inputs/so_F.txt 3 < inputs/so_F.txt`

# Casos de Testes

## Lobosolitario - nao tem relacao com ninguem
- Relações amistosas tem mais prioridade do que relações de casal.
- Relações amistosas tem mais prioridade do que o menor preço.

## garanhao - tem afinidade alta com todos
- Homem solteiro "Casimiro" ficou junto de duas mulheres solteiras "Iasmine" e "Chris"

## fedorento - ninguem gosta dele
- Funciona corretamente

## odiado - ele nao gosta de ninguem e vice-versa
- Se a pessoa não é satisfeita, tentar colocar no quarto mais barato.

## sem_casal
- Funciona corretamente

## mais_gente_que_quarto
- Funciona corretamente: unsat

## sem_casal
- Funciona corretamente

## so_casal
- Funciona corretamente

## casal_brigado - É um casal, mas tem afinidade baixa.
- Mantém o casal junto no mesmo quarto

## so_F
- Funcionamento Correto
## so_H
- Funcionamento Correto

# infiel
- Individuo do casal se relaciona com mais de uma pessoa
- Comportamento indefinido. Depende de afinidade. Pode juntar casal com amante.

