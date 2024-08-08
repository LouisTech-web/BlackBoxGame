def check_ray_path(start_pos, direction, board_size, ball_positions):
    x, y = start_pos
    dx, dy = direction
    path = []
    result_type = "Miss"  # Default result type

    # Assurez-vous que le rayon commence à une position valide
    if not (0 <= x < board_size and 0 <= y < board_size):
        print(f"Starting position {start_pos} is out of bounds.")
        return path, result_type

    while 0 <= x < board_size and 0 <= y < board_size:
        print(f"Verification de la position ({x}, {y})")  # Debugging line

        if (x, y) in ball_positions:
            result_type = "Hit"
            path.append((x, y))  # Include the position of the ball in the path
            print(f"Atome trouvé en ({x}, {y})")  # Debugging line
            break
        
        path.append((x, y))

        x += dx
        y += dy

        # Check if the ray has exited the board
        if not (0 <= x < board_size and 0 <= y < board_size):
            result_type = "Miss"
            print(f"Le laser est sorti du plateau ({x}, {y})")  # Debugging line
            break

    return path, result_type
