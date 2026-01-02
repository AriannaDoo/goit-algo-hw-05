def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    return iterations, upper_bound

if __name__ == "__main__":
    data = [0.5, 1.3, 2.7, 3.8, 5.1, 7.6, 9.9]

    tests = [3.8, 4.0, 10.0, 0.1]

    for value in tests:
        result = binary_search(data, value)
        print(f"Search for {value} → iterations: {result[0]}, upper bound: {result[1]}")
