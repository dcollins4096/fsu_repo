
import jinja2

class group():
    def __init__(self, name="MOON",image="NO.png",web="google.com"):
        self.name=name
        self.image=image
        self.web=web

ResearchGroupInfo={}
ResearchGroupInfo['atomic']={'web':"https://physics.fsu.edu/research/atomic-physics",
                 'image':"Research_Atomic.png",
                 'name':"Atomic Physics"}
ResearchGroupInfo['CME']={'web':"https://physics.fsu.edu/research/condensed-matter-experimental-physics",
'image':"Research_CM_X.png",
'name': "Condensed Matter Experiment"}
ResearchGroupInfo['NT']={'web':"http://wwwphysics.fsu.acsitefactory.com/nuclear-theory",
          'image':"Research_NUC_T.jpg" ,
          'name':"Nuclear Theory"}
ResearchGroupInfo['Hadronic']={'web':"http://hadron.physics.fsu.edu/",
          'image':"Research_NUC_Had.png" ,
          'name':"Nuclear: Hadronic"}
ResearchGroupInfo['CMT']={'web':"https://physics.fsu.edu/research/condensed-matter-theoretical-physics",
              'image':"Research_CM_T.jpg",
              'name':"Condensed Matter Theory"}
ResearchGroupInfo['HET']={'web':"http://www.hep.fsu.edu/",
              'image':"Research_HE_T.png",
              'name':"High Energy Physics: Theory"}
ResearchGroupInfo['HEE']={'web':"http://www.hep.fsu.edu/",
          'image':"Research_HE_X.jpg",
          'name':"High Energy Physics: Experiment"}
ResearchGroupInfo['NHM']={'web':"https://magnet.fsu.edu",
          'image':"Research_MAG.jpg" ,
          'name':"National High Magnetic Field Lab"}
ResearchGroupInfo['Fox']={'web':"http://fsunuc.physics.fsu.edu/",
          'image':"Research_NUC_X.jpg" ,
          'name':"Nuclear: John D. Fox Accelerator Lab"}
ResearchGroupInfo['astro']={'web':"Astrophysics",'image':"Research_Astro.png", 'name':"http://astrophysics.physics.fsu.edu/"))
g=[]
g.append(group(***ResearchGroupInfo['astro']))
g.append(
    group(**ResearchGroupInfo['atomic']))
g.append(
    group(**ResearchGroupInfo['CME']))
g.append(
    group(**ResearchGroupInfo['CMT']))
g.append(
    group(**ResearchGroupInfo['HET']))
g.append(
    group(**ResearchGroupInfo['HEE']))
g.append( group(**ResearchGroupInfo['NHM']))
g.append(
    group(**ResearchGroupInfo['Fox']))
g.append(
          group(**ResearchGroupInfo['NT']))
g.append(
    group(**ResearchGroupInfo['Hadronic']))

"""Sometimes the template used
<div class="clearfix visible-xs visible-sm visible-lg"></div>
but sometimes only "visible-xs"
"""
live = False
if live:
    image_path="https://physics.fsu.edu/sites/g/files/upcbnu441/files/media/images_research"
    head = ""
else:
    image_path="./ResearchImages"
    head = open("Research_Head.html").read()

loader=jinja2.FileSystemLoader('.')
env = jinja2.Environment(loader=loader)
template = env.get_template('ResearchPageTemplate.html')
foutptr = open("ResearchPageLive.html",'w')
foutptr.write( template.render(head=head,groups=g,image_path=image_path))
foutptr.close()

"""
HTML Template Blank:
mostly 
{% for d in list_of_days%}
      <tr><td> {{d.date.month}} / {{d.date.day}}</td>
          <td> {{d.pending_items}}</td>
          <td> {{d.expected_item}}</td>
          <td>{{d.remaining_items}}</td>
          <td style = {{d.css_remaining}}>{{d.remaining_balance}}</td>
          <td style = {{d.css_remaining_perdiem}}>{{d.remaining_balance_with_perdiem}}</td>
          <!-- <td style =
              {{d.css_budget_health}}>{{d.budget_health}} </td>  -->
      </tr>
      {% endfor %}
"""
         

