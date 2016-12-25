import jinja2
import os
import webapp2
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Student(ndb.Model):
	name = ndb.StringProperty()

class Course(ndb.Model):
	name = ndb.StringProperty()

class Enroll(ndb.Model):
	studentkey = ndb.KeyProperty()	
	classkey = ndb.KeyProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('homepage.html')
        self.response.write(template.render({}))

class studentHandler(webapp2.RequestHandler):
	def get(self):
		message = ""
		template = jinja_environment.get_template('createstudent.html')
		self.response.write(template.render({'message':message}))
	def post(self):
		if self.request.get('name'):
			if not Student.query().filter(Student.name == self.request.get('name')).fetch():
				s = Student()
				s.name = self.request.get('name')
				s.put()
				message = "Student: " + s.name + " created"
			else:
				message = "That student already exists"
		else:
			message = "Please enter a student name"
		template = jinja_environment.get_template('createstudent.html')
		self.response.write(template.render({'message':message}))

class courseHandler(webapp2.RequestHandler):
	def get(self):
		message = ""
		template = jinja_environment.get_template('createcourse.html')
		self.response.write(template.render({'message':message}))
	def post(self):
		if self.request.get('name'):
			if not Course.query().filter(Course.name == self.request.get('name')).fetch():
				c = Course()
				c.name = self.request.get('name')
				c.put()
				message = "Class: " + c.name + " created"
			else:
				message = "Course already exists"
		else:
			message = "Please enter a class name"
		template = jinja_environment.get_template('createcourse.html')
		self.response.write(template.render({'message':message}))

class enrollHandler(webapp2.RequestHandler):
	def get(self):
		message = ""
		student = Student.query().fetch()
		course = Course.query().fetch()
		template = jinja_environment.get_template('enroll.html')
		self.response.write(template.render({'message':message, 'student': student, 'course': course}))

	def post(self):
		message = ""
		sname = self.request.get('name')
		cname = self.request.get('course')
		student = Student.query(Student.name == sname).fetch()[0]
		course = Course.query(Course.name == cname).fetch()[0]

		e = Enroll()
		e.studentkey = student.key
		e.classkey = course.key
		e.put()

		self.redirect("/enrollhandler")

		# message = "Enrollemnt completed"
		# template = jinja_environment.get_template('enroll.html')
		# self.response.write(template.render({'message':message}))11


class studentlookupHandler(webapp2.RequestHandler):
	def get(self):
		student = Student.query().fetch()
		template = jinja_environment.get_template('studentandcourse.html')
		self.response.write(template.render({'student': student}))

	def post(self):

		sname = self.request.get('name')
		
		student = Student.query(Student.name == sname).fetch()[0]
		
		e = Enroll.query(Enroll.studentkey == student.key).fetch()[0]
		
		c = Course.query(Course.key== e.classkey).fetch()
		
		template = jinja_environment.get_template('studentandcourse.html')
		self.response.write(template.render({'courses': c}))


		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/studenthandler', studentHandler),
    ('/courseHandler', courseHandler),
    ('/enrollhandler', enrollHandler),
    ('/studentlookuphandler', studentlookupHandler),
], debug=True)
