class Opinion:
    def __init__(self, extracted_details):
        self.load_details(extracted_details)
    def load_details(self, extracted_details) -> None:
        #id:str, author:str, recommended:bool, score:int, verified:bool, review_date:str, buy_date:str, likes:int, dislikes:int, content:str, plus:int, minus:int
        self.id = extracted_details['id']
        self.author = extracted_details['author']
        self.recommended = extracted_details['recommended']
        self.score = extracted_details['score']
        self.verified = extracted_details['verified']
        self.review_date = extracted_details['review_date']
        self.buy_date = extracted_details['buy_date']
        self.likes = extracted_details['likes']
        self.dislikes = extracted_details['dislikes']
        self.content = extracted_details['content']
        self.plus = extracted_details['plus']
        self.minus = extracted_details['minus']
