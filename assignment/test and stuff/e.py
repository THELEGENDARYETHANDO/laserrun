def rotate_90_clockwise(matrix):
    """
    Rotate a 2D matrix by 90 degrees clockwise.
    
    Args:
    matrix (list of list): The input 2D matrix.
    
    Returns:
    list of list: The rotated matrix.
    """
    if not matrix or len(matrix) == 0:
        return []
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Create a new matrix to store the rotated values
    rotated_matrix = [[0] * rows for _ in range(cols)]
    
    # Rotate the matrix
    for i in range(rows):
        for j in range(cols):
            rotated_matrix[j][rows - i - 1] = matrix[i][j]
    
    return rotated_matrix

# Example usage:
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
rotated_matrix = rotate_90_clockwise(matrix)
for row in rotated_matrix:
    print(row)
