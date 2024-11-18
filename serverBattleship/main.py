
import socket


def create_empty_table():
    return [["~"] * 10 for _ in range(10)]


def placeShip(client_socket, board, size, shipSize):
    placed = False
    while not placed:
        try:
            client_socket.send("Pick an orientation: horizontal(H) or vertical(V):\n".encode())
            orientation = client_socket.recv(1024).decode().strip().upper()
            client_socket.send("Keep in mind that the table starts from index 1,1\n".encode())
            client_socket.send("Pick the starting point of your ship (ex: 2,3 for row 2 column 3):\n".encode())

            startPoint = client_socket.recv(1024).decode().strip()
            row, col = map(int, startPoint.split(','))
            if not (0 <= row < size and 0 <= col < size):
                client_socket.send("Starting point out of bounds. Enter valid coordinates.\n".encode())
                continue
            row -= 1
            col -= 1

            if orientation == "H":
                client_socket.send("Pick a direction: left(L) or right(R):\n".encode())
                direction = client_socket.recv(1024).decode().strip().upper()
                if direction == "L":
                    if col - shipSize + 1 >= 0 and all(board[row][c] == "~" for c in range(col, col - shipSize, -1)):
                        for c in range(col, col - shipSize, -1):
                            board[row][c] = "S"
                        placed = True
                        client_socket.send("Ship placed successfully!\n".encode())
                    else:
                        client_socket.send("Invalid position! Ship can't be placed here. Try again.\n".encode())
                elif direction == "R":
                    if col + shipSize <= size and all(board[row][c] == "~" for c in range(col, col + shipSize)):
                        for c in range(col, col + shipSize):
                            board[row][c] = "S"
                        placed = True
                        client_socket.send("Ship placed successfully!\n".encode())
                    else:
                        client_socket.send("Invalid position! Ship can't be placed here. Try again.\n".encode())
                else:
                    client_socket.send("Invalid direction. Please choose L or R.\n".encode())
            elif orientation == "V":
                client_socket.send("Pick a direction: up(U) or down(D):\n".encode())
                direction = client_socket.recv(1024).decode().strip().upper()
                if direction == "U":
                    if row - shipSize + 1 >= 0 and all(board[r][col] == "~" for r in range(row, row - shipSize, -1)):
                        for r in range(row, row - shipSize, -1):
                            board[r][col] = "S"
                        placed = True
                        client_socket.send("Ship placed successfully!\n".encode())
                    else:
                        client_socket.send("Invalid position! Ship can't be placed here. Try again.\n".encode())
                elif direction == "D":
                    if row + shipSize <= size and all(board[r][col] == "~" for r in range(row, row + shipSize)):
                        for r in range(row, row + shipSize):
                            board[r][col] = "S"
                        placed = True
                        client_socket.send("Ship placed successfully!\n".encode())
                    else:
                        client_socket.send("Invalid position! Ship can't be placed here. Try again.\n".encode())
                else:
                    client_socket.send("Invalid direction. Please choose U or D.\n".encode())
            else:
                client_socket.send("Invalid orientation. Please choose H or V.\n".encode())
        except (ValueError, IndexError):
            client_socket.send("Invalid input. Please try again.\n".encode())
            continue


def main():
    table0 = create_empty_table()
    table1 = create_empty_table()
    hidden_table0 = create_empty_table()
    hidden_table1 = create_empty_table()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.214.14",6969))  # Replace with your server IP
    server.listen(2)

    print("Waiting for clients to connect...")
    client_sockets = []
    for _ in range(2):
        client_socket, client_address = server.accept()
        print(f"Client {client_address} connected.")
        client_sockets.append(client_socket)

    print("Both clients connected. Starting the game.")
    ships = int(input("How many ships will each of the players place on their table?\n"))

    for i in range(2):
        current_client = client_sockets[i]
        current_table = table0 if i == 0 else table1
        current_client.send("Place your ships on the board.\n".encode())
        for j in range(ships):
            current_client.send(f"Place your {j+1}-length boat.\n".encode())
            placeShip(current_client, current_table, 10, j+1)

        current_client.send("Here is your table with the ships placed:\n".encode())
        current_client.send("\n".join(" ".join(row) for row in current_table).encode())
        current_client.send("\n\n".encode())

    while True:
        for i in range(2):
            current_client = client_sockets[i]
            opponent_table = table1 if i == 0 else table0
            current_hidden_table = hidden_table0 if i == 0 else hidden_table1

            current_client.send("\n".join(" ".join(row) for row in current_hidden_table).encode())
            current_client.send("\nYour turn (Write it this way 'x,y'):\n".encode())

            try:
                move = current_client.recv(1024).decode().strip()
                x, y = map(int, move.split(","))
                x -= 1
                y -= 1

                if opponent_table[x][y] == "S":
                    opponent_table[x][y] = "⯐"
                    current_hidden_table[x][y] = "⯐"
                    result = "Hit!"
                else:
                    opponent_table[x][y] = "X"
                    current_hidden_table[x][y] = "X"
                    result = "Miss!"

                current_client.send(f"You {result}\n".encode())
                other_client = client_sockets[1 - i]
                other_client.send(f"Opponent's move at ({x+1},{y+1}) was a {result}\n".encode())

                if not any("S" in row for row in opponent_table):
                    current_client.send("You win!\n".encode())
                    other_client.send("You lose!\n".encode())
                    server.close()
                    return
            except (ValueError, IndexError):
                current_client.send("Invalid move. Try again.\n".encode())


if __name__ == "__main__":
    main()


