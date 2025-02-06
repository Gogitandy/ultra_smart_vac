from random import shuffle, choice, randint


class Room:

    def __init__(self, x=5):

        self.nrows = x

        self.ncols = x

        # add random layout to the room constructor

        self.layout = self.layout_randomizer()

        # print(self.layout)

        self.no_islands()

        print("---")

        for list in self.layout:
            print(list)

        self.add_furniture()

        print("---")

        for row in self.layout:
            print(row)

        return

    # method to generate a random layout within the grid size determined by user

    def layout_randomizer(self):

        # list for entire layout

        layout = []

        # add buffer of 0's across top for out of bounds

        layout.append([0] * (self.ncols + 2))

        # iterate through all rows

        for i in range(self.nrows):

            # list for cells in row (will be 1 or 0) starting with initial 0

            row = [0]

            # iterate through all columns

            for j in range(self.ncols):

                # pick at random 1 (cell=in room) 0 (cell=not in room)

                if i == 0 or i == self.nrows - 1:

                    row.append(choice([0, 1]))

                elif j == 0 or j == self.ncols - 1:

                    row.append(choice([0, 1]))

                else:

                    row.append(1)

            # add 0 for boundary

            row.append(0)

            # add completed row to layout

            layout.append(row)

        # add bottom border of 0's for buffer

        layout.append([0] * (self.ncols + 2))

        return layout

    # check all the corners to make sure that there are no isolated 1's

    # updated to fix corners inside the border of 0's

    def no_islands(self):

        # check upper left corner

        # print("check1")

        if (

                self.layout[1][1] == 1 and

                self.layout[1][2] == 0 and

                self.layout[2][1] == 0

        ):
            # fix upper left island

            # print("FIX!")

            self.layout[1][2] = 1

        # check upper right corner

        if (

                self.layout[1][self.ncols] == 1 and

                self.layout[1][self.ncols - 1] == 0 and

                self.layout[2][self.ncols] == 0

        ):
            # fix upper right island

            # print("FIX!")

            self.layout[1][self.ncols - 1] = 1

        # check lower left corner

        if (

                self.layout[self.nrows][1] == 1 and

                self.layout[self.nrows][2] == 0 and

                self.layout[self.nrows - 1][1] == 0

        ):
            # fix lower left island

            # print("FIX!")

            self.layout[self.nrows][2] = 1

        # check lower right corner

        # print("check2")

        if (

                self.layout[self.nrows][self.ncols] == 1 and

                self.layout[self.nrows][self.ncols - 1] == 0 and

                self.layout[self.nrows - 1][self.ncols] == 0

        ):
            # fix lower right island

            # print("FIX!")

            self.layout[self.nrows][self.ncols - 1] = 1

        return

    # method to add random furniture if room > 7x7

    def add_furniture(self):

        if self.ncols > 7:

            for i in range(3, self.nrows - 3):

                for j in range(3, self.ncols - 3):

                    if choice([True, False]):

                        if (

                                self.layout[i - 1][j] == 1 and

                                self.layout[i + 1][j] == 1 and

                                self.layout[i][j + 1] == 1 and

                                self.layout[i][j - 1] == 1

                        ):
                            self.layout[i][j] = 0

                            print(f"add {i},{j}")

        return


class SmartVac:

    def __init__(self, r):

        # initialize the room dimensions

        self.room = r

        # initialize the map

        self.map = {}

        # intial position randomizer

        while True:

            x_p = randint(0, self.room.nrows - 1)

            y_p = randint(0, self.room.ncols - 1)

            if self.room.layout[x_p][y_p] == 1:
                self.position = (x_p, y_p)

                print(f"start{x_p},{y_p}")

                break

        # initialize object sensors

        self.left_sensor = 0

        self.right_sensor = 0

        self.front_sensor = 0

        # initialize movements

        self.moves = {0: "∧", 1: "∨", 2: ">", 3: "<", -1: "X"}

        # initialize direction (0: up, 2: right, 1: down, 3: left)

        self.directions = [0, 2, 1, 3]

        self.direction_index = 0

        self.direction = self.directions[self.direction_index]

        # holder for converted map

        self.perimeter_map = []

        return

    # map perimeter of room

    def map_room(self):

        # set starting position

        x, y = self.position

        # Track visited positions and their hit counts

        visited_positions = {}

        visited_positions[self.position] = 1

        # starting positioin = visited

        self.map[(x, y)] = 1

        # update sensors

        self.update_sensors(x, y)

        # move forward until getting a bump

        while self.front_sensor == 1:
            self.move_forward()

        self.turn_right()

        tracing_perimeter = True

        while True:

            x, y = self.position

            print(f"Front: {self.front_sensor}, Left: {self.left_sensor}, Right: {self.right_sensor}")

            print(f"Current Position: ({x}, {y}), Direction: {self.direction}")

            if tracing_perimeter:

                self.trace_wall()

                if self.left_sensor == 1:

                    tracing_perimeter = False

                    self.trace_object()

                    while self.front_sensor == 1:
                        self.move_forward()

            else:

                self.trace_object()

                while self.front_sensor == 1:
                    self.move_forward()

                if self.left_sensor == 0:
                    tracing_perimeter = True

                    # self.position == self.start_position:

                    # break

            # update the hit count for the current position

            if self.position in visited_positions:

                visited_positions[self.position] += 1

                if visited_positions[self.position] >= 4:  # adjust the threshold as needed

                    print("Completed lap around the perimeter.")

                    self.perimeter_map = self.convert_map()

                    break

            else:

                visited_positions[self.position] = 1

            input("push enter")

    def print_room_with_vac(self):

        # create a copy of the room layout to modify

        room_with_vac = [row[:] for row in self.room.layout]

        # determine the symbol based on the vacuum's direction

        direction_symbols = {0: '^', 1: 'v', 2: '>', 3: '<'}

        vac_symbol = direction_symbols[self.direction]

        # place the vacuum symbol in the current position

        x, y = self.position

        room_with_vac[x][y] = vac_symbol

        # print the modified room layout

        for row in room_with_vac:
            print(' '.join(str(cell) for cell in row))

    # method to move forward

    def move_forward(self):

        print("moving forward")

        if self.front_sensor == 1:

            next_x, next_y = self.position

            # print(f"Trying to move forward, dir ={self.direction}")

            if self.direction == 0:

                next_x -= 1

            elif self.direction == 1:

                next_x += 1

            elif self.direction == 2:

                next_y += 1

            elif self.direction == 3:

                next_y -= 1

            x, y = next_x, next_y

            self.map[(x, y)] = 1

            self.position = (x, y)

            self.update_sensors(x, y)

            # moved = True

            self.print_room_with_vac()

            # print(f"Moved to: ({x}, {y}) dir ={self.direction}")

            # self.turn_right()

        else:
            print("blocked")

        # print(f"pos after move_forward={self.position}")

        input("press enter")

        return  # a value?

    # method to turn left

    def turn_left(self):

        # print("turn left")

        self.direction_index = (self.direction_index - 1) % 4

        if self.direction_index < 0:
            self.direction_index += 4

        self.direction = self.directions[self.direction_index]

        x, y = self.position

        self.update_sensors(x, y)

        self.print_room_with_vac()

        # print(self.direction)

        input("press enter")

    # method to turn right

    def turn_right(self):

        # print("turn right")

        self.direction_index = (self.direction_index + 1) % 4

        self.direction = self.directions[self.direction_index]

        x, y = self.position

        self.update_sensors(x, y)

        self.print_room_with_vac()

        # print(self.direction)

        input("press enter")

    # method to trace wall using left sensor

    def trace_wall(self):

        print("tracing wall")

        # outter logic to turn right first?

        start_trace_position = self.position

        while True:

            while self.left_sensor == 0 and self.front_sensor == 1:

                self.move_forward()

                if self.position == start_trace_position:
                    print("at start position")

                    return  # return a value?

            if self.left_sensor == 1:
                # print("left sensor = 1")

                return  # return a value?

            # bumped

            self.turn_right()

    # method to trace an object

    def trace_object(self):

        print("tracing object")

        start_trace_position = self.position

        while True:

            # need outter logic to turn left and move forward

            while self.front_sensor == 1 and self.left_sensor == 0:

                self.move_forward()

                if self.position == start_trace_position:
                    print("at start position")

                    return  # return a value?

            if self.left_sensor == 1:

                self.turn_left()

                self.move_forward()

                if self.position == start_trace_position:
                    print("at start position")

                    return  # return a value?

            if self.front_sensor == 0:
                print("bump!")

                return

    # update all three sensor inputs

    def update_sensors(self, x, y):

        print("updating sensors")

        # set front left and right to match vac direction

        directions = [

            ((x - 1, y), (x, y - 1), (x, y + 1)),  # facing up

            ((x + 1, y), (x, y + 1), (x, y - 1)),  # facing down

            ((x, y + 1), (x - 1, y), (x + 1, y)),  # facing right

            ((x, y - 1), (x + 1, y), (x - 1, y))  # facing left

        ]

        front, left, right = directions[self.direction]

        # update front sensor

        self.front_sensor = self.room.layout[front[0]][front[1]]

        # update left

        self.left_sensor = self.room.layout[left[0]][left[1]]

        # update right sensor

        self.right_sensor = self.room.layout[right[0]][right[1]]

        return

    # convert dictionary map into a 2d array

    def convert_map(self):

        # find out what the boundaries are

        min_x = min(key[0] for key in self.map.keys())

        max_x = max(key[0] for key in self.map.keys())

        min_y = min(key[1] for key in self.map.keys())

        max_y = max(key[1] for key in self.map.keys())

        # initialize 2d with size for border of 0's as well

        nrows = max_x - min_x + 3

        ncols = max_y - min_y + 3

        array_map = [[0 for _ in range(ncols)] for _ in range(nrows)]

        # fill in the array buffering for the border

        for (x, y), value in self.map.items():
            array_map[x - min_x + 1][y - min_y + 1] = value

        return array_map

    # vacuuming down a column

    def move_down(self, array_map):

        x, y = self.position

        # current_col = y

        last_1_in_col = max(i for i in range(len(array_map)) if array_map[i][y] == 1)

        # make sure pointing down

        while True:

            while self.direction != 1:
                self.turn_left()

                print(self.direction)

            # vacuum

            array_map[x][y] = 2

            print(f"vacummed {x},{y}")

            for row in array_map:
                print(row)

            input("press enter")

            # check if at last open cell in col

            if self.position[0] == last_1_in_col:
                print("end of col")

                break

            # move forward if can

            if self.front_sensor == 1:

                self.move_forward()

            # if not turn left

            else:

                self.turn_left()

                # go around object

                x, y = self.position

                while self.position[0] <= x or self.position[1] != y:

                    if self.right_sensor == 1:

                        self.turn_right()

                        self.move_forward()

                    elif self.front_sensor == 1:

                        self.move_forward()

                    else:

                        self.turn_left()

            x, y = self.position

        return array_map

    # move column over after vacuuming down

    def next_col_up(self, array_map):

        while self.direction != 2:
            self.turn_left()

        if self.front_sensor == 1:

            self.move_forward()

        else:

            self.turn_left()

            x, y = self.position

            while self.position[1] == y:

                if self.right_sensor == 1:

                    self.turn_right()

                    self.move_forward()

                elif self.front_sensor == 1:

                    self.move_forward()

                else:

                    self.turn_left()

        x, y = self.position

        start_in_col = max(i for i in range(len(array_map)) if array_map[i][y] == 1)

        while self.direction != 1:
            self.turn_right()

            print(self.direction)

        while self.position[0] != start_in_col:
            self.move_forward()

        print("ready to vacuum up")

    # move a column over after going up

    def next_col_down(self, array_map):

        # face right

        while self.direction != 2:
            self.turn_right()

        # move forward if can

        if self.front_sensor == 1:

            self.move_forward()

        # if not, move around object to get to an open spot in the next column

        else:

            self.turn_right()

            x, y = self.position

            while self.position[1] == y:

                if self.left_sensor == 1:

                    self.turn_left()

                    self.move_forward()

                elif self.front_sensor == 1:

                    self.move_forward()

                else:

                    self.turn_right()

        x, y = self.position

        # first open space in column

        start_in_col = min(i for i in range(len(array_map)) if array_map[i][y] == 1)

        # point up

        while self.direction != 0:
            self.turn_right()

            print(self.direction)

        # go to first space

        while self.position[0] != start_in_col:
            self.move_forward()

        print("ready to vacuum up")

    # vacuum up a column

    def move_up(self, array_map):

        x, y = self.position

        first_1_in_col = min(i for i in range(len(array_map)) if array_map[i][y] == 1)

        # make sure pointing up

        while True:

            while self.direction != 0:
                self.turn_left()

                print(self.direction)

            # vacuum

            array_map[x][y] = 2

            print(f"vacuumed {x},{y}")

            for row in array_map:
                print(row)

            input("press enter")

            # check if at end of col

            if self.position[0] == first_1_in_col:
                print("end of col")

                break

            # move forward if can

            if self.front_sensor == 1:

                self.move_forward()

            # if not prepare to go around

            else:

                self.turn_right()

                # go around

                x, y = self.position

                while self.position[0] >= x or self.position[1] != y:

                    if self.left_sensor == 1:

                        self.turn_left()

                        self.move_forward()

                    elif self.front_sensor == 1:

                        self.move_forward()

                    else:

                        self.turn_right()

            x, y = self.position

        return array_map

    # vacuum down a column but go around objects towards left of map

    def move_down_left_bias(self, array_map):

        x, y = self.position

        last_1_in_col = max(i for i in range(len(array_map)) if array_map[i][y] == 1)

        # make sure pointing down

        while True:

            while self.direction != 1:
                self.turn_left()

                print(self.direction)

            # vacuum

            array_map[x][y] = 2

            print(f"vacuumed {x},{y}")

            for row in array_map:
                print(row)

            input("press enter")

            # check if at last open cell in col

            if self.position[0] == last_1_in_col:
                print("end of col")

                break

            # move forward if can

            if self.front_sensor == 1:

                self.move_forward()

            # if not turn right

            else:

                self.turn_right()

                # go around object

                x, y = self.position

                while self.position[0] <= x or self.position[1] != y:

                    if self.left_sensor == 1:

                        self.turn_left()

                        self.move_forward()

                    elif self.front_sensor == 1:

                        self.move_forward()

                    else:

                        self.turn_right()

            x, y = self.position

        return array_map

    # vacuum up columm but moving around ojbects towards left of map

    def move_up_left_bias(self, array_map):

        x, y = self.position

        first_1_in_col = min(i for i in range(len(array_map)) if array_map[i][y] == 1)

        # make sure pointing up

        while True:

            while self.direction != 0:
                self.turn_left()

                print(self.direction)

            # vacuum

            array_map[x][y] = 2

            print(f"vacuumed {x},{y}")

            for row in array_map:
                print(row)

            input("press enter")

            # check if at end of col

            if self.position[0] == first_1_in_col:
                print("end of col")

                break

            # move forward if can

            if self.front_sensor == 1:

                self.move_forward()

            # if not prepare to go around

            else:

                self.turn_left()

                # go around

                x, y = self.position

                while self.position[0] >= x or self.position[1] != y:

                    if self.right_sensor == 1:

                        self.turn_right()

                        self.move_forward()

                    elif self.front_sensor == 1:

                        self.move_forward()

                    else:

                        self.turn_left()

            x, y = self.position

        return array_map

    def explore_room(self):

        # convert the perimeter map to a 2D array

        array_map = self.convert_map()

        # find the starting position in the farthest left column

        start_found = False

        for j in range(len(array_map[0])):  # iterate through columns first

            for i in range(len(array_map)):  # then iterate through rows

                if array_map[i][j] == 1:
                    self.position = (i, j)

                    start_found = True

                    break

            if start_found:
                break

        while self.direction != 1:
            self.turn_left()

            print(self.direction)

        self.update_sensors(self.position[0], self.position[1])

        # find half way point of room

        halfway_col = len(array_map[0]) // 2

        # begin vacuuming!

        going_down = True

        current_col = self.position[1]

        while current_col < len(array_map[0]):

            if current_col < halfway_col:

                if going_down:

                    print("vac down")

                    array_map = self.move_down(array_map)

                    self.next_col_up(array_map)

                    going_down = False

                else:

                    print("vac up")

                    array_map = self.move_up(array_map)

                    self.next_col_down(array_map)

                    going_down = True

            else:

                if going_down:

                    print("vac down left")

                    array_map = self.move_down_left_bias(array_map)

                    # check for columns with 1's before moving to the next column

                    if (current_col + 1 < len(array_map[0]) and

                            any(array_map[i][current_col + 1] == 1

                                for i in range(len(array_map)))

                    ):
                        self.next_col_up(array_map)

                    going_down = False

                else:

                    print("vac up left")

                    array_map = self.move_up_left_bias(array_map)

                    # check for columns with 1's before moving to the next column

                    if (current_col + 1 < len(array_map[0]) and

                            any(array_map[i][current_col + 1] == 1

                                for i in range(len(array_map)))

                    ):
                        self.next_col_down(array_map)

                    going_down = True

            # update col

            current_col += 1

            # check for more columns with 1's

            if (current_col >= len(array_map[0]) or

                    all(array_map[i][current_col] != 1

                        for i in range(len(array_map)))

            ):
                print("Finished vacuuming the room")

                break

        return array_map

    def print_map(self, array_map):

        for row in array_map:
            print(' '.join(str(cell) for cell in row))

        print(f"Current Position: {self.position}")

        print("---")


# =========================================

# Main Code


room = Room(9)

rx = SmartVac(room)

rx.map_room()

print("map from vac")

for row in rx.perimeter_map:
    print(row)

print("----map of room----")

for row in room.layout:
    print(row)

array_map = rx.explore_room()

for row in room.layout:
    print(row)

print("vac map")

for row in array_map:
    print(row)