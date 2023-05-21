import os

from database import createDatabase
from database.createDatabase import csgo_cur
from database.handler.updateTargets import update_buy_offers


def main():

    # Create database if not available or if env is set
    if (not os.path.isfile("CSGO.db")) or (bool(os.getenv('DATABASE_RESET'))):
        print("Created new Database")
        createDatabase.createDatabase()

    update_buy_offers()

if __name__ == '__main__':
    main()
