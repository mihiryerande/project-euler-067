# Problem 67:
#     Maximum Path Sum 2
#
# Description:
#     By starting at the top of the triangle below and moving to adjacent numbers on the row below,
#       the maximum total from top to bottom is 23.
#
#            (3)
#           (7) 4
#          2 (4) 6
#         8  5 (9) 3
#
#     That is, 3 + 7 + 4 + 9 = 23.
#
#     Find the maximum total from top to bottom in triangle.txt (right click and Save Link/Target As...),
#       a 15K text file containing a triangle with one-hundred rows.
#
#     NOTE:
#       This is a much more difficult version of Problem 18.
#       It is not possible to try every route to solve this problem, as there are 2^99 altogether!
#       If you could check one trillion (10^12) routes every second
#         it would take over twenty billion years to check them all.
#       There is an efficient algorithm to solve it. ;o)

from typing import List, Tuple


def read_triangle(filename: str) -> List[List[int]]:
    """
    Reads the number triangle written in the given `filename`.

    Args:
        filename (str): Name of file containing number triangle

    Returns:
        (List[List[int]]): Number triangle as a list of int list

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(filename) == str

    with open(filename, 'r') as f:
        triangle = [list(map(int, line.strip().split())) for line in f.readlines()]
    return triangle


def compute_trellis(triangle: List[List[int]]) -> List[List[Tuple[int, int]]]:
    """
    Given a number `triangle`, returns a 'trellis',
      computed using dynamic programming,
      which is the same shape as the triangle,
      and each element holds information about the best paths
      starting from the top of the triangle to each cell.

    Args:
        triangle (List[List[int]]): Number triangle

    Returns:
         List[List[Tuple[int, int]]]:
           Trellis storing the best paths from top to each cell.
    """
    # Dynamic programming structure to keep track of the
    #   best paths landing at each point in the triangle
    # Trellis will hold a tuple of...
    #   * Maximum sum achievable by landing at this point in triangle
    #   * -1 or 0, indicating whether best path from above went through left or right element
    trellis = [[(0, 0) for _ in line] for line in triangle]

    # Initialize trellis using first triangle element
    trellis[0][0] = (triangle[0][0], 1)  # 1 here is a dummy value

    # Populate each row of the trellis
    for i in range(1, len(trellis)):
        # Fill in leftmost and rightmost elements, as they both have only one possible incoming path
        trellis[i][0] = (trellis[i-1][0][0] + triangle[i][0], 0)
        trellis[i][-1] = (trellis[i-1][-1][0] + triangle[i][-1], -1)

        # Fill in remaining (inner) entries of trellis row
        for j in range(1, len(trellis[i])-1):
            best_s = max([-1, 0], key=lambda s: trellis[i-1][j+s])
            this_elt = triangle[i][j]
            trellis[i][j] = (trellis[i-1][j+best_s][0] + this_elt, best_s)

    return trellis


def compute_best_path(triangle: List[List[int]], trellis: List[List[Tuple[int, int]]]) -> Tuple[int, List[int]]:
    """
    Given a number `triangle`, and the corresponding `trellis`,
        returns the maximum achievable total path sum
        walking down the triangle from top to bottom,
        as well as the path elements which produce that total.

    Args:
       triangle (List[List[int]]): Number triangle
       trellis (List[List[Tuple[int, int]]]): Computed trellis

    Returns:
        (Tuple[int, List[int]]):
            Tuple of...
              * (int)      Maximum Path Sum
              * (int list) Maximum Path elements
    """
    # First find the index of the best path's endpoint in the final row
    endpoint = max(enumerate(trellis[-1]), key=lambda x: x[1][0])

    # Unpack relevant values
    curr_j = endpoint[0]
    best_sum = endpoint[1][0]

    # Start at that point in the last row,
    #   and walk backwards (up the trellis)
    #   to figure out the path which led there
    curr_i = len(trellis) - 1
    best_path = []  # Best path (first determined in reverse order)
    while curr_i >= 0:
        best_path.append(triangle[curr_i][curr_j])
        step_j = trellis[curr_i][curr_j][1]
        curr_i -= 1  # Step up to previous row
        curr_j += step_j  # Step left/right to the best incoming point
    best_path.reverse()

    return best_sum, best_path


def main(filename: str) -> Tuple[int, List[int]]:
    """
    Returns the maximum achievable total path sum
      walking down the triangle from top to bottom,
      as well as the path elements which produce that total.

    Args:
        filename (str): Name of file containing number triangle

    Returns:
        (Tuple[int, List[int]]):
            Tuple of...
              * (int)      Maximum Path Sum
              * (int list) Maximum Path elements
    """
    assert type(filename) == str

    triangle = read_triangle(filename)

    trellis = compute_trellis(triangle)

    return compute_best_path(triangle, trellis)


if __name__ == '__main__':
    max_sum, max_path = main('triangle.txt')
    print('Maximum Path Sum in provided triangle:')
    print('  {}'.format(max_sum))
    print('Path producing the Maximum Sum:')
    print('  {}'.format('\n  → '.join(map(str, max_path))))
