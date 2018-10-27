import webapp2
import jinja2
import os
from google.appengine.api import users
from models import User
from models import Writing
import random
import urllib, json

the_jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = [],
    autoescape = True
)

wordnik_api_key = 'YOUR API KEY HERE'
restriction = 0
mode = 0
limits = 0
quotes = ["If you can tell stories, create characters, devise incidents, and have sincerity and passion, it doesn't matter a damn how you write. -William Somerset Maughm",
    "You write a hit play the same way you write a flop. -William Saroyan",
    "Write freely and as rapidly as possible and throw the whole thing on paper. Never correct or rewrite until the whole thing is done. Rewrite in process is usually found to be an excuse for not going on. -John Steinbeck",
    "Every creator painfully experiences the chasm between his inner vision and its ultimate expression. The chasm is never completely bridged. We all have the conviction, perhaps illusory, that we have much more to say that appears on the paper. -Isaac Bachevis Singer",
    "You can lie to your wife or your boss, but you cannot lie to your typewriter. Sooner or later you must reveal your true self in your pages. -Leon Uris",
    "I write to ease the passing of time. -Jorge Luis Borges",
    "The art of writing is the art of applying the seat of the pants to the seat of the chair. -Mary Heaton Vorse",
    "Convince yourself that you are working in clay, not marble, on paper not eternal bronze: Let that first sentence be as stupid as it wishes. -Jacques Barzun",
    "I haven't had writer's block. I think it's because my process involves writing very badly. -Jennifer Egan",
    "The secret of getting ahead is getting started. The secret of getting started is breaking your complex overwhelming tasks into small manageable tasks, and then starting on the first one. -Mark Twain",
    "You don't start out writing good stuff. You start out writing crap and thinking it's good stuff, and then gradually you get better at it. That's why I say one of the most valuable traits is persistence. -Octavia Butler",
    "If I waited for perfection, I would never write a word. -Margaret Atwood",
    "Nothing will work unless you do. -Maya Angelou",
    "You can't think yourself out of a writing block; you have to write yourself out of a thinking block. -John Rogers",
    "You must write for yourself and not what you think people want to read. -Jodi Ellen Malpas",
    "You can't write the thing unless you write the thing.",
    "Close the door. Write with no one looking over your shoulder. Don't try to figure out what other people want to hear from you; figure out what you have to say. It's the one and only thing you have to offer. -Barbara Kingsolver",
    "The first draft is just you telling yourself the story. -Terry Pratchett",
    "Write because you love the art and the discipline, not because you're looking to sell something. -Ann Patchett",
    "You might not write well every day, but you can always edit a bad page. You can't edit a blank page. -Jodi Picoult",
    "Sit down and put down everything that comes into your head and then you're a writer. But an author is one who can judge his own stuff's worth, without pity, and destroy most of it. -Sidonie Gabrielle",
    "Writers write while dreamers procrastinate. -Besa Kosova"]
characters = ["Old Woman", "Waiter/Waitress", "Rabbit", "Tightrope Walker", "Soldier",
            "Princess", "TV Anchor", "Tiger", "College Student", "Athlete", "Sailor",
            "Surfer", "Professor", "Wizard", "Snowman", "Orphan", "Homeless Person"]
genres = ["Tragedy", "Romance", "Coming-of-Age", "Sci-fi", "Comedy", "Suspense",
        "Dystopian", "Horror", "Action", "Mystery", "Poetry", "Adventure"]
activities = ["waking up from a dream", "finishing a task", "dreaming", "eating food",
            "getting stuck", "being framed for a crime", "getting lost", "meeting a stranger",
            "thinking about life", "learning a lesson", "applying for a job", "buying something"]
locations = ["in the Grand Canyon", "at a wedding", "at the zoo", "in a forest",
            "in an observatory", "in a food court", "in the past", "on a boat",
            "in space", "in a museum", "under the sea", "in a mine", "in a foreign country"]

def logged_in():
    user = users.get_current_user()
    status = ""
    if user:
        status = "Sign Out"
    else:
        status = "Sign In"
    return status

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        status = logged_in()
        link = users.create_logout_url('/login')
        if status == "Sign In":
            link = '/login'
        welcome_template = the_jinja_environment.get_template('templates/welcome.html')
        temp_dict = {'status': status, 'link': link}
        self.response.write(welcome_template.render(temp_dict))

class QuotesPage(webapp2.RequestHandler):
    def get(self):
        status = logged_in()
        link = users.create_logout_url('/login')
        if status == "Sign In":
            link = '/login'
        quotes_template = the_jinja_environment.get_template('templates/quotes.html')
        temp_dict = {'status': status, 'link': link, 'quote': quotes[random.randint(0, len(quotes) - 1)]}
        self.response.write(quotes_template.render(temp_dict))

class ResourcesPage(webapp2.RequestHandler):
    def get(self):
        status = logged_in()
        link = users.create_logout_url('/login')
        if status == "Sign In":
            link = '/login'
        resources_template = the_jinja_environment.get_template('templates/resources.html')
        temp_dict = {'status': status, 'link': link}
        self.response.write(resources_template.render(temp_dict))

class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.response.write('''
                <body style='background-color: antiquewhite;'>
                <div style='margin: auto; text-align: center; padding: 15em 25em 15em 25em;'>
                <div style='padding: 3em; background: whitesmoke; border-radius: 25px; opacity: 0.9; border: 0.1em solid silver;'>
                Please log in to our site! <br>
                <a href="%s">Sign in</a><br><br>
                Or sign up now!<br><a href="%s">Sign Up</a><br><br>
                <a href="/">Go Home</a>
                </div>
                </div>
                </body>'''
                % (users.create_login_url('/login'), users.create_login_url('/login')))
        else:
            email_address = user.nickname()
            dwg_user = User.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' %(users.create_logout_url('/login'))
            if dwg_user:
                self.response.write('''<body style='background-color: antiquewhite;'>
                <div style='margin: auto; text-align: center; padding: 15em 25em 15em 25em;'>
                <div style='padding: 3em; background: whitesmoke; border-radius: 25px; opacity: 0.9; border: 0.1em solid silver;'>
                Welcome %s %s (%s)!<br> %s<br><br> <a href="/">Go Home</a>
                </div></div></body>''' % (dwg_user.first_name, dwg_user.last_name, email_address, signout_link_html))
            else:
                self.response.write('''
                    <body style='background-color: antiquewhite;'>
                    <div style='margin: auto; text-align: center; padding: 15em 25em 15em 25em;'>
                    <div style='padding: 3em; background: whitesmoke; border-radius: 25px; opacity: 0.9; border: 0.1em solid silver;'>
                    Please Sign Up %s!<br>
                    <form method="post" action="/login">
                    <input type="text" name="first_name" placeholder="First Name">
                    <br>
                    <input type="text" name="last_name" placeholder="Last Name">
                    <br>
                    <input type="text" name="username" placeholder="Username">
                    <br>
                    <input type="submit">
                    </form>
                    <br>%s
                    <br><br>
                    <a href="/">Go Home</a>
                    </div></div></body>''' % (email_address, signout_link_html))
    def post(self):
        user = users.get_current_user()
        dwg_user = User(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            username=self.request.get('username'),
            id=user.user_id())
        dwg_user.put()
        self.response.write('''
            <body style='background-color: antiquewhite;'>
            <div style='margin: auto; text-align: center; padding: 15em 25em 15em 25em;'>
            <div style='padding: 3em; background: whitesmoke; border-radius: 25px; opacity: 0.9; border: 0.1em solid silver;'>
            Thanks for signing up, %s %s! You are now logged in!<br>
            <a href="%s">Sign Out</a><br><br>
            <a href="/">Go Home</a>
            </div></div></body>''' % (dwg_user.first_name, dwg_user.last_name, users.create_logout_url('/')))

class AboutPage(webapp2.RequestHandler):
    def get(self):
        status = logged_in()
        link = users.create_logout_url('/login')
        if status == "Sign In":
            link = '/login'
        about_template = the_jinja_environment.get_template('templates/about.html')
        temp_dict = {'status': status, 'link': link}
        self.response.write(about_template.render(temp_dict))

class WritePage(webapp2.RequestHandler):
    def get(self):
        status = logged_in()
        link = users.create_logout_url('/login')
        check = ""
        if status == "Sign In":
            link = '/login'
            check = "WARNING: You must be logged in to save your work!"
        write_template = the_jinja_environment.get_template('templates/write.html')
        temp_dict = {'status': status, 'link': link, 'check': check}
        self.response.write(write_template.render(temp_dict))
    def post(self):
        restriction = int(self.request.get('restriction'))
        mode = int(self.request.get('mode'))
        time_dict = {1: "five", 2: "ten", 3: "fifteen", 4: "thirty", 5: 100, 6: 250, 7: 500, 8: 1000}
        time = ""
        if self.request.get('limits') != "":
            limits = int(self.request.get('limits'))
            time = time_dict[limits]
        status = logged_in()
        link = users.create_logout_url('/login')
        if status == "Sign In":
            link = '/login'
        writing_template = the_jinja_environment.get_template('templates/writing.html')
        temp_dict = {'status': status, 'link': link, 'time': time}
        self.response.write(writing_template.render(temp_dict))
        if restriction == 1: #Timed Challenge
            self.response.write('''Instructions for Timed Writing''')
            if mode == 1: #Plot Generator
                self.response.write('<br><br>Below is a sentence outlining a plot. Your job is to make it into a story. You do not have to strictly obey the sentence, but try and folow the general gist of it. For example, you can choose a different genre or a different location.')
                self.response.write(' For a new sentence, refresh the page.')
                self.response.write("<br><br>Write about a %s %s %s in a %s genre." % (characters[random.randint(0, len(characters) - 1)], activities[random.randint(0, len(activities) - 1)], locations[random.randint(0, len(locations) - 1)], genres[random.randint(0, len(genres) - 1)]))
                self.response.write('''
                    <form method="post" action="/writings">
                        <br><br><textarea name="text"></textarea>
                        <br><div id="submit"><input type="submit" value="Click here to save your work!"></div>
                    </form>''')
            elif mode == 2: #One Word Writing
                url = "http://api.wordnik.com/v4/words.json/randomWord?api_key=" + wordnik_api_key
                response = urllib.urlopen(url)
                data = json.loads(response.read())
                word = data["word"]
                url = "http://api.wordnik.com/v4/word.json/" + word + "/definitions?api_key=" + wordnik_api_key
                response = urllib.urlopen(url)
                data = json.loads(response.read())
                definition = data[0]["text"]
                self.response.write('<br><br>Write about something relating to the word below. NOTE: You do not have to use the word, but try to do so. For a new word, refresh the page.')
                self.response.write('<br><br>Word: ' + word + '<br>Definition: ' + definition)
                self.response.write('''
                    <form method="post" action="/writings">
                        <br><br><textarea name="text"></textarea>
                        <br><div id="submit"><input type="submit" value="Click here to save your work!"></div>
                    </form>''')
            elif mode == 3: #Free Write
                self.response.write('<br><br>You are free to write on whatever topic you like! Keep an eye on the clock though!')
                self.response.write('''
                    <form method="post" action="/writings">
                        <br><br><textarea name="text"></textarea>
                        <br><div id="submit"><input type="submit" value="Click here to save your work!"></div>
                    </form>''')
        elif restriction == 2: #Word Count
            self.response.write('''Instructions for Word Count''')
            if mode == 1: #Plot Generator
                self.response.write('<br><br>Below is a sentence outlining a plot. Your job is to make it into a story in at least ' + str(time) + ' words. You do not have to strictly obey the sentence, but try and folow the general gist of it. For example, you can choose a different genre or a different location.')
                self.response.write(' For a new sentence, refresh the page.')
                self.response.write("<br><br>Write about a %s %s %s in a %s genre." % (characters[random.randint(0, len(characters) - 1)], activities[random.randint(0, len(activities) - 1)], locations[random.randint(0, len(locations) - 1)], genres[random.randint(0, len(genres) - 1)]))
                self.response.write('''
                    <form method="post" action="/writings">
                        <br><br><textarea name='text' id='toCount'></textarea>
                        <br><div id="submit"><input type="submit" value="Click here to save your work!"></div>
                    </form>
                <script>document.getElementById('toCount').addEventListener('input', function () {
                    var text = this.value;
				   if(text == ""){
        	document.querySelector('.count').textContent = 0 + " words";
        }else{
        	count = text.trim().split(' ').length;

        	document.querySelector('.count').textContent = count + " words";
			}
    });</script>''')
            elif mode == 2: #One Word Writing
                url = "http://api.wordnik.com/v4/words.json/randomWord?api_key=" + wordnik_api_key
                response = urllib.urlopen(url)
                data = json.loads(response.read())
                word = data["word"]
                url = "http://api.wordnik.com/v4/word.json/" + word + "/definitions?api_key=" + wordnik_api_key
                response = urllib.urlopen(url)
                data = json.loads(response.read())
                definition = data[0]["text"]
                self.response.write('<br><br>Write about something relating to the word below in at least ' + str(time) + ' words. NOTE: You do not have to use the word, but try to do so. For a new word, refresh the page.')
                self.response.write('<br><br>Word: ' + word + '<br>Definition: ' + definition)
                self.response.write('''
                    <form method="post" action="/writings">
                        <br><br><textarea name='text' id='toCount'></textarea>
                        <br><div id="submit"><input type="submit" value="Click here to save your work!"></div>
                    </form>
                <script>document.getElementById('toCount').addEventListener('input', function () {
                    var text = this.value;
				   if(text == ""){
        	document.querySelector('.count').textContent = 0 + " words";
        }else{
        	count = text.trim().split(' ').length;

        	document.querySelector('.count').textContent = count + " words";
			}
    });</script>''')
            elif mode == 3: #Free Write
                self.response.write('<br><br>You are free to write on whatever topic you like using at least ' + str(time) + ' words!')
                self.response.write('''
                    <form method="post" action="/writings">
                        <br><br><textarea name='text' id='toCount'></textarea>
                        <br><div id="submit"><input type="submit" value="Click here to save your work!"></div>
                    </form>
                <script>document.getElementById('toCount').addEventListener('input', function () {
                    var text = this.value;
				   if(text == ""){
        	document.querySelector('.count').textContent = 0 + " words";
        }else{
        	count = text.trim().split(' ').length;

        	document.querySelector('.count').textContent = count + " words";
			}
    });</script>''')
        elif restriction == 3: #No Limits
            self.response.write('''Instructions for No Limits''')
            if mode == 1: #Plot Generator
                self.response.write('<br><br>Below is a sentence outlining a plot. Your job is to make it into a story. You do not have to strictly obey the sentence, but try and folow the general gist of it. For example, you can choose a different genre or a different location.')
                self.response.write(' For a new sentence, refresh the page.')
                self.response.write("<br><br>Write about a %s %s %s in a %s genre." % (characters[random.randint(0, len(characters) - 1)], activities[random.randint(0, len(activities) - 1)], locations[random.randint(0, len(locations) - 1)], genres[random.randint(0, len(genres) - 1)]))
                self.response.write('''
                    <form method="post" action="/writings">
                        <br><br><textarea name="text"></textarea>
                        <br><div id="submit"><input type="submit" value="Click here to save your work!"></div>
                    </form>''')
            elif mode == 2: #One Word Writing
                url = "http://api.wordnik.com/v4/words.json/randomWord?api_key=" + wordnik_api_key
                response = urllib.urlopen(url)
                data = json.loads(response.read())
                word = data["word"]
                url = "http://api.wordnik.com/v4/word.json/" + word + "/definitions?api_key=" + wordnik_api_key
                response = urllib.urlopen(url)
                data = json.loads(response.read())
                definition = data[0]["text"]
                self.response.write('<br><br>Write about something relating to the word below. NOTE: You do not have to use the word, but try to do so. For a new word, refresh the page.')
                self.response.write('<br><br>Word: ' + word + '<br>Definition: ' + definition)
                self.response.write('''
                    <form method="post" action="/writings">
                        <br><br><textarea name="text"></textarea>
                        <br><div id="submit"><input type="submit" value="Click here to save your work!"></div>
                    </form>''')
            elif mode == 3: #Free Write
                self.response.write('<br><br>You are free to write on whatever topic you like! You are free from all restrictions!')
                self.response.write('''
                    <form method="post" action="/writings">
                        <br><br><textarea name="text"></textarea>
                        <br><div id="submit"><input type="submit" value="Click here to save your work!"></div>
                    </form>''')

class WritingsPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        status = logged_in()
        link = users.create_logout_url('/login')
        if status == "Sign In":
            link = '/login'
        writings = Writing.query().filter(Writing.user_id == user.user_id()).fetch()
        writings_template = the_jinja_environment.get_template('templates/writings.html')
        temp_dict = {'status': status, 'link': link, 'writings': writings}
        self.response.write(writings_template.render(temp_dict))

    def post(self):
        text = self.request.get('text')
        user = users.get_current_user()
        user_id = user.user_id()
        writings = Writing(text=text, user_id=user_id)
        writings.put()
        self.redirect('/writings')

class UnhiddenQuotesPage(webapp2.RequestHandler):
    def get(self):
        status = logged_in()
        link = users.create_logout_url('/login')
        if status == "Sign In":
            link = '/login'
        unhidden_template = the_jinja_environment.get_template('templates/unhidden.html')
        temp_dict = {'status': status, 'link': link, 'quote': quotes[random.randint(0, len(quotes) - 1)]}
        self.response.write(unhidden_template.render(temp_dict))

app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/quotes', QuotesPage),
    ('/resources', ResourcesPage),
    ('/login', LoginPage),
    ('/about', AboutPage),
    ('/write', WritePage),
    ('/writings', WritingsPage),
    ('/quote', UnhiddenQuotesPage)
], debug = True)
