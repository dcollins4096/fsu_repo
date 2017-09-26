
# displayname="von Moln a r, Stephan"
import jinja2
import pdb
import glob
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


#set up.
all_people = {} #dictionary of groups
fptr = open("faculty_list.txt","r")
lines=fptr.readlines()
fptr.close()
stuff = {} #temp storage for parsing

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
            this_list = all_people.get(this_group,[])
            stuff['local_image']=False

            this_list.append(person(**stuff)) # **stuff unrolls to key=value pairs for functions
            all_people[this_group] = this_list
        stuff={}

if 1:
    #set up the template.
    loader=jinja2.FileSystemLoader('.')
    env = jinja2.Environment(loader=loader)
    template_fname= 'people_template.html'
    template = env.get_template(template_fname)

    #push the people into the template.
    fname = 'people.html' #%npeople
    foutptr = open(fname,'w')
    foutptr.write( template.render(**all_people) )
    foutptr.close()
    print "wrote", fname

