# f = open('alumnos.txt', 'r')
# # alumnos = f.read()
# # print(alumnos)
# # f.seek(0)
# # alumnos1 = f.read()
# # print(alumnos1)

# # alumnos = f.readlines()
# # print(alumnos)
# # print(alumnos[0])
# # for item in alumnos:
# #     print(item, end='')

# alumnos = f.readline()
# print(alumnos)
# f.close()

f = open('alumnos2.txt', 'w')
f.write('\n' + 'Hola mundo!!')
f.write('\n' + 'Nuevo Hola mundo!!')
f.close()