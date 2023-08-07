import time
from random import Random

matrix_size = 200
matrix_a = [[0] * matrix_size for a in range(matrix_size)]
matrix_b = [[0] * matrix_size for b in range(matrix_size)]
result = [[0] * matrix_size for r in range(matrix_size)]

random = Random()

def generate_random_matrix(matrix):
    for row in range(matrix_size):
        for col in range(matrix_size):
            matrix[row][col] = random.randint(-5, 5)

start = time.time()
for t in range(10): # perform 10 matrix multiplications
    generate_random_matrix(matrix_a)
    generate_random_matrix(matrix_b)
    result = [[0] * matrix_size for r in range(matrix_size)]
    # select row, select col, then go through each elem in that row/col
    for row in range(matrix_size):
        for col in range(matrix_size):
            for i in range(matrix_size):
                result[row][col] += matrix_a[row][i] + matrix_b[i][col]

end = time.time()
print("Done, time take: ", end - start)