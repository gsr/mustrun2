#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
import os
import urllib
import gdata.auth
import gdata.gauth
import gdata.docs.client
import gdata.docs.data
import gdata.docs.service
import gdata.alt.appengine
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import memcache


from aeoid import middleware, users
from django.utils import simplejson as json
from time import time
from datetime import *
from models import *


SETTINGS = {
  'APP_NAME': 'cornellsun-mustrun-v1',
  'CONSUMER_KEY': 'mustrun.cornellsun.com',
  'CONSUMER_SECRET': 'XGdnYd9TZrs2Zrv4ZdubeN8a',
  'SIG_METHOD': gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
  'SCOPES': ['https://docs.google.com/feeds/']
  }

def get_ass_from_memcache(assignment_id):
    assignment = memcache.get(assignment_id)
    if assignment is not None:
        return assignment
    else:
        k = db.Key(encoded=assignment_id)
        assignment = db.get(k)
        if assignment is not None:
            memcache.set(assignment_id, assignment)
        return assignment

def get_permissions(uID):
    perms = memcache.get(uID)
    if perms is not None:
        return perms
    else:
        pID = Permissions.all().filter("uID =",uID).fetch(1)    
        if pID: #empty lists are false, non-empty ones are "true"
            #k = db.Key(encoded=pID[0].key()) I don't think you need this line, not sure though.
            perms = db.get(pID[0].key())
            if perms is not None:
                memcache.set(uID,perms) #in memcache, key the perms to the user key, not the key of the permissions entity, that way it's easier to get out since we're passing the uID in
            return perms
        else:
            return None

def get_assigned(aID,uID):
    assigned = memcache.get(aID+uID)
    if assigned is not None:
        return assigned
    else:
        assignedID = Assignee.all().filter("assignee =", uID).filter("assignment =", aID).fetch(1).key()
        #k = db.Key(encoded=assignedID) ditto above.  also need to check if we got anything out of Assignee
        #like we did above
        assigned = db.get(assignedID[0].key)
        if assigned is not None:
            memcache.set(aID+uID,assigned)
        return assigned

def get_section_list():
    section_list = []
    sections = Section.all().fetch(1000)
    return sections

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)
#This function found at http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models
def to_dict(model):
    output = {}

    for key, prop in model.properties().iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime):
            output[key] = value.strftime("%Y-%m-%d")
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output

#This function found at http://code.activestate.com/recipes/521915-start-date-and-end-date-of-given-week/
def get_week_details(_weekNo, _Year, _weekStart):
    rslt = []
    janOne = datetime.strptime('%s-01-01' % _Year, '%Y-%m-%d')
    dayOfFirstWeek = ((7-int((janOne.strftime("%u")))+ int(_weekStart)) % 7)
    if dayOfFirstWeek == 0:
        dayOfFirstWeek = 7
    dateOfFirstWeek = datetime.strptime('%s-01-%s' % (_Year, dayOfFirstWeek), '%Y-%m-%d')
    dayOne = datetime( dateOfFirstWeek.year, dateOfFirstWeek.month, dateOfFirstWeek.day )
    daysToGo = 7*(int(_weekNo)-1)
    lastDay = daysToGo+6
    dayX = dayOne + timedelta(days = daysToGo)
    dayY = dayOne + timedelta(days = lastDay)
    resultDateX = datetime.strptime('%s-%s-%s' % (dayX.year, dayX.month, dayX.day), '%Y-%m-%d')
    resultDateY = datetime.strptime('%s-%s-%s' % (dayY.year, dayY.month, dayY.day), '%Y-%m-%d')
    rslt.append(resultDateX)
    rslt.append(resultDateY)
    return rslt

#used to simulate someone being logged in.  On the local server, OpenID doesn't work, so we use this to bypass permissions.
def get_testing():
    testing = Testing.all().fetch(1000)
    if testing:
        return True
    else:
        return False

class AppsFederationHandler(webapp.RequestHandler):
    #moo
    """Handles openid login for federated Google Apps Marketplace apps."""
    def get(self):
        domain = self.request.get("domain")
        if not domain:
            self.redirect("/")
        else:
            openid_url = "https://www.google.com/accounts/o8/site-xrds?hd=" + domain
            self.redirect("%s?openid_url=%s" %
                    (users.OPENID_LOGIN_PATH, urllib.quote(openid_url)))

class GetOauthToken(webapp.RequestHandler):
    def get(self):
        user_id = users.get_current_user().user_id()
        saved_request_token = gdata.gauth.AeLoad("tmp_"+user_id)
        gdata.gauth.AeDelete ("tmp_" + user_id)
        request_token = gdata.gauth.AuthorizeRequestToken(saved_request_token, self.request.uri)
        #upgrade the token
        access_token = client.GetAccessToken(request_token)
        #save the upgraded token
        gdata.gauth.AeSave(access_token, user_id)
        self.redirect('/test')     

#Doesn't work currently.
class Test(webapp.RequestHandler):
    def get(self):
        TOKEN = gdata.gauth.AeLoad(users.get_current_user().user_id())
        if TOKEN:
            client = gdata.docs.client.DocsClient(source=SETTINGS['APP_NAME'])
            client.auth_token = gdata.gauth.AeLoad(users.get_current_user().user_id()) #could try to put back as TOKEN?
            
            self.response.out.write('moo baby')
            client.ssl = True
            feed = client.GetDocList(auth_token=gdata.gauth.AeLoad(users.get_current_user().user_id())) #auth_token=TOKEN
            self.response.out.write(feed)
            self.response.out.write('moo boobob')
            self.response.headers['Content-Type'] = 'text/plain'
            for entry in feed.entry:
                self.response.out.writeln(entry.title.text)
        else:
            # Get unauthorized request token
            gdata.gauth.AeDelete(users.get_current_user().user_id())
            client = gdata.docs.client.DocsClient(source=SETTINGS['APP_NAME'])
            client.ssl = True # Force communication through HTTPS

            oauth_callback_url = ('http://%s/get_oauth_token' %
                                  self.request.host)

            request_token = client.GetOAuthToken(
                SETTINGS['SCOPES'], oauth_callback_url, SETTINGS['CONSUMER_KEY'],
                consumer_secret=SETTINGS['CONSUMER_SECRET'])
            gdata.gauth.AeSave(request_token, "tmp_"+users.get_current_user().user_id())
            # Authorize request token
            domain = None#'cornellsun.com'
            self.redirect(str(request_token.generate_authorization_url(google_apps_domain=domain)))

class Support(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/support.html')
        self.response.out.write(template.render(path, template_values))

class CreateDesker(webapp.RequestHandler):
    def get(self):
        # We don't reference users with Deskers - b/c sometimes editors use share accounts (i.e. news-editor, etc.).  So we just use names
        user = users.get_current_user()
        if user or get_testing(): #if a user is logged in.  I would have used @logged_in but OpenId doesn't play nice with it.  Oh well.
            if get_testing():
                userPerms = Permissions()
                userPerms.role = 2
            else:
                userPerms = get_permissions(str(users.get_current_user().user_id()))            
                
            if userPerms:
                role = userPerms.role
            else:
                role = 0
            if role >=1: #check the permissions.  This pattern is repeated for most of the functions.  Again, would have used @logged_in but OpenId doesn't like it
                name = self.request.get('name')
                section = self.request.get('section')
                date = self.request.get('date')
                if name and section and date:
                    new_desker = Desker()
                    new_desker.name = name
                    new_desker.section = section
                    new_desker.date = datetime.strptime(date,"%Y-%m-%d")
                    new_desker.put()
                    out = {}
                    out['dID']=str(new_desker.key())
                    self.response.out.write(json.dumps(out))
            else: #if bad permissions, do this
                self.response.out.write(json.dumps(False))
        else: #if user isn't logged in, do this
            self.redirect("/")

class CreateSection(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user or get_testing():
            if get_testing():
                userPerms = Permissions()
                userPerms.role = 2
            else:
                userPerms = get_permissions(str(users.get_current_user().user_id()))
                
            if userPerms:
                role = userPerms.role
            else:
                role = 0
            if role >=2:
                name = self.request.get('name')
                if name:
                    new_section = Section()
                    new_section.name = name
                    new_section.put()
                    out = {}
                    out['sID']=str(new_section.key())
                    self.response.out.write(json.dumps(out)) #currently not used b/c there's no callback that gets the sections & outputs them.  It's only internal right now.
                else:
                    self.response.out.write(json.dumps(False)) #currently not used
                self.redirect("/admin") #if ajax updating of admin page is implemented, we should delete this.
            else:
                self.redirect("/")
        else:
            self.redirect("/")
    def post(self):
        CreateSection.get(self)
 
class CreateModifyUserPrefs(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user or get_testing():
            if get_testing():
                userInfo = UserInfo()
                userInfo.uID = str(users.User("james.elkins1@gmail.com").user_id())
            else:
                userInfo = UserInfo.all().filter('uID =', str(users.get_current_user().user_id())).fetch(1)
                
            if not userInfo: #if there is no record, make a new record
                userInfo = UserInfo()
            else: #if there is a record, userInfo is currently an array.  We need to get the object out of the array
                userInfo = userInfo[0]
                
            if self.request.get('phone'):
                userInfo.phone = self.request.get('phone')
            if self.request.get('section'):
                userInfo.prefSection = self.request.get('section')
            userInfo.put()
            out = {}
            out['uInfoKey'] = str(userInfo.key())
            self.response.out.write(json.dumps(out))            
        else:
            self.redirect("/")
        
class CreateModifyUserPerms(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user or get_testing:
            if get_testing():
                userPerms = Permissions()
                userPerms.role = 2
            else:
                #this is the userPerms for the user trying to change other users permissions
                userPerms = get_permissions(str(users.get_current_user().user_id()))
                
            if userPerms:
                role = userPerms.role
            else:
                role = 0
            if role >=2:
                if self.request.get('userEmail'): #have to have something to input/edit
                    user = users.User(self.request.get('userEmail')) #has to be a valid google account.
                    #this is now the userPerms for the user who is being modified
                    userPerms = get_permssions(str(user.user_id()))
                    if not userPerms: #look @ CreateModifyUserPrefs for explanation of what's going on here
                        userPerms = Permissions()
                    else:
                        userPerms = userPerms[0]
                    userPerms.uID = str(user.user_id())
                    if self.request.get('role'):
                        userPerms.role = self.request.get('role')
                    if self.request.get('section'):
                        userPerms.section = self.request.get('section')
                    userPerms.put()
                    out = {}
                    out['uPermsKey'] = str(userPerms.key())
                    self.redirect("/admin")
                    #self.response.out.write(json.dumps(out)) if we were doing ajax, we would use this.  However, we are not, and thus we're just redirecting to /admin
                else:
                    self.response.out.write(json.dumps(False))
            else:
                self.redirect("/")
        else:
            self.redirect("/")

class CreateModifyAssignment(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user or get_testing():
            if get_testing():
                userPerms = Permissions()
                userPerms.role = 2
            else:
                userPerms = get_permissions(str(users.get_current_user().user_id()))
                
            if userPerms:
                role = userPerms.role
            else:
                role = 0
            #We assume that we're going to get good keys for now.
            mod = False #if we are modifying the data, or creating it
            if role >= 1:
                if not self.request.get('aID'):
                    assignment = Assignment()
                    assignment.created = datetime.now()
                    assignment.creator = 'mooman'#users.get_current_user().user_id() PUT BACK OH YEAHHHHH
                else:
                    assignment = get_ass_from_memcache(self.request.get('aID'))
                    mod = True
                
                if self.request.get('title'): 
                    assignment.title = self.request.get('title')
                elif not mod: # so if mod is false (we are creating a new assignment), 
                              # and there was no input, set value to default
                              # but if mod is true, and there was no input, keep value the same (i.e. do nothing)
                    assignment.title = ""
                
                if self.request.get('descript'): 
                    assignment.descript = self.request.get('descript')
                elif not mod:
                    assignment.descript = ""
                    
                if self.request.get('status'):
                    assignment.status = self.request.get('status')
                elif not mod:
                    assignment.status = ""
                
                if self.request.get('dueDate'): 
                    assignment.dueDate = datetime.strptime(self.request.get('dueDate'),"%Y-%m-%d")
                elif not mod:
                    oneDay = timedelta(days=1)
                    tomorrow = datetime.today()+oneDay
                    assignment.dueDate = tomorrow
                    
                if self.request.get('weight'): 
                    assignment.weight = int(self.request.get('weight'))
                elif not mod:
                    assignment.weight = 0
                    
                if self.request.get('section'): 
                    assignment.section = self.request.get('section')
                elif not mod:
                    assignment.section = ""
        
                if self.request.get('docLink'): 
                    #methinks there will be a lot of stuff that goes into this. this is not right as is
                    assignment.docLink = self.request.get('docLink')
                elif not mod:
                    assignment.docLink = ""
                    
                assignment.modified = datetime.now()
                
                if self.request.get('creator'):
                    assignment.creator = self.request.get('creator')
                elif not mod:
                    assignment.creator = ""
                
                if self.request.get('public'): 
                    if self.request.get('public') == "True":
                        assignment.public = True
                    else:
                        assignment.public = False
                elif not mod:
                    assignment.public = False
                
                assignment.put()
                
                #this fixes the issue of memcache and datastore being out of sync
                memcache.set(self.request.get('aID'),assignment)
                
                new_assignee_IDs = []
                out = {}
                new_assignee = False
                if self.request.get_all('uID'): #the assignee routine. To delete, use DeleteEntity
                    for passed_assignee in self.request.get_all('uID'):                
                        in_datastore = False
                        assignees = Assignee.all().filter("assignment =",str(assignment.key())).fetch(1000)
                        if assignees:
                            for assignee in assignees:
                                if str(assignee.assignee) == passed_assignee:
                                    in_datastore = True
                        if in_datastore == False:
                            new_assignee = Assignee()
                            new_assignee.assignment = str(assignment.key())
                            new_assignee.assignee = passed_assignee
                            new_assignee.put()
                            new_assignee_IDs.append(str(new_assignee.key()))
            
                out = to_dict(assignment)
                out['aID']=str(assignment.key())
                if new_assignee:
                    out['assigneeIDs'] = new_assignee_IDs
                    out['uIDs'] = self.request.get_all('uID')
                self.response.out.write(json.dumps(out))
            else:
                self.redirect("/")
        else:
            self.redirect("/")
    def post(self):
        CreateAssignment.get(self)

class DeleteEntity(webapp.RequestHandler): #works for anything - just pass it the ID/key of what you want to delete.
    def get(self):
        user = users.get_current_user()
        if user or get_testing():
            if get_testing():
                userPerms = Permissions()
                userPerms.role = 2
            else:
                userPerms = get_permissions(users.get_current_user().user_id())
            
            if userPerms:
                role = userPerms.role
            else:
                role = 0
            if self.request.get('key') and role >= 1:
                try:
                    k = db.Key(encoded=self.request.get('key'))
                    result = db.get(k)
                    db.delete(result)
                    self.response.out.write(json.dumps(True))
                except:
                    self.response.out.write(json.dumps(False))
            else:
                self.response.out.write(json.dumps(False))
        else:
            self.redirect("/")
    
    def post(self):
        DeleteEntity.get(self)
            

#FIX THIS!!!
class PickupAssignment(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user or get_testing():
            assignment = self.request.get('assignment')
            if get_testing():
                uID = str(users.User('web_editor@cornellsun.com').user_id())
            else:
                uID = str(users.get_current_user().user_id())
            
            if assignment:
                pickup = PickUp()
                pickup.uID = uID
                pickup.requested = datetime.now()
                pickup.assignment = assignment
                pickup.put()
                out = {}
                out['pickupID'] = str(pickup.key())
                self.response.out.write(json.dumps(out))
            else:
                self.response.out.write(json.dumps(False))
        else:
            self.redirect("/")

class Dashboard(webapp.RequestHandler): #have to do the pref section here
    def get(self):
        WeekData = get_week_details(datetime.today().isocalendar()[1],datetime.today().strftime("%Y"),1)
        if users.get_current_user():
            userInfo = UserInfo.all().filter("uID =",str(users.get_current_user().user_id())).fetch(1)
            userPerms = get_permissions(str(users.get_current_user().user_id()))
            TOKEN = gdata.gauth.AeLoad(users.get_current_user().user_id())
            role = 0
        elif get_testing():
            userInfo = []
            new_userInfo = UserInfo()
            new_userInfo.prefSection = str(Section.all().fetch(1)[0].key())
            userInfo.append(new_userInfo)
            userPerms = Permissions()
            userPerms.role = 2
            TOKEN = None
        else:
            userPerms = None
            TOKEN = None
            role = 0
            userInfo = None
        if userPerms:
            role = userPerms.role
        if userInfo:
            prefSection = userInfo[0].prefSection
        else:
            prefSection = str(Section.all().fetch(1)[0].key()) # this must be changed based on the Default model that the admin sets
        
        if TOKEN:
            check_token = False
        else:
            check_token = True
            
        user = users.get_current_user()
        template_values = {
            'user': user, #if user is none, nobody here
            'login_url': "/apps_login?domain=cornellsun.com",
            'check_token': check_token,
            'logout_url': users.create_logout_url('/'), 
            'start_day': WeekData[0],
            'end_day':  WeekData[1],
            'role': role, #0= not logged in, 1=editor, 2=admin
            'prefSection': prefSection,
            'sections': get_section_list()
            }
        path = os.path.join(os.path.dirname(__file__), 'templates/dashboard.html')
        self.response.out.write(template.render(path, template_values))

class Preferences(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user or get_testing():
            if get_testing():
                userInfo = None
            else:
                userInfo = UserInfo.all().filter("uID =",users.get_current_user().user_id()).fetch(1)
            
            if userInfo:
                template_values = {
                    'prefSection': userInfo.prefSection,
                    'phone': userInfo.phone,
                    'sections': get_section_list()
                    }
            else:
                template_values = {
                    'prefSection': "",
                    'phone': "",
                    'sections': get_section_list()
                    }
            path = os.path.join(os.path.dirname(__file__), 'templates/pref.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect("/apps_login?domain=cornellsun.com")

class AddAssignee(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user or get_testing():
            if get_testing():
                userPerms = Permissions()
                userPerms.role = 2
            else:
                userPerms = get_permissions(users.get_current_user().user_id())
            
            if userPerms:
                role = userPerms.role
            else:
                role = 0
            
            if self.request.get("aID") and self.request.get("email"):
                aID = self.request.get("aID")
                email = self.request.get("email")
                
                curAssignees = Assignee.all().filter("aID =",aID)
                
                in_datastore = False
                #check if assignee is already assigned
                for assignee in curAssignees:
                    if assignee == email:
                        in_datastore == True;
                
                if not in_datastore:
                    assignee = Assignee()
                    assignee.assignment = aID
                    assignee.assignee = email
                    assignee.put()
                    
                    out = to_dict(assignee)

                    self.response.out.write(json.dumps(out))
                else:
                    self.response.out.write(json.dumps(False))
                    
        else:
            self.redirect("/")

    def post(self):
        AddAssignee.get(self)

class AssignmentPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            TOKEN = gdata.gauth.AeLoad(users.get_current_user().user_id())
        else:
            TOKEN = None
        if TOKEN:
            check_token = False
        else:
            check_token = True
                    
        template_values = {
            #'check_token' = check_token,
            'aID': self.request.get('aID'),
            }            
        path = os.path.join(os.path.dirname(__file__), 'assignment.html')
        self.response.out.write(template.render(path, template_values))
    def post(self):
        AssignmentPage.get(self)
        
class TestPut(webapp.RequestHandler):
    def get(self):
        section = Section()
        section.name = "News"
        section.put()
        #assignment = Assignment()
        #assignment.created = datetime.now()
        #assignment.status = "oh yeah!"
        #assignment.descript = "the best assignment ever"
        #assignment.title = "whos your daddy"
        #assignment.public = True
        #assignment.dueDate = datetime.strptime("2010-05-06","%Y-%m-%d")
        #assignment.put()
        #assignee = Assignee()
        #assignee.put()
        #userInfo = UserInfo()
        #userInfo.put()
        #derivAssignment = DerivAssignment()
        #derivAssignment.put()
        #testing = Testing()
        #testing.permOff = True
        #testing.put()
        #permissions = Permissions()
        #permissions.uID = str(users.User('james.elkins1@gmail.com').user_id())
        #permissions.role = 2
        #permissions.section = "agttdXN0cnVuMnN1bnIOCxIHU2VjdGlvbhjpBww"
        #permissions.put()
        #pickUp = PickUp()
        #pickUp.put()
        #desker = Desker()
        #desker.put()

class Administer(webapp.RequestHandler):
    def get(self): #not sure what to do for this right now.  Maybe have stuff
        #for editing sections & users?
        #important to set permissions for deskers - the possible deskers that show up are the ones that
        #have permissions for that section
        user = users.get_current_user()
        if user or get_testing():
            if get_testing():
                userPerms = Permissions()
                userPerms.role = 2
            else:
                userPerms = get_permissions(str(users.get_current_user().user_id()))
            if userPerms:
                role = userPerms.role
            else:
                role = 0
            if role >=2:
                template_values = {
                    'sections': get_section_list(),
                    'user': user,
                    'login_url': "/apps_login?domain=cornellsun.com",
                    'logout_url': users.create_logout_url('/')
                    }
                path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
                self.response.out.write(template.render(path, template_values))
            else:
                self.redirect("/")
        else:
            self.redirect("/apps_login?domain=cornellsun.com")       
       
class SetNextWeek(webapp.RequestHandler): #is this better done in just the javascript?  Parse the dates there?
    def get(self):
        shift = self.request.get('shift')
        start_day = self.request.get('start_day')
        end_day = self.request.get('end_day')
        out = {}
        
        if shift:
            if shift == "+":
                out['start_day'] = datetime.strptime(start_day,"%Y-%m-%d") + timedelta(days=7)
                out['end_day'] = datetime.strptime(end_day,"%Y-%m-%d")  + timedelta(days=7)
            elif shift == "-":
                out['start_day'] = datetime.strptime(start_day) - timedelta(days=7)
                out['end_day'] = datetime.strptime(end_day,"%Y-%m-%d") - timedelta(days=7)
            self.response.out.write(json.dumps(out)) #have to have the javascript set those holding divs equal to the start & end day and then reload the weeks assignments.

class GetWeeksAssignments(webapp.RequestHandler):
    def get(self):
        start_day = self.request.get('start_day')
        end_day = self.request.get('end_day')
        section = self.request.get('section')
        
        assignments = Assignment.all().filter("dueDate >=",datetime.strptime(start_day,"%Y-%m-%d")).filter("dueDate <=",datetime.strptime(end_day,"%Y-%m-%d")).order('dueDate').order('weight')
        if self.request.get('section'):
            assignments.filter("section =",section)
        out_assignments = []
        out_assignment = {}
        
        curPerms = None
        assigned = None
        if users.get_current_user() or get_testing():
            if get_testing():
                curPerms = Permissions()
                curPerms.role = 2
                assigned = None
            else:
                curPerms = get_permissions(str(users.get_current_user().user_id())) #I am assuming that staffers don't have permissions
                assigned = get_assigned(str(users.get_current_user().user_id()),str(assignment.key())) #This is necessary to check permissions [if it's assigned to a staffer, that staffer can see it]
            
        for a in assignments.fetch(1000):
            if curPerms is not None or assigned is not None: #put back '' when we use permissions and assigned again
                out_assignment = to_dict(a)
            elif a.public == True:
                #no status, weight, docLink, public
                out_assignment = to_dict(assignment)
                del out_assignment['status']
                del out_assignment['weight']
                del out_assignment['docLink']
                del out_assignment['public']
            else:
                #break - put the break in b/c later we don't want to have all these "can't view this" signs
                out_assignment['dueDate'] = a.dueDate.strftime("%Y-%m-%d")
                out_assignment['title'] = "You may not view this assignment. Please ask to be assigned to it or have your editor make it publicly viewable"            
            out_assignment['aID'] = str(a.key())
            out_assignments.append(out_assignment)
        self.response.out.write(json.dumps(out_assignments))

class GetWeeksDeskers(webapp.RequestHandler):
    def get(self):
        start_day = self.request.get('start_day')
        end_day = self.request.get('end_day')
        
        deskers = Desker.all().filter("date >=",datetime.strptime(start_day,"%Y-%m-%d")).filter("date <=",datetime.strptime(end_day,"%Y-%m-%d"))
        if self.request.get('section'):
            deskers.filter("section =",self.request.get('section'))
        
        out_deskers = []
        for d in deskers.fetch(1000):

            out_desker = to_dict(d)
            out_desker['dID'] = str(d.key())
            out_deskers.append(out_desker)
        
        self.response.out.write(json.dumps(out_deskers))        

class GetAssignment(webapp.RequestHandler):
    def get(self):
        aID = self.request.get('aID')
        assignment = get_ass_from_memcache(aID)
        #Do I want to make this function work for getting the week as well as just one?
        #Then I'd have to add a 'self.request.get('week')' if statement.  Screw it for now.
        out_assignment = {}
        curPerms = None
        assigned = None 
        if users.get_current_user() or get_testing():
            if get_testing():
                curPerms = Permissions()
                curPerms.role = 2
            else:
                curPerms = get_permissions(str(users.get_current_user().user_id())) 
                assigned = get_assigned(str(users.get_current_user().user_id()),str(assignment.key()))
        #I am assuming that staffers don't have permissions
        if curPerms is not None or assigned is not None: 
            out_assignment = to_dict(assignment)
        elif assignment.public == True:
            #no status, weight, docLink, public
            out_assignment = to_dict(assignment)
            del out_assignment['status']
            del out_assignment['weight']
            del out_assignment['docLink']
            del out_assignment['public']
        else:
            out_assignment['dueDate'] = assignment.dueDate.strftime("%Y-%m-%d")
            out_assignment['title'] = "You may not view this assignment. Please ask to be assigned to it or have your editor make it publicly viewable"
        out_assignment['aID'] = str(assignment.key())
        self.response.out.write(json.dumps(out_assignment))
        
#we're going to need a dropdown method for possible assignments for derivative assignments
def main():
    application = webapp.WSGIApplication([('/', Dashboard),
                                          ('/apps_login', AppsFederationHandler),
                                          ('/get_weeks_deskers',GetWeeksDeskers),
                                          ('/create_desker',CreateDesker),
                                          ('/set_next_week',SetNextWeek),
                                          ('/preferences',Preferences),
                                          ('/pickup',PickupAssignment),
                                          ('/testput',TestPut),
                                          ('/admin',Administer),
                                          ('/delete',DeleteEntity),
                                          ('/get_weeks_assignments',GetWeeksAssignments),
                                          ('/assignment',AssignmentPage),
                                          ('/add_assignee',AddAssignee),
                                          ('/get_assignment',GetAssignment),
                                          ('/create_section',CreateSection),
                                          ('/cr_mod_assignment',CreateModifyAssignment),
                                          ('/cr_mod_user_perms',CreateModifyUserPerms),
                                          ('/cr_mod_user_prefs',CreateModifyUserPrefs),
                                          ('/support',Support),
                                          ('/get_oauth_token', GetOauthToken),
                                          ('/test',Test)
                                        ],
                                         debug=True)
    application = middleware.AeoidMiddleware(application)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
