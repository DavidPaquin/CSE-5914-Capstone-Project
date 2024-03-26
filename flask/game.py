import uuid

class Game:
    def __init__(self, id: uuid.UUID, start_article: str, end_article: str):
        self.id = id #The game id
        self.history = [start_article] #A history of articles the player has visited
        self.start_article = start_article
        self.end_article = end_article
        self.choices = [] #The articles that could be chosen for the next turn

    def __str__(self):
        return f"ID: {self.id} | Start Article ID: {self.start_article} | End Article ID: {self.end_article} | History: {self.history} | Choices: {self.choices}"

    def hop(self, article_id: str):
        if article_id not in self.choices:
            #The requested hop is to an article that isn't a choice
            return False
        self.history.append(article_id)
        return True
    
    def check_win(self, article_id: str):
        return article_id == self.end_article
