
# displayname="von Moln a r, Stephan"
import jinja2
import pdb
import glob

from optparse import OptionParser
parser = OptionParser("python makepeople.py <options> \n\tmakes the people page.  Maybe does other stuff.")
parser.add_option("-l", "--local_images", dest="local_images", help="Uses local images to make sure things work.",
                  action = "store_true", default = False)
parser.add_option("-r", "--research_area", dest="research_area", help="Return a list of all people associated with a research area.",
                  action = "store", default = None)
parser.add_option("-p", "--page_skip", dest="page_skip", help="skip making the page.",
                  action = "store_true", default = False)
(options, args) = parser.parse_args()

ef = execfile
def no_whites(something):
    """Removes any empty charachters"""
    out = ""
    for s in something:
        #print "."+s+".",
        if s not in  ['', ' ', '\n']:
            out += s
    #print "x"
    return out

class person():
    def __init__(self, displayname=None,
            image=None,title="",room="",phone="",email=None,web=None,group=None,
            research_area=None, other=None,
            local_image=False):
        self.displayname=displayname
        self.image      =image
        if local_image:
            image_root = "images"
        else:
            image_root = "/sites/g/files/upcbnu441/files/media/images_people/"
        self.title      =title
        self.room       =room
        self.phone      =phone
        self.email       =email
        self.web        =web
        self.group = group
        self.research_area = research_area
        if self.web is not None:
            self.name_and_link = '<a href="%s" target="_self">%s</a>'%(self.web,self.displayname)
        else:
            self.name_and_link = '%s'%self.displayname
        if self.displayname is not None:
            names = self.displayname.split(",")
            self.firstname=no_whites(names[1])
            self.lastname=no_whites(names[0])
        if self.image == None:
            image_name = "%s%s.jpg"%(self.lastname,self.firstname)
        else:
            image_name = self.image

        if glob.glob("images/%s"%image_name) != []:
            self.image = "<img alt='%s' height='50' width='50' src='%s/%s'>"%(image_name,image_root,image_name)
        else:
            self.image = "&nbsp;"
        if self.email is not None:
            try:
                is_formed_right = self.email.index("@")
            except:
                print "Email error", self.displayname

            name = '"%s %s"'%(names[1],names[0])
            p1 = self.email.split("@")
            addy =   '"%s"'%p1[0]
            domain = '"%s"'%p1[1]
            send_email = "href='javascript:send(%s,%s,%s)'"%(name,addy,domain)
            show_email = "href='javascript:show(%s,%s,%s)'"%(name,addy,domain)
            self.email=send_email
            self.sendemail=send_email
            self.showemail=show_email
    def get_name(self):
        return self.displayname


#set up.
fptr = open("faculty_list.txt","r")
lines=fptr.readlines()
fptr.close()
stuff = {} #temp storage for parsing

class people():
    def __init__(self):
        self.people_by_group={}
        self.research_areas=[]
        self.groups = []
    def add_to_group(self,group,person):
        if group not in self.groups:
            self.people_by_group[group]=[]
            self.groups.append(group)
        self.people_by_group[group].append(person)
        if person.research_area not in self.research_areas:
            self.research_areas.append(person.research_area)

    def sort_groups(self):
        for group in self.people_by_group.keys():
            self.people_by_group[group] = sorted(self.people_by_group[group],key=lambda x: x.displayname)


    def __getitem__(self,item):
        output = []
        if item in self.groups:
            output= self.people_by_group[item]
        elif item in self.research_areas:
            for group in self.people_by_group.keys():
                for person in self.people_by_group[group]:
                    if person.research_area == item:
                        output.append(person)
            output = sorted(output,key=lambda x:x.displayname)
        return output

all_people=people()
"""for later: https://nationalmaglab.org/research/publications-all"""

for line in lines:

    #sanatize any key=value pairs, store them temporarily in stuff
    spl = line.split("=") 
    if len(spl) != 2:
        continue
    key = spl[0].strip().strip('"')
    val = spl[1].strip().strip('"')

    #check for parsing.
    if key in ['research_area','displayname','title','room','phone','email','web','group', 'other','image','withus']:
        stuff[key]=val
    else:
        print "Unknown keyword ", line

    #we assume that group happens last.  
    #When it appears, injest stuff into a person, add to the appropriate list.
    if key == 'group': 
        withus = True
        if stuff.has_key('withus'):
            withus =  eval(stuff['withus'])
        if stuff.has_key('displayname') and withus:
            this_group = stuff.get('group','Oops') 
            stuff['local_image']=options.local_images

            all_people.add_to_group(this_group,person(**stuff)) # **stuff unrolls to key=value pairs for functions
        stuff={}
all_people.sort_groups()
if options.research_area is not None:
    for person in all_people[options.research_area]:
        print person.get_name()
if options.page_skip is False:
    #set up the template.
    loader=jinja2.FileSystemLoader('.')
    env = jinja2.Environment(loader=loader)
    template_fname= 'people_template.html'
    template = env.get_template(template_fname)

    #push the people into the template.
    fname = 'people.html' #%npeople
    foutptr = open(fname,'w')
    foutptr.write( template.render(all_people=all_people) )
    foutptr.close()
    print "wrote", fname

