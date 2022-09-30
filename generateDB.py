from neo4j import GraphDatabase
import random as r

driver = GraphDatabase.driver("bolt://localhost:7420", auth=('neo4j', 'neo4j'))

def populate_users_from_csv():
    sesh = driver.session()
    lines = open("MOCK_DATA.csv").readlines()

    for line in lines[1:]:
        i, u, p, b, pp = line.split(',')
        sesh.run("CREATE (:User {id:"+i+", username:'"+u+"', password:'"+p+"', bio:'"+b+"', photo:'"+pp[:-1]+"'})")


def generate_follows(n=100):
    sesh = driver.session()
    for i in range(n):
        a_id = r.randint(1, 1000)
        b_id = r.randint(1, 1000)
        while (b_id==a_id):
            b_id=r.randint(1, 1000)
        
        sesh.run("MATCH (a:User {id:" + str(a_id)+"}),"
                 "      (b:User {id:" + str(b_id)+"})"
                 "MERGE (a)-[:FOLLOWS]->(b)")
        print(i, ":", str(a_id), "->", str(b_id))

def close():
    driver.close()

if __name__=="__main__":
    populate_users_from_csv()
    generate_follows(222)
