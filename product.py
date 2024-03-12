from opinion import Opinion
class Product:
    def __init__(self, id:str, name:str, photo_link:str, opinions:list[Opinion]):
        self.id = id
        self.name = name
        self.photo_link = photo_link
        self.opinions = opinions