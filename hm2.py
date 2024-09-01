from telethon.sync import TelegramClient
from telethon import functions, types, events, Button, errors

# Leave api_id and api_hash empty
client = TelegramClient('sessions/robot', api_id, api_hash)
client.start(bot_token=bot_token)
async def main():
    # Log in using your phone number
    await client.start(phone_number='+989218750331')

    # After login, you can save the session string
    session_string = client.session.save()
    print("Session string:", session_string)
    
    # You can now use the session string for future logins
    
with client:
    client.loop.run_until_complete(main())



async def get_grid_state(bot):
    messages = await client.get_messages(bot, limit=1)
    grid = parse_grid(messages[0].message)  # Implement parse_grid according to your game
    return grid

def parse_grid(message):
    grid = []
    for line in message.splitlines():
        if line.strip():  # Skip empty lines
            grid.append([int(char) for char in line if char.isdigit()])
    return grid

def find_best_move(grid):
    best_move = None
    best_score = 0
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if col < len(grid[row]) - 1:
                score = simulate_move(grid, row, col, row, col + 1)  # Swap right
                if score > best_score:
                    best_score = score
                    best_move = (row, col, row, col + 1)

            if row < len(grid) - 1:
                score = simulate_move(grid, row, col, row + 1, col)  # Swap down
                if score > best_score:
                    best_score = score
                    best_move = (row, col, row + 1, col)
    
    return best_move

def simulate_move(grid, row1, col1, row2, col2):
    new_grid = [row[:] for row in grid]
    new_grid[row1][col1], new_grid[row2][col2] = new_grid[row2][col2], new_grid[row1][col1]
    score = calculate_score(new_grid)  # Implement this based on game rules
    return score

def calculate_score(grid):
    score = 0
    return score

async def execute_move(bot, move):
    row1, col1, row2, col2 = move
    move_command = f"swap {row1},{col1} with {row2},{col2}"
    await client.send_message(bot, move_command)

async def claim_rewards(bot):
    messages = await client.get_messages(bot, limit=1)
    buttons = messages[0].buttons
    if buttons:
        await buttons[0][0].click()
        print("Claimed rewards!")

async def play_hexa_puzzle():
    await client.start(phone_number)
    bot = await client.get_entity('HamsterKombatBot')
    
    start_time = time.time()
    
    while True:
        grid = await get_grid_state(bot)
        if not grid:
            break
        
        best_move = find_best_move(grid)
        if best_move:
            await execute_move(bot, best_move)
            await asyncio.sleep(1)  # Wait time between moves
        else:
            break  # No more valid moves
        
        # Check if an hour has passed
        if time.time() - start_time > 3600:
            print("Time's up! Exiting puzzle to claim rewards.")
            await client.send_message(bot, '/quit')
            await asyncio.sleep(2)  # Wait for the exit to process
            await claim_rewards(bot)
            start_time = time.time()  # Reset the timer
            await asyncio.sleep(2)  # Small delay before restarting the puzzle

            # Restart the puzzle
            await client.send_message(bot, '/minigames')
            await asyncio.sleep(2)
            messages = await client.get_messages(bot, limit=1)
            buttons = messages[0].buttons
            if buttons:
                await buttons[0][0].click()
                print("Restarted Hexa Puzzle")

with client:
    client.loop.run_until_complete(play_hexa_puzzle())
