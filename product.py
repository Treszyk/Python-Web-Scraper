from opinion import Opinion
from stats import get_cons_pros, get_avg_rating
class Product:
    def __init__(self, id:str, name:str, photo_link:str, num_of_opinions:int):
        self.id = id
        self.name = name
        self.photo_link = photo_link
        self.num_of_opinions = num_of_opinions
    
    def update_product_data(self):
        #num_of_pluses:int, num_of_minuses:int, avg_rating:int
        pass

    def update_opinions(self, opinions:list[Opinion]):
        self.opinions = opinions
        cons_pros = get_cons_pros(self)
        self.num_of_pros = cons_pros[0]
        self.num_of_cons = cons_pros[1]
        self.avg_rating = get_avg_rating(self)