from API import StartAPI
from db_seeder import seed_database, CreateTable

if __name__ == "__main__": 
    CreateTable()
    StartAPI()  