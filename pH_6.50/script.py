import sys

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print("Usage: python script.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    # Open the file
    with open(file_path, "r") as file:
        # Read lines and convert to float
        values = [float(line.strip()) for line in file.readlines()]

    # Initialize counters
    count_greater_than_0_8 = 0
    count_smaller_than_0_2 = 0

    # Iterate through the values
    for value in values:
        if value > 0.8:
            count_greater_than_0_8 += 1
        elif value < 0.2:
            count_smaller_than_0_2 += 1

    total_values = count_greater_than_0_8 + count_smaller_than_0_2
    print("Number of values larger than 0.8:", count_greater_than_0_8)
    print("Number of values smaller than 0.2:", count_smaller_than_0_2)
    print("Percentage of values larger than 0.8: {:.2f}".format((count_greater_than_0_8 / total_values)))
    print("Percentage of values smaller than 0.2: {:.2f}".format((count_smaller_than_0_2 / total_values)))

except FileNotFoundError:
    print("File not found:", file_path)
