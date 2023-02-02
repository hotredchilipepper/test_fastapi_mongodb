from fastapi import FastAPI
from pathlib import Path
from custom_logging import CustomizeLogger
from pymongo import MongoClient
import schemas
import json

with open("employees.json", "r") as jsr:
    data = json.load(jsr)

client = MongoClient("localhost", 27017)
database = client["persons_db"]
persons = database.persons

ids = persons.insert_many(data).inserted_ids
print(len(ids))


config_path=Path(__file__).with_name("logging_config.json")

# Инициализация приложения FastApi.
def create_app() -> FastAPI:
    app = FastAPI(title='Test task', debug=False)
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app

app = create_app()


@app.post("/api/v1/getPersons", response_model=schemas.ResponseStatus)
async def get_persons(data: schemas.GetPersons):
    """Получение пользователей по заданному параметру.

        Params:
            email - str, поиск записи пользователя по почте
            sort - 0/1 где 0 - поиск по почте, 1 поиск по остальным параметрам 
            company - str,
            job_title - str,
            gender - str,
    """
    if data.sort == "0":
        if data.email is None:
            return {"status": "0", "data": "Параметр email не был указан"}
        else:
            data_person = persons.find_one({"email": data.email})
            if data_person is None:
                return {"status": "2", "data": "Данного пользователя не сущетвует"}
            data_person['_id'] = str(data_person['_id'])
            return {"status": "1", "data": data_person}

    return {"status": "11", "data": "Ok"}

    #TODO
    # На моменте рещения тестового задания я не мог определиться по каким параметрам осущетсвлять сортровку,
    # не хотел тут городить очень много некрасивого кода, чтобы обработать всевозможные комбинации фильтров
    # по которым бы отбирались сотрудники, ибо задача потавлена в общих чертах, и я решил остановиться на этой 
    # реализации. Если бы ТЗ было бы конкретнее то и решение было бы соответсвующее.
    # Отталкиваясь от того какие поля есть в коллекции то сортировку(выборку) можно сделать по многим из них и 
    # соответственно из множества их комбинаций и пересечений.


