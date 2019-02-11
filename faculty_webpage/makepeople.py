
# displayname="von Moln a r, Stephan"
import jinja2
import pdb
import glob
import numpy as np
nar = np.array

full_key_list = ['displayname','department','title','room','phone','email', 'other_email','web','group','research_area', 'other','image','withus', 'image_name']
from optparse import OptionParser
parser = OptionParser("python makepeople.py <options> \n\tmakes the people page.  Maybe does other stuff.")
parser.add_option("-l", "--local_images", dest="local_images", help="Uses local images to make sure things work.",
                  action = "store_true", default = False)
parser.add_option("-r", "--research_area", dest="research_area", help="Return a list of all people associated with a research area.",
                  action = "store", default = None)
parser.add_option("-p", "--page_skip", dest="page_skip", help="skip making the page.",
                  action = "store_true", default = False)
parser.add_option("-t", "--tsv", dest="tsv", help="make a tsv page",
                  action = "store_true", default = False)
parser.add_option("-n", "--fname", dest="fname", help="filename",
                  action = "store", default = "CurrentList.tsv")
parser.add_option("-e", "--email", dest="email", help="Hunt for email addresses that are still physics.fsu.edu",
                  action = "store_true", default = False)
parser.add_option("-x", "--title_revert", dest="title_revert", help="look for title changes",
                  action = "store_true", default = False)
(options, args) = parser.parse_args()

def no_whites(something):
    """Removes any empty charachters"""
    out = ""
    for s in something:
        #print "."+s+".",
        if s not in  ['', ' ', '\n']:
            out += s
    #print "x"
    return out
import physics_data
default_space = "&nbsp;"
def make_space(val):
    if len(val.strip()) ==0:
        return default_space
    else:
        return val
class person():
    def __init__(self, displayname=None,Name=None,
            image_name=None,image=None,title="",room=default_space,phone=default_space,email=None,web=None,group=None,
            research_area=None, other=None, other_email=None,
            local_image=False,Department=None,withus=""):
        self.displayname=displayname
        self.withus=withus

        if Name is not None:
            self.displayname=Name
        self.image_name      =image_name
        if local_image:
            image_root = "images"
        else:
            image_root = "/sites/g/files/upcbnu441/files/media/images_people/"
        self.title      =title
        self.room       =make_space(room)
        self.phone      =make_space(phone)
        self.email       =email
        self.web        =web
        self.group = group
        self.research_area = research_area
        self.research_area_web = research_area
        self.department=Department

        if self.research_area is not None:
            self.research_area_web = ''
            area_list = [a.strip().strip('"') for a in self.research_area.split(',')]
            for area in area_list:
                if area in physics_data.group_info:
                    stuff=physics_data.group_info[area]
                    self.research_area_web += '<a = href= %s target="_blank">%s</a><br>'%(stuff['web'],stuff['name'])
            
        self.email_domain=''
        self.other = other
        self.other_email=other_email
        if self.web  not in [None,'']:
            self.name_and_link = '<a href="%s" target="_self">%s</a>'%(self.web,self.displayname)
            self.weblink = '<a href="%s" target="_blank">web'%(self.web)
        else:
            self.name_and_link = '%s'%self.displayname
            self.weblink = ''
        if self.displayname is not None:
            names = self.displayname.split(",")
            self.firstname=no_whites(names[1])
            self.lastname=no_whites(names[0])

        if self.image_name == None or self.image_name == "":
            image_name = "%s%s.jpg"%(self.lastname,self.firstname)
        else:
            image_name = self.image_name
        self.image_name=image_name

        if glob.glob("images/%s"%image_name) != []:
            self.image = "<img alt=\"%s\" data-entity-type=\"\" data-entity-uuid=\"\"  height=\"50\" src=\"%s/%s\" width=\"50\" />"%(image_name,image_root,image_name)
        else:
            self.image = "&nbsp;"

        if self.email not in [None,'']:
            try:
                is_formed_right = self.email.index("@")
            except:
                print("Email error", self.displayname)

            name = '&quot;%s %s&quot;'%(names[1],names[0])
            p1 = self.email.split("@")
            addy =   '&quot;%s&quot;'%p1[0]
            domain = '&quot;%s&quot;'%p1[1]
            send_email = ' href="javascript:send(%s,%s,%s)"'%(name,addy,domain)
            show_email = ' href="javascript:show(%s,%s,%s)"'%(name,addy,domain)
            self.email_domain = domain
            #self.email=send_email
            self.sendemail=send_email
            self.showemail=show_email
    def get_name(self):
        return self.displayname
    def to_tsv(self):
        output = ""
        for key in full_key_list:
            value = self.__dict__.get(key,"")
            if value is None:
                value = ""
            output += value + "\t"
        output += "\n"
        return output



class people():
    def __init__(self):
        self.people_by_group={}
        self.research_areas=[]
        self.groups = []
    def return_all_people(self):
        all_people = []
        for group in list(self.people_by_group.keys()):
            all_people+=self.people_by_group[group]
        return all_people
    def to_tsv(self, fname = 'people.tsv'):
        all_people = []
        fptr = open(fname,'w')
        nkey=len(full_key_list)
        fptr.write( "%s\t"*nkey%tuple(full_key_list)+"\n")
        for group in list(self.people_by_group.keys()):
            for person in self.people_by_group[group]:
                fptr.write( person.to_tsv() )
        fptr.close()
    def add_to_group(self,group,person):
        if group not in self.groups:
            self.people_by_group[group]=[]
            self.groups.append(group)
        self.people_by_group[group].append(person)
        if person.research_area not in self.research_areas:
            self.research_areas.append(person.research_area)

    def sort_groups(self):
        for group in list(self.people_by_group.keys()):
            self.people_by_group[group] = sorted(self.people_by_group[group],key=lambda x: x.displayname)
    def parse_text_file(self,fname="faculty_list.txt"):
        fptr = open(fname,"r")
        lines=fptr.readlines()
        fptr.close()
        stuff = {} #temp storage for parsing
        for line in lines:
            if line[0] == '#':
                continue
            spl = line.split("=") 
            if len(spl) < 2:
                continue
            key = spl[0].strip().strip('"')
            val = line[line.index('=')+1:].strip().strip('"')
            if key in full_key_list:
                stuff[key]=val
            else:
                print("Unknown keyword ", line)
            if key == 'group': 
                withus = True
                if 'withus' in stuff:
                    withus =  eval(stuff['withus'])
                if 'displayname' in stuff and withus:
                    this_group = stuff.get('group','Oops') 
                    stuff['local_image']=options.local_images

                    self.add_to_group(this_group,person(**stuff)) # **stuff unrolls to key=value pairs for functions
                stuff={}
        self.sort_groups()
    def parse_tsv(self,fname = 'full_list.tsv'):
        fptr = open(fname,"r")
        lines = fptr.readlines()
        fptr.close()
        heads = lines[0][:-1].split("\t")
        if heads[-1][-1] == '\r':
            heads[-1] = heads[-1][:-1]
        for line in lines[1:]:
            values = line[:-1].split("\t")
            this_dict = dict( zip( heads, values))
            this_group = this_dict.get('group','Oops')
            this_dict['local_image']=options.local_images
            self.add_to_group(this_group, person(**this_dict))
        self.sort_groups()



    def __getitem__(self,item):
        output = []
        if item in self.groups:
            output= self.people_by_group[item]
        elif item in self.research_areas:
            for group in list(self.people_by_group.keys()):
                for person in self.people_by_group[group]:
                    if person.research_area == item:
                        output.append(person)
            output = sorted(output,key=lambda x:x.displayname)
        return output

"""for later: https://nationalmaglab.org/research/publications-all"""

#set up.

def physics_email_hunt(all_people):
    ap = nar(all_people.return_all_people())
    b = nar([a.email_domain.strip('"') =='physics.fsu.edu' for a in ap])
    still_old = ap[b]
    for p in still_old:
        print(p.displayname) #, p.email

all_people=people()
if options.fname[-3:] == 'txt':
    all_people.parse_text_file(options.fname)
elif options.fname[-3:] == 'tsv':
    all_people.parse_tsv(options.fname)
if options.tsv:
    all_people.to_tsv("test.tsv")
if options.email:
    physics_email_hunt(all_people)
if options.research_area is not None:
    for person in all_people[options.research_area]:
        print(person.get_name())

if options.title_revert is True:
    old_version=people()
    old_version.parse_text_file('faculty_list.txt')
    current=people()
    current.parse_tsv('CurrentList.tsv')
    old_people = old_version.return_all_people()
    new_people = current.return_all_people()
    print("old",len(old_people))
    print("new",len(new_people))
    for po in old_people:
        for pn in new_people:
            if po.displayname == pn.displayname:
                if po.title != pn.title:
                    print("Person %30s old %20s new %20s"%(po.displayname, po.title,pn.title))
    

if options.page_skip is False:
    #set up the template.
    loader=jinja2.FileSystemLoader('.')
    env = jinja2.Environment(loader=loader)
    template_fname= 'people_template.html'
    template = env.get_template(template_fname)

    #push the people into the template.
    fname = 'people.html' #%npeople
    foutptr = open(fname,'w')

    category_labels = {}
    category_labels['faculty']='Faculty'
    category_labels['teaching_faculty']="Teaching Faculty"
    category_labels['research_faculty']='Research Faculty'
    category_labels['nonr_fac']='Non-Graduate Faculty'
    category_labels['emeritus']='Emeritus Faculty'
    category_labels['postdocs']='Postdoctoral Fellows'
    category_labels['staff']='Staff'
    category_list=[]
    category_list.append('faculty')
    category_list.append('teaching_faculty')
    category_list.append('research_faculty')
    category_list.append('nonr_fac')
    category_list.append('emeritus')
    category_list.append('postdocs')
    category_list.append('staff')

    foutptr.write( template.render(all_people=all_people, category_labels=category_labels, category_list=category_list) )
    foutptr.close()
    print("wrote new starter page:", fname)
    print("To do:  Edit people page.")
    print("        COPY people page.")
    print("        pbpaste > current_page_2.html")
    print("        vimdiff current_page.html, current_page_2.html")
    print("        THEY SHOULD BE THE SAME, otherwise ingest the differences")
    print("        cat people.html |pbcopy")
    print("        paste into editor window.")
    print("        Save as draft, edit, copy, pbpaste current_page_3, diff.")
    print("        check in current_page_3 as current_page.")
    print("        check in all other changes.")

