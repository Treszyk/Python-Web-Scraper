def get_cons_pros(product) -> list:
    opinions = product.opinions
    pros = 0
    cons = 0
    for opinion in opinions:
        pros += len(opinion.plus)
        cons += len(opinion.minus)
    return [pros, cons]

def get_avg_rating(product) -> float:
    opinions = product.opinions
    suma = 0
    for opinion in opinions:
        suma += opinion.score
    return round(suma/len(opinions), 1)
