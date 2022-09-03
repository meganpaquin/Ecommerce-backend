import pymongo
import certifi

connection = "mongodb+srv://ecommerce_trial:uV1aI5iUM98GTXfN@ecommerce.ftlcple.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection, tlsCAFile=certifi.where())

database = client.get_database("Ecommerce")

