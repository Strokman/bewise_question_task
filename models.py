from requests import get


class Jserviceapihandler:

    def __init__(self, count):
        self.count = count
        self.__data = get(f"https://jservice.io/api/random?count={count}")

    def json_data(self):
        return self.__data.json()




