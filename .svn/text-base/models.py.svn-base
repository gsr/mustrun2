from google.appengine.ext import db

class Assignment(db.Model):
    title = db.StringProperty()
    descript = db.StringProperty()
    status = db.StringProperty()
    dueDate = db.DateTimeProperty()
    weight = db.IntegerProperty()
    section = db.StringProperty() #is the section ID
    docLink = db.StringProperty() #should this be a string or integer?
    created = db.DateTimeProperty()
    modified = db.DateTimeProperty()
    creator = db.StringProperty() #is the User ID
    public = db.BooleanProperty()

class Assignee(db.Model):
    assignment = db.StringProperty() #is the Assignment ID
    assignee = db.StringProperty() #is the User ID
    
class Section(db.Model):
    name = db.StringProperty()
    
class UserInfo(db.Model):
    uID = db.StringProperty() #User ID - is the key of the user - use the baked in users stuff
    prefSection = db.StringProperty() #is the Section ID
    phone = db.PhoneNumberProperty()
    
class DerivAssignment(db.Model):
    assignment = db.IntegerProperty() #is the Assignment ID
    derivative = db.IntegerProperty() #is the deriv Assignment ID
    
class Permissions(db.Model):
    uID = db.StringProperty() # - is NOT the key of UserInfo - is the key of users
    role = db.IntegerProperty()
    section = db.StringProperty() # used not for restricting people to editing a specific section, but for
    # telling the system which editors to email/notify when writers want to pick stories up. 

class PickUp(db.Model):
    uID = db.StringProperty()
    assignment = db.IntegerProperty()
    requested = db.DateTimeProperty()
    
class Defaults(db.Model):
    default_section = db.StringProperty()

class Desker(db.Model):
    name = db.StringProperty()
    section = db.StringProperty()
    date = db.DateTimeProperty()

class Testing(db.Model):
    permOff = db.BooleanProperty()