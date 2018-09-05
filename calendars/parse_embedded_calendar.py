#parses urls.
import re
import copy
import pdb
draft_0="""<iframe frameborder="0" height="600" scrolling="no" src="https://calendar.google.com/calendar/embed?showTitle=0&amp;showNav=0&amp;showPrint=0&amp;showTabs=0&amp;showCalendars=0&amp;mode=AGENDA&amp;height=600&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;src=rpif5nsqd7bipmkriqhfoqr22k%40group.calendar.google.com&amp;color=%23B1440E&amp;src=r1qo2c73g80kihocpdijf9hbf0%40group.calendar.google.com&amp;color=%235229A3&amp;src=7utib8ste6k7vhvdtf3d12r79k%40group.calendar.google.com&amp;color=%23875509&amp;src=1jdrd283q5ass10b0d2t241c4s%40group.calendar.google.com&amp;color=%2328754E&amp;src=a616nel9l80bhpfnnhmkf1n7o8%40group.calendar.google.com&amp;color=%23182C57&amp;src=aaug7o5n7103nu2rn9gbqhd8ik%40group.calendar.google.com&amp;color=%2342104A&amp;src=nbk8v9jvejqqlpcfpr4fq2l9f4%40group.calendar.google.com&amp;color=%235229A3&amp;ctz=America%2FNew_York" style="border-width:0" width="100%"></iframe>"""

def parse_iframe(string):
    match = re.match(r"<iframe(.*)>.?</iframe>",string)
    if match is not None:
        work = match.group(1)
    else:
        work= string

    work=work.strip()
    kwargs = work.split(" ")
    kwd = {}
    for i in kwargs:
        both = i.split("=")
        if len(both) > 1 :
            kw = both[0].strip()
            if i.startswith('src'):
                kwd[kw] = [b.split("=") for b in sorted(i[ i.index('?'):].split("&amp;"))]
            else:

                kwd[kw]=both[1].strip()
#   url_args = {}
#   if 'src' not in kwd:
#       print("src not found in kwd.  That's probably bad.")
#   else:
#       args = kwd['src'].split('&amp;')
#       for j in args:
#           print("---%s"%j)

    return kwd

draft_1="""<iframe src="https://calendar.google.com/calendar/embed?showTitle=0&amp;showNav=0&amp;showPrint=0&amp;showTabs=0&amp;mode=AGENDA&amp;height=600&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;src=rpif5nsqd7bipmkriqhfoqr22k%40group.calendar.google.com&amp;color=%23B1440E&amp;src=7utib8ste6k7vhvdtf3d12r79k%40group.calendar.google.com&amp;color=%23875509&amp;src=1jdrd283q5ass10b0d2t241c4s%40group.calendar.google.com&amp;color=%2328754E&amp;src=a616nel9l80bhpfnnhmkf1n7o8%40group.calendar.google.com&amp;color=%23182C57&amp;src=aaug7o5n7103nu2rn9gbqhd8ik%40group.calendar.google.com&amp;color=%2342104A&amp;src=nbk8v9jvejqqlpcfpr4fq2l9f4%40group.calendar.google.com&amp;color=%235229A3&amp;ctz=America%2FNew_York" style="border-width:0" width="100%" height="600" frameborder="0" scrolling="no"></iframe>"""
large_view="""<iframe src="https://calendar.google.com/calendar/embed?title=FSU%20Physics%20Seminars&amp;showPrint=0&amp;height=600&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;src=rpif5nsqd7bipmkriqhfoqr22k%40group.calendar.google.com&amp;color=%23B1440E&amp;src=r1qo2c73g80kihocpdijf9hbf0%40group.calendar.google.com&amp;color=%235229A3&amp;src=7utib8ste6k7vhvdtf3d12r79k%40group.calendar.google.com&amp;color=%23875509&amp;src=1jdrd283q5ass10b0d2t241c4s%40group.calendar.google.com&amp;color=%2328754E&amp;src=a616nel9l80bhpfnnhmkf1n7o8%40group.calendar.google.com&amp;color=%23182C57&amp;src=aaug7o5n7103nu2rn9gbqhd8ik%40group.calendar.google.com&amp;color=%2342104A&amp;src=nbk8v9jvejqqlpcfpr4fq2l9f4%40group.calendar.google.com&amp;color=%235229A3&amp;ctz=America%2FNew_York" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>"""
main = parse_iframe(draft_0)
new = parse_iframe(large_view)
def kzz(lst):
    return [a[0] for a in lst]
def vzz(lst):
    return [a[1] for a in lst]
def differ(D1,D2, print_samesies=True):
    template = "%60s %20s %s"
    both_keys = list(set(list(D1.keys())+list(D2.keys())))
    if 'src' in both_keys:
        ind = both_keys.index('src')
        both_keys.pop(ind)

    for k in D1:
        if k not in both_keys and k not in ['src']:
            print(template%("",k,""))
            print(template%(D1[k],"||",""))
    for k in D2:
        if k not in both_keys and k not in ['src']:
            print(template%("",k,""))
            print(template%("","||",D2[k]))
    for k in both_keys:
        middle = "||"
        #print(template%("",k,""))
        if D1[k] != D2[k]:
            middle = "**" + k + "**"
            print(template%(D1[k],middle,D2[k]))
        else:
            if print_samesies:
                middle = "--" + k + "--"
                print(template%(D1[k],middle,D2[k]))
    if 'src' in D1 and 'src' in D2:
        s1 = D1['src'][:]
        s2 = D2['src'][:]
        got = False
        while len(s1) or len(s2):
            if len(s1) and len(s2):
                if s1[0][0] == s2[0][0]:
                    if s1[0][1] == s2[0][1]:
                        if print_samesies:
                            print( template%(s1[0][1],"==%s=="%s1[0][0],s2[0][1]))
                        s1.pop(0)
                        s2.pop(0)
                    else: #elif s1[0][1] != s2[0][1]:
                        if s1[0][1] not in vzz(s2):
                            print(template%(s1[0][1],"!!%s"%s1[0][0],""))
                            s1.pop(0)
                        elif s2[0][1] not in vzz(s1):
                            print(template%("","!!%s"%s[0][0],s2[0][1]))
                            s2.pop(0)
                        else:
                            print(template%(s1[0][1],"!!%s"%s1[0][0],s2[0][1]))
                            s1.pop(0)
                            s2.pop(0)
                else:
                    if s1[0][0] not in kzz(s2):
                        print(template%(s1[0][1],"!!!!%s*"%s1[0][0],""))
                        s1.pop(0)
                    elif s2[0][0] not in kzz(s1):
                        print(template%("","*%s!!!!"%s2[0][0],s2[0][1]))
                        s2.pop(0)
                    else:
                        print(template%(s1[0][1],"**",s2[0][1]))
                        s1.pop(0)
                        s2.pop(0)
            elif len(s1):
                print(s1.pop(0))
            elif len(s2):
                print(s2.pop(0))
            else:
                print("wtf? !!!!!! %d %d"%(len(s1),len(s2)))


dumb=differ(main,new,print_samesies=False)
