import web
import arduino
import schedule
from web import form
import time
import thread

render = web.template.render('templates/')

urls = (
	'/', 'Index',
	'/login', 'Login',
	'/logout', 'Logout'
)
app = web.application(urls, globals())
door_open = False

task_num = 0

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session

password = "12Mika"

class Login:
	login_form = form.Form(
	form.Textbox('password', web.form.notnull),	
	form.Button('submit', class_="submit"))

	def GET(self):
		f = self.login_form()
		return render.login(f)

	def POST(self):
		if not self.login_form.validates():
			return render.login(self.login_form)

		p = self.login_form.d['password']
		if p == password:
			session.logged_in = True
			raise web.seeother('/')

		return render.login(self.login_form)

class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')

class Index:
	button_form = form.Form(
		form.Button("btn", html="Door", value="Door"),
		form.Button("btn", html="Bell", value="Bell"))

	def GET(self):
		if session.get('logged_in', False):
			return render.index(self.button_form, ("Door is Open" if arduino.door_open else "Door is Closed"))
		else:
			raise web.seeother('/login')

	def POST(self):
		global door_open
		global task_num

		f = self.button_form()
		output_str = "Door is "

		if f.validates():
			data = web.input()

			if data.btn == "Door":
				print "Door Button"
			
				if(not arduino.write('d')):
					print "Write Serial Error"
					output_str = "Serial Error: " + output_str

				if(str(arduino.read()) == 'r'):
					print "Door Toggled"
					arduino.door_open = not arduino.door_open

			elif data.btn == "Bell":
				print "Bell Button"
				if(not arduino.write('b')):
					print "Write Serial Error"
					output_str = "Serial Error: " + output_str
					
				if(str(arduino.read()) == 'r'):
					print "Bell Toggled"

		return render.index(self.button_form, output_str + ("Open" if arduino.door_open else "Closed"))


if __name__ == "__main__":
	web.config.debug = False

	def door_open_job():
		if arduino.door_open:
			print "Door Already Open"
			return

		if(not arduino.write('d')):
			print "Write Serial Error"
			return

		if(str(arduino.read()) == 'r'):
			print "Door Toggled"
			arduino.door_open = not arduino.door_open

	def door_close_job():
		if not arduino.door_open:
			print "Door Already Closed"
			return

		if(not arduino.write('d')):
			print "Write Serial Error"
			return

		if(str(arduino.read()) == 'r'):
			print "Door Toggled"
			arduino.door_open = not arduino.door_open

	def door_ring_job():
		if(not arduino.write('b')):
			print "Write Serial Error"
			return

		if(str(arduino.read()) == 'r'):
			print "Bell Toggled"

		time.sleep(5)

		if(not arduino.write('b')):
			print "Write Serial Error"
			return

		if(str(arduino.read()) == 'r'):
			print "Bell Toggled"

	schedule.every().day.at("08:00").do(door_open_job)
	schedule.every().day.at("08:18").do(door_ring_job)
	schedule.every().day.at("08:20").do(door_close_job)

	schedule.every().day.at("18:00").do(door_open_job)
	schedule.every().day.at("18:18").do(door_ring_job)
	schedule.every().day.at("18:20").do(door_close_job)

	def run_schedule():
		while True:
			schedule.run_pending()
			time.sleep(1)

	thread.start_new_thread(run_schedule, ())

	app.run()