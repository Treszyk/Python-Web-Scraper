def get_cons_pros(product) -> list:
    opinions = product.opinions
    pros = 0
    cons = 0
    for opinion in opinions:#liczba wad i zalet
        pros += len(opinion.plus)
        cons += len(opinion.minus)
    return [pros, cons]

def get_avg_rating(product) -> float:
    opinions = product.opinions
    suma = 0
    for opinion in opinions:#liczba wad i zalet
        suma += opinion.score
    return suma/len(opinions)
