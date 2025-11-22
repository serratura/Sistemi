import asyncio
import tornado.web
from pymongo import AsyncMongoClient
import json
from bson import ObjectId
from bson import json_util

"""
PUBLISHERS
[
  {
    "name": "Einaudi",
    "founded_year": 1933,
    "country": "Italia"
  },
  {
    "name": "Penguin Random House",
    "founded_year": 2013,
    "country": "USA"
  },
  {
    "name": "Mondadori", 
    "founded_year": 1907,
    "country": "Italia"
  },
  {
    "name": "HarperCollins",
    "founded_year": 1989,
    "country": "USA"
  },
  {
    "name": "Feltrinelli",
    "founded_year": 1954,
    "country": "Italia"
  }
]
Invoke-WebRequest -Uri "http://localhost:8888/publishers/ID_DA_MODIFICARE" `
    -Method Put `
    -Body '{"_id": "69182d76008aab5e7d9dc2a1", "name":"NuovoNome", "founded_year":2000, "country":"Italia"}' `
    -ContentType "application/json"

BOOKS

[
  {
    "title": "Il barone rampante",
    "author": "Italo Calvino",
    "genre": "Romanzo",
    "year": 1957,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc29d")
  },
  {
    "title": "Se una notte d'inverno un viaggiatore",
    "author": "Italo Calvino",
    "genre": "Romanzo",
    "year": 1979,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc29d")
  },
  {
    "title": "Il nome della rosa",
    "author": "Umberto Eco",
    "genre": "Giallo",
    "year": 1980,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc29d")
  },
  {
    "title": "Il codice da Vinci",
    "author": "Dan Brown",
    "genre": "Giallo",
    "year": 2003,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc29e")
  },
  {
    "title": "Harry Potter e la pietra filosofale",
    "author": "J.K. Rowling",
    "genre": "Fantasy",
    "year": 1997,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc29e")
  },
  {
    "title": "Il signore degli anelli",
    "author": "J.R.R. Tolkien",
    "genre": "Fantasy",
    "year": 1954,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc29e")
  },
  {
    "title": "1984",
    "author": "George Orwell",
    "genre": "Romanzo",
    "year": 1949,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc29f")
  },
  {
    "title": "Hunger Games",
    "author": "Suzanne Collins",
    "genre": "Fantasy",
    "year": 2008,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc29f")
  },
  {
    "title": "La ragazza del treno",
    "author": "Paula Hawkins",
    "genre": "Giallo",
    "year": 2015,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc29f")
  },
  {
    "title": "Harry Potter e il prigioniero di Azkaban",
    "author": "J.K. Rowling",
    "genre": "Fantasy",
    "year": 1999,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc2a0")
  },
  {
    "title": "Il piccolo principe",
    "author": "Antoine de Saint-Exupéry",
    "genre": "Romanzo",
    "year": 1943,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc2a0")
  },
  {
    "title": "Il vecchio e il mare",
    "author": "Ernest Hemingway",
    "genre": "Romanzo",
    "year": 1952,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc2a0")
  },
  {
    "title": "Sostiene Pereira",
    "author": "Antonio Tabucchi",
    "genre": "Romanzo",
    "year": 1994,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc2a1")
  },
  {
    "title": "La ragazza del treno",
    "author": "Paula Hawkins",
    "genre": "Giallo",
    "year": 2015,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc2a1")
  },
  {
    "title": "Cecità",
    "author": "José Saramago",
    "genre": "Romanzo",
    "year": 1995,
    "publisher_id": ObjectId("69182d76008aab5e7d9dc2a1")
  }
]

"""


class PublisherHandler(tornado.web.RequestHandler):
    async def get(self, publisher_id=None):
        self.set_header("Content-Type", "application/json")
        name = self.get_query_argument("name", None)
        year = self.get_query_argument("founded_year", None)
        country = self.get_query_argument("country", None)
        query = {}

        if publisher_id:
            query["_id"] = ObjectId(publisher_id)
        if name:
            query["name"] = name
        if year:
            query["founded_year"] = year
        if country:
            query["country"] = country

        found = []
        documents = publishers_collection.find(query)
        async for document in documents:
            found.append(document)
        self.write(json_util.dumps(found))

    async def post(self):
        self.set_header("Content-Type", "application/json")
        try:
            data = tornado.escape.json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write({"errore": ""})
            return

        if not ("founded_year" in data.keys()) and not data["founded_year"]:
            self.set_status(400)
            self.write({"errore": "parametri errati"})
            return
        if not ("name" in data.keys()) and not data["name"]:
            self.set_status(400)
            self.write({"errore": "parametri errati"})
            return
        if not ("country" in data.keys()) and not data["country"]:
            self.set_status(400)
            self.write({"errore": "parametri errati"})
            return

        await publishers_collection.insert_one(data)
        found = []
        documents = publishers_collection.find({})
        async for document in documents:
            found.append(document)
        self.write(json_util.dumps(found))

    async def put(self, publisher_id):
        self.set_header("Content-Type", "application/json")

        try:
            data = tornado.escape.json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write({"errore": "JSON non valido"})
            return
        try:
            result = await publishers_collection.update_one(
                {"_id": ObjectId(publisher_id)},
                {"$set": data}
            )
        except Exception:
            self.write("Errore nell'id")
            self.set_status(400)
            return
        self.write({
            "matched": result.matched_count,
            "modified": result.modified_count
        })

    async def delete(self, publisher_id):
        self.set_header("Content-Type", "application/json")

        try:
            data = tornado.escape.json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write({"errore": "JSON non valido"})
            return
        try:
            result = await publishers_collection.delete_one(
                {"_id": ObjectId(publisher_id)}
            )
        except Exception:
            self.write("Errore nell'id")
            self.set_status(400)
            return

        found = []
        documents = publishers_collection.find()
        async for document in documents:
            found.append(document)
        self.write(json_util.dumps(found))



class BooksHandler(tornado.web.RequestHandler):
    async def get(self, id):
        id = int(id)
        prodotto = None
        for p in products:
            if p["id"] == id:
                prodotto = p
                break
        if not prodotto:
            self.set_status(404)
            self.write("Prodotto non trovato")
            return

    def post(self, id):
        global products
        id = int(id)
        prodotto = None
        for p in products:
            if p["id"] == id:
                prodotto = p
                break

        if not prodotto:
            self.set_status(404)
            self.write("Prodotto non trovato")
            return

        prodotto["nome"] = self.get_argument("nome")
        prodotto["categoria"] = self.get_argument("categoria")
        prodotto["prezzo"] = float(self.get_argument("prezzo"))
        prodotto["disponibile"] = self.get_argument("disponibile", None) is not None

        self.redirect("/products")


def make_app():
    return tornado.web.Application([
        (r"/publishers", PublisherHandler),
        (r"/publishers/([0-9a-fA-F]{24})", PublisherHandler),
        (r"/publishers/([0-9a-fA-F]{24})/books", BooksHandler),
        (r"/publishers/([0-9a-fA-F]{24})/books/{book_id}", BooksHandler),
    ], debug=True)


async def main(shutdown_event):
    app = make_app()
    app.listen(8888)
    print("Server attivo su http://localhost:8888/publishers")
    await shutdown_event.wait()
    print("Chiusura server...")


if __name__ == "__main__":
    client = AsyncMongoClient("mongodb://localhost:27017")
    db = client["test"]
    publishers_collection = db["Publisher"]

    books_collection = db["books"]
    shutdown_event = asyncio.Event()
    try:
        asyncio.run(main(shutdown_event))
    except KeyboardInterrupt:
        shutdown_event.set()
