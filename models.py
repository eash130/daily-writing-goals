from google.appengine.ext import ndb

class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    username = ndb.StringProperty()

class Writing(ndb.Model):
    text = ndb.StringProperty()
    user_id = ndb.StringProperty()
