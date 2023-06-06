from math import gcd
from functools import reduce
import copy
from itertools import product
import os

rooms = []
r_counter = {"C": 0, "D": 0, "T": 0, "Q": 0}
numberOfRooms = int(input())
for i in range(0, numberOfRooms):
  room = input().split(" ")
  if room[0] == 'C':
    r_counter['C'] += 1
  if room[0] == 'D':
    r_counter['D'] += 1
  if room[0] == 'T':
    r_counter['T'] += 1
  if room[0] == 'Q':
    r_counter['Q'] += 1
  rooms.append(room)

people = {"C": []}
total_people = 0
for i in range(0, 2):
  n_people = input().split(" ")
  total_people += int(n_people[0])
  if int(n_people[0]) == 0:
    people[n_people[1]] = []
    continue
  people[n_people[1]] = input().split(" ")
n_people = input().split(" ")
n_casal = int(n_people[0])

for i in range(0, int(n_people[0])):
  people[n_people[1]].append(tuple(input().split(" ")))  
  
if n_casal > r_counter["C"]:
  n_casal = n_casal - r_counter["C"]
  total_people -= 2*r_counter["C"]
  r_counter["C"] = 0
else:
  r_counter["C"] = r_counter["C"] - n_casal
  total_people -= 2*n_casal
  n_casal = 0

if r_counter["C"]*1 + r_counter["D"]*2 + r_counter["T"]*3 + r_counter["Q"]*4 < total_people:
  print("UNSAT")
  exit()

relationships = {}  
for i in range(0, int(input())):
  people_relations = input().strip().split(":")
  relations = people_relations[1][1:].split(" ")
  relationships[people_relations[0].strip()] = {relations[i-2:i][0] : int(relations[i-2:i][1])
                                                  for i in range(2, len(relations) + 2, 2)}
for person in people["M"] + people["F"]:
  if person not in relationships.keys():
    relationships[person] = {}
for person in relationships:
  for male in people["M"]:
    if person in people["M"] and person != male:
      try:
        try:
          if relationships[person][male] > relationships[male][person]:
            relationships[person][male] = relationships[male][person]
          else:
            relationships[male][person] = relationships[person][male]
        except:
          if relationships[person][male] < 50:
            relationships[male][person] = relationships[person][male]
          else:
            del relationships[person][male]
      except:
        pass
    if person in people["F"]:
      try:
        try:
          if relationships[person][male] > relationships[male][person]:
            relationships[person][male] = relationships[male][person]
          else:
            relationships[male][person] = relationships[person][male]
        except:
          relationships[male][person] = (0, "S")
          relationships[person][male] = (0, "S")
      except:
        pass
  for female in people["F"]:
    if person in people["F"] and person != female:
      try:
        try:
          if relationships[person][female] > relationships[female][person]:
            relationships[person][female] = relationships[female][person]
          else:
            relationships[female][person] = relationships[person][female]
        except:
          if relationships[person][female] < 50:
            relationships[female][person] = relationships[person][female]
          else:
            del relationships[person][female]
      except:
        pass

for married in people["C"]:
  try:
    relationships[married[0]][married[1]] = (100, "M")
  except:
    relationships[married[0]] = {}
    relationships[married[0]][married[1]] = (100, "M")
  try:
    relationships[married[1]][married[0]] = (100, "M")
  except:
    relationships[married[1]] = {}
    relationships[married[1]][married[0]] = (100, "M")

couple_members = []
for couple in people["C"]:
  couple_members.extend([*couple])

symbolCounter = 1
people_clauses = {}
for person in people["M"]:
  people_clauses[person] = list(range(symbolCounter, symbolCounter + numberOfRooms))
  symbolCounter += numberOfRooms

for person in people["F"]:
  people_clauses[person] = list(range(symbolCounter, symbolCounter + numberOfRooms))
  symbolCounter += numberOfRooms
rooms_clauses = {}
for i, room in enumerate(rooms):
  weight = 0
  casal_weight = 0
  max_val = 0
  if room[0] == "C":
    weight = 2
    casal_weight = (1, 1)
    max_val = 2
  if room[0] == "D":
    weight = 1
    casal_weight = (1, 1)
    max_val = 2
  if room[0] == "T":
    weight = 1
    casal_weight = (1, 1)
    max_val = 3
  if room[0] == "Q":
    weight = 1
    casal_weight = (1, 1)
    max_val = 4
  rooms_clauses[i] = ([(weight, clause[i]) if person not in couple_members
                      else
                      (casal_weight[0], clause[i]) if person in people["M"]
                      else (casal_weight[1], clause[i])
                      for person, clause in people_clauses.items()] + [max_val], symbolCounter)
  symbolCounter += 1

rooms_gcd = reduce(lambda x,y:gcd(*[x,y]),[int(room[1]) for room in rooms])
minimized_room_values = [int(int(room[1])/rooms_gcd) for room in rooms]
max_minimized_room_value = max(minimized_room_values)

room_binding_clauses = {}
for room_index, room_symbols in rooms_clauses.items():
  room_binding_clauses[room_symbols[1]] = []
  all_symbols = []
  for symbol in room_symbols[0][:-1]:
    room_binding_clauses[room_symbols[1]].append([-symbol[1], room_symbols[1]])
    all_symbols.append(symbol[1])
  all_symbols.append(-room_symbols[1])
  room_binding_clauses[room_symbols[1]].append(all_symbols)
  room_binding_clauses[room_symbols[1]].append(minimized_room_values[room_index])

relationships_copy = copy.deepcopy(relationships)

relationship_clauses = {}
for person in relationships:
  for person2 in relationships[person]:
    if person2 in relationships_copy[person]:
      pair_list = list(zip(people_clauses[person], people_clauses[person2]))
      for pair_symbols_for_room in pair_list:
        try:
          relationship_clauses[symbolCounter].append([-symbol for symbol in pair_symbols_for_room] + [symbolCounter])
        except:
          relationship_clauses[symbolCounter] = [[-symbol for symbol in pair_symbols_for_room] + [symbolCounter]]
      relationship_clauses[symbolCounter].extend([list(clause) + [-symbolCounter] for clause in product(*pair_list)])
      if relationships[person][person2] == (0, "S"):
        relationship_clauses[symbolCounter].append((relationships[person][person2][0] - 50) * max_minimized_room_value * 3)
      elif relationships[person][person2] == (100, "M"):
        relationship_clauses[symbolCounter].append((relationships[person][person2][0] - 50) * max_minimized_room_value * 2)        
      else:
        relationship_clauses[symbolCounter].append((relationships[person][person2] - 50) * max_minimized_room_value)        

      symbolCounter += 1
      try:
        del relationships_copy[person][person2]
      except:
        pass
      try:
        del relationships_copy[person2][person]
      except:
        pass
minimizer_clauses = []

for room_index, room_symbol in enumerate(room_binding_clauses.keys()):
  minimizer_clauses.append((minimized_room_values[room_index], room_symbol))

for rel_symbol, rel_val in relationship_clauses.items():
  minimizer_clauses.append((-rel_val[-1], rel_symbol))
  relationship_clauses[rel_symbol] = relationship_clauses[rel_symbol][:-1]

total_constraints = len(people_clauses) + len(rooms_clauses) + len(room_binding_clauses)*(len(people_clauses)+1) + len(relationship_clauses)*(2**len(rooms_clauses) + len(rooms_clauses))
pbo_file = open("clauses.pbo", mode="wt")
pbo_file.write(f"* #variable= {symbolCounter - 1} #constraint= {total_constraints}\n\n")
pbo_file.write("min:")

for min_clause in minimizer_clauses:
  pbo_file.write(f" {min_clause[0]} x{min_clause[1]}")
pbo_file.write(";\n\n")

for pers, pers_clauses in people_clauses.items():
  for pers_clause in pers_clauses:
    pbo_file.write(f"{1} x{pers_clause} ")
  pbo_file.write("= 1;\n")
pbo_file.write("\n")

for room_s, room_clauses_it in rooms_clauses.items():
  for room_clause in room_clauses_it[0]:
    try:
      pbo_file.write(f"-{room_clause[0]} x{room_clause[1]} ")
    except:
      pbo_file.write(f">= -{room_clause}")
  pbo_file.write(";\n")
pbo_file.write("\n")

for r_to_bind, r_binding_clauses in room_binding_clauses.items():
  for r_binding_clause in r_binding_clauses[:-2]:
    pbo_file.write(f"1 ~x{-r_binding_clause[0]} 1 x{r_binding_clause[1]} ")
    pbo_file.write(">= 1;\n")
  for r_binding_clause in r_binding_clauses[-2][:-1]:
    pbo_file.write(f"1 x{r_binding_clause} ")
  pbo_file.write(f"1 ~x{-r_binding_clauses[-2][-1]} >= 1;\n\n")

for rel_ind, rel_clauses in relationship_clauses.items():
  for relationship_clause in rel_clauses:
    if len(relationship_clause) == 3:
      pbo_file.write(f"1 ~x{-relationship_clause[0]} 1 ~x{-relationship_clause[1]} 1 x{relationship_clause[2]} >= 1;\n")
    else:
      for symb in relationship_clause[:-1]:
        pbo_file.write(f"1 x{symb} ")
      pbo_file.write(f"1 ~x{-relationship_clause[-1]} >=1;\n")
  pbo_file.write("\n")
pbo_file.close()

print(symbolCounter - 1)

clasp_output = os.popen('clasp clauses.pbo').read()
clasp_result = []
for clasp_line in clasp_output.split("\n")[:-1]:
  if "UNSAT" in clasp_line:
    print("UNSAT")
    exit()
  if clasp_line[0] == "v":
    clasp_result.extend(clasp_line[1:].strip().split(" "))
clasp_true_res = []
for clasp_var in clasp_result:
  if "-" not in clasp_var:
    clasp_true_res.append(int(clasp_var.replace("x", "")))

room_result = {}
for result_symb in clasp_true_res:
  for person, person_symbs in people_clauses.items():
    if result_symb in person_symbs:
      try:
        room_result[(person_symbs.index(result_symb), tuple(rooms[person_symbs.index(result_symb)]))].append(person)
      except:
        room_result[(person_symbs.index(result_symb), tuple(rooms[person_symbs.index(result_symb)]))] = [person]
res_list = []
for result in room_result:
  res_list.append((result, room_result[result]))
res_list.sort()
for result in res_list:
  print(result)
