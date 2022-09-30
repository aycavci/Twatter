from neo4j import GraphDatabase
import re

class Database:
    def __init__(self):
        print("neo4j username:")
        username=input()
        print("neo4j password:")
        password=input()
        self.driver = GraphDatabase.driver("bolt://localhost:7420", auth=(username, password))

    def kill(self):
        self.driver.close()

    ###########################################################################
    # CREATE
    ###########################################################################

    def create_user(self, username, password, bio=''):
        """1. For First Time User Registration
        """
        sesh=self.driver.session()
        try:
            sesh.run("CREATE (:User {username:'"+username+"', password:'"+password+"', bio:'"+bio+"'})")
            return True
        except:
            return False

    def create_tweet(self, username, tweet_content):
        sesh=self.driver.session()
        t_id = sesh.run("MATCH (n:User {username:'" + username +"'})"
                 "CREATE (n)-[:POSTED]->(t:Tweet {"
                 "content: '" + tweet_content + "', id:n.username+'_'+timestamp(),"
                 "time: timestamp()}) RETURN t.id").data()[0]['t.id']
        # extract hashtags
        print (t_id)
        hashtags = re.findall(pattern=u"#\w+", string=tweet_content)
        for h in hashtags:
            sesh.run("MATCH (t:Tweet {id:'" + t_id+"'})"
                     "MERGE (h:Hashtag {name:'" + h+"'})"
                     "MERGE (t)-[:TAGGED]->(h)")


    def create_like(self, username, tweet_id):
        sesh=self.driver.session()
        sesh.run("MATCH (n:User {username:'" + username +"'}),"
                       "(t:Tweet {id:'" + tweet_id + "'})"
                 "CREATE (n)-[:LIKES]->(t)")

    def create_retweet(self, username, tweet_id):
        sesh=self.driver.session()
        sesh.run("MATCH (n:User {username:'" + username +"'}),"
                       "(t:Tweet {id:'" + tweet_id + "'})"
                 "CREATE (n)-[:RETWEETED {time:timestamp()}]->(t)")

    def create_follow(self, follower_uname, followee_uname):
        sesh=self.driver.session()
        sesh.run("MATCH (a:User {username:'" + follower_uname +"'}),"
                 "      (b:User {username:'" + followee_uname+"'})"
                 "MERGE (a)-[:FOLLOWS]->(b)")

    ###########################################################################
    # READ
    ###########################################################################

    def get_users_as_search(self, search, limit=25):
        sesh=self.driver.session()
        users =sesh.run("MATCH (a:User)"
                        "WHERE a.username=~'.*" + search +".*'"
                        "RETURN a.username as user,"
                        "a.bio as bio "
                        "LIMIT " + str(limit)).data()
        return users

    def get_followers(self, username, limit=25):
        sesh=self.driver.session()
        users =sesh.run("MATCH (a:User)<-[:FOLLOWS]-(b:User)"
                        "WHERE a.username='" + username +"' "
                        "RETURN b.username as user,"
                        "b.bio as bio "
                        "LIMIT " + str(limit)).data()
        print (str(users))
        return users

    def get_followees(self, username, limit=25):
        sesh=self.driver.session()
        users =sesh.run("MATCH (a:User)-[:FOLLOWS]->(b:User)"
                        "WHERE a.username='" + username +"' "
                        "RETURN b.username as user,"
                        "b.bio as bio "
                        "LIMIT " + str(limit)).data()
        print (str(users))
        return users

    def get_num_retweets(self, tweet_id):
        pass

    def get_tweets_from_user(self, username):
        sesh=self.driver.session()
        q = "MATCH (t:Tweet)<-[:POSTED]-(u:User {username:'" + username + """'})
        OPTIONAL MATCH (t)<-[l:LIKES]-(), (t)<-[r:RETWEETED]-()
        RETURN t.content as content, t.id as id,
        datetime({epochmillis:t.time}) as time,
        count(l) as likes, count(r) as rts, u.username as username
        """
        print (q)
        tweets=sesh.run(q)
        return tweets

    def get_tweets_from_followees(self, username):
        pass

    ###########################################################################
    # UPDATE
    ###########################################################################
    def update_password(self, username, new_password):
        pass

    def update_bio(self, username, bio):
        pass

    def update_photo(self, username, photo_url):
        pass

    ###########################################################################
    # DELETE
    ###########################################################################

    ###########################################################################
    # SECURITY & MISC
    ###########################################################################
    def valid_login(self, username, password):
        """ 2. Login Functionality
        """
        sesh = self.driver.session()
        obj = sesh.run("MATCH (n:User {username:'"+username+"', password:'"+password+"'}) RETURN n")
        return (len(obj.data()) == 1)

    def query(self, query_string):
        """
            XXX USE CONSERVATIVELY XXX
        """
        sesh = self.driver.session()
        return sesh.run(query_string)
