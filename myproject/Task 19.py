#Task 1
import json
from textwrap import indent


class Product:
    def __init__(self, name, price, quantity):
        self.name=name
        self.price=price
        self.quantity=quantity

    def transform(self):
        return {
            'Name': self.name,
            'Price': self.price,
            'Quantity': self.quantity
        }


product_list=[
    Product('Product1',2000,1),
    Product('Product2', 3000, 2),
    Product('Product3', 4000, 3),
    Product('Product4', 5000, 4),
    ]



def serialization(products,file):

    list_=list()
    for i in products:
        result=i.transform()
        list_.append(result)

    with open (file,'w') as file_:
        json.dump(list_,file_, indent=4)


def deserialization(file):
    with open (file,'r') as file_:
        result=json.load(file_)
        list_=list()
        for i in result:
            product_=Product(i["Name"],i["Price"],i["Quantity"])
            list_.append(product_)
        return list_


serialization(product_list,'Product.json')
des_result=deserialization('Product.json')

for product in des_result:
    print(f"Name: {product.name}, Price: {product.price}, Quantity: {product.quantity}")


#Task 2

def movie(file):
    with open(file, 'r') as file_:
        movies = json.load(file_)

    new_version = list()

    for i in movies[0]['results']:
        year = int(i.get("release_date", "").split('-')[0])
        genre = i.get("genres", [])
        if year > 2000 and 'Crime' in genre:
            updated_genre = list()
            for j in genre:
                if "Crime" in j:
                    new_genre = j.replace("Crime", "New_Crime")
                    updated_genre.append(new_genre)
                else:
                    updated_genre.append(j)
            i['genres'] = updated_genre
            new_version.append(i)

        elif year < 2000 and 'Drama' in genre:
            updated_genre = list()
            for j in genre:
                if 'Drama' in j:
                    new_genre = j.replace('Drama', 'Old_Drama')
                    updated_genre.append(new_genre)
                else:
                    updated_genre.append(j)
            i["genres"] = updated_genre
            new_version.append(i)

        elif year == 2000:
            updated_genre = genre + ['New Century']
            i["genres"] = updated_genre
            new_version.append(i)

    with open(file, 'w') as file_:
        json.dump(new_version, file_, indent=4)

movie("C:/Users/Elene/Desktop/movies.json")
