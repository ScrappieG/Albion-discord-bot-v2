import sqlite3

def execute_query(query:str, conn:sqlite3.Connection)->list:
    c=conn.cursor()
    c.execute(query)
    result=c.fetchall()
    c.close()

def add_member(member_id:str, conn:sqlite3.Connection)->list:
    c=conn.cursor()
    c.execute(f'INSERT INTO users (discord_id) values ({member_id})')
    conn.commit()
    conn.close()

def remove_member(member_id:str, conn:sqlite3.Connection)->list:
    c=conn.cursor()
    c.execute(f'DELETE FROM users WHERE(discord_id) LIKE ({member_id})')
    conn.commit()
    conn.close()

def is_member(member_id:str, conn:sqlite3.Connection)->list:
    c=conn.cursor()
    if c.execute(f'SELECT discord_id FROM users WHERE discord_id like {member_id}') == None:
        print('none')
        return False
    else:
        for row in c.execute(f'SELECT discord_id FROM users WHERE discord_id like {member_id}'):
            print(row)
            print(row[0])
            print(member_id)
            if row[0] == member_id:
                conn.close
                return True
    conn.close()
    print('end return')
    return False

def find_guild_balance(member_id:str, conn:sqlite3.Connection)->list:
    c=conn.cursor()
    c.execute(f'SELECT guild_silver_balance FROM users WHERE(discord_id) LIKE ({member_id})')
    result = c.fetchall()
    error_value = -1
    if result == None:
        print(f'error occured with {member_id} balance')
        return error_value
    else:
        conn.close
        result = result[0]
        result = result[0]
        return result

def update_guild_balance(member_id:str, ammount:int, conn:sqlite3.Connection)->list:
    c=conn.cursor()
    c.execute(f'UPDATE users SET guild_silver_balance = {int(ammount)} WHERE discord_id = {member_id}')
    conn.commit()
    conn.close()
    return

def find_all_balance(conn:sqlite3.Connection)->list:
    c=conn.cursor()
    c.execute(f'SELECT guild_silver_balance, discord_id FROM users WHERE(guild_silver_balance) NOT LIKE 0 ORDER BY guild_silver_balance DESC')
    result = c.fetchall()
    print(result)
    error_value = -1
    if result == None:
        print(f'error occured')
        return error_value
    else:
        conn.close
        return result
