from opinion import Opinion
class Product:
    def __init__(self, id:str, name:str, photo_link:str, num_of_opinions:int):
        self.id = id
        self.name = name
        self.photo_link = photo_link
        self.num_of_opinions = num_of_opinions
    
    def update_product_data(self):
        #num_of_pluses:int, num_of_minuses:int, avg_rating:int
        pass

    def set_opinions(self, opinions:list[Opinion]):
        self.opinions = opinions