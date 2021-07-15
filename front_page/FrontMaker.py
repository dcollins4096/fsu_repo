
import jinja2
#import physics_data
#class group():
#    def __init__(self, name="MOON",image="NO.png",web="google.com"):
#        self.name=name
#        self.image=image
#        self.web=web
#
#group_info = physics_data.group_info
#g=[]
#for name in group_info:
#    g.append(group(**group_info[name]))

"""Sometimes the template used
<div class="clearfix visible-xs visible-sm visible-lg"></div>
but sometimes only "visible-xs"
"""
live = True
if live:
    image_path="https://physics.fsu.edu/sites/g/files/upcbnu441/files/media/images_research"
    head = ""
else:
    image_path="./FrontImages"
    head = open("Head.html").read()

loader=jinja2.FileSystemLoader('.')
env = jinja2.Environment(loader=loader)
template = env.get_template('Template.html')
foutptr = open("LiveFrontPage.html",'w')
foutptr.write( template.render())#head=head,groups=g,image_path=image_path))
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
         

