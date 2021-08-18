def nextSquare():
    i = 1

    # An Infinite loop to generate squares
    while True:
        print(f'in white {i}')
        yield i * i
        i += 1  # Next execution resumes
        # from this point


# Driver code to test above generator
# function
for num in nextSquare():
    if num > 100:
        break
    print(num)
