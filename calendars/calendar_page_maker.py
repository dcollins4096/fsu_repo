
import jinja2

loader=jinja2.FileSystemLoader('.')
env = jinja2.Environment(loader=loader)
template = env.get_template('calendar_page_template.html')
web_data={}
web_data['astro']={'title':'Astrophysics Seminar','time':'Wednesdays, 11:45-12:45','location':'Keen 621'}
web_data['astro']['cal']='rpif5nsqd7bipmkriqhfoqr22k%40group.calendar.google.com'
web_data['astro']['text']=''
web_data['CMS']={'title':'Condensed Matter Seminar','time':'Friday, 3:00','location':'B101 MagLab'}
web_data['CMS']['cal']='r1qo2c73g80kihocpdijf9hbf0%40group.calendar.google.com'
web_data['CMS']['text']='<a href="https://nationalmaglab.org/news-events/events/calendar">More events at the MagLab can be found here</a>'
web_data['grad']={'title':'Graduate Student Seminar','time':'Fridays, 5:00','location':'Keen 701'}
web_data['text']="Introductions to the many research groups in Physics are held most Fridays, to introduce the new graduates to the possible opportunities for study."
web_data['grad']['cal']='7utib8ste6k7vhvdtf3d12r79k%40group.calendar.google.com'
web_data['hep']={'title':'High Energy Seminar','time':'Friday, 1:15-2:15','location':'Keen 503'}
web_data['hep']['cal']='1jdrd283q5ass10b0d2t241c4s%40group.calendar.google.com'
web_data['hep']['text']=''
web_data['nuc']={'title':'Nuclear Seminar','time':'Friday, 2:30-3:30','location':'Keen 701'}
web_data['nuc']['cal']='a616nel9l80bhpfnnhmkf1n7o8%40group.calendar.google.com'
web_data['nuc']['text']=''
web_data['col']={'title':'Physics Colloquium','time':'Thursday, 3:45-4:45','location':'UPL 101'}
web_data['col']['cal']='aaug7o5n7103nu2rn9gbqhd8ik%40group.calendar.google.com'
web_data['col']['text']='A reception precedes the talk, beginning at 3:30'
web_data['spe']={'title':'Special Events and Seminars','time':'various','location':''}
web_data['spe']['cal']='nbk8v9jvejqqlpcfpr4fq2l9f4%40group.calendar.google.com'
web_data['text']=''
for group in web_data:
	foutptr = open("live_calendar_%s.html"%group,'w')
	foutptr.write( template.render(stuff=web_data[group]))
	foutptr.close()

