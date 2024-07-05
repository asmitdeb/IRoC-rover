import time

def SCM_init_test():
    coordinates = []
    current_x = 0.6
    current_y = 0.6
    # coordinates.append((current_x, current_y))
    x = float(input("Enter x coordinate "))
    y = float(input("Enter y coordinate "))
    coordinates.append((x, y))
    while True:
        choice = int(input("Enter 0 to stop or 1 to add more points "))
        if choice == 0:
            break
        else:
            x = float(input("Enter x coordinate "))
            y = float(input("Enter y coordinate "))
            coordinates.append((x, y))

    for point in coordinates:
        (target_x, target_y) = point
        print(f"moving from ({current_x}, {current_y}) to ({target_x}, {target_y})")
        time.sleep(1)
        # move_to_coordinate(current_x, current_y, target_x, target_y) #moving from current position to target
        (current_x, current_y) = (target_x, target_y)

    print(f"Final position of rover is ({current_x}, {current_y})")




