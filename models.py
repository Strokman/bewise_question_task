from requests import get


class Jserviceapihandler:

    def __init__(self, count):
        self.count = count
        self.__data = get(f"https://jservice.io/api/random?count={count}")

    # @property
    # def count(self):
    #     return self.__count
    #
    # @count.setter
    # def count(self, count):
    #     self.__count = get('count')

    def json_data(self):
        return self.__data.json()






