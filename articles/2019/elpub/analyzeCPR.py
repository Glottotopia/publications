import glob  
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import distinct

import math
import numpy as np
import matplotlib.pyplot as plt
import pprint

#prepare db
Base = declarative_base()

class Paperhive(Base):
    __tablename__ = 'paperhive' 
    bookID = Column(Integer, primary_key=True)
    commentID = Column(Integer, primary_key=True)
    proofreaderID = Column(String(12))
    pagenumber = Column(Integer)
    startpos = Column(Integer)
    endpos = Column(Integer)
    title = Column(String(42))
    body = Column(String(32768))
     

engine = create_engine('sqlite:///data/paperhive.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession() 

#plotting functions

def boxplot(data, bottom, top, label, filename):
    fig1, ax1 = plt.subplots()
    plt.ylim(bottom,top)
    ax1.set_title(label)
    ax1.boxplot(data)
    fig1.show()
    fig1.savefig(filename)
    
def barplot(data, bottom, top, label, filename):
    fig1, ax1 = plt.subplots()
    #plt.ylim(bottom,top)
    ax1.set_title(label)
    min_ = min(data)
    max_ = max(data)
    x = [i+min_ for i in range(max_+1-min_)]
    d = dict(zip(x,[0 for i in x]))
    for el in data: 
        d[el] += 1
    y = [d[i] for i in x]
    plt.bar(x,y)
    fig1.show()
    fig1.savefig(filename)
    
def scatter(data, bottom, top, label, filename):
    fig1, ax1 = plt.subplots()
    plt.ylim(bottom,top)
    ax1.set_title(label)
    ax1.scatter([0 for x in data],data)
    fig1.show()
    fig1.savefig(filename)
    
def power(data, bottom, top, label, filename):
    fig1, ax1 = plt.subplots()
    plt.ylim(bottom,top)
    plt.xlim(-1,len(data)+1)
    ax1.set_title(label)
    data.sort(reverse=True)
    ax1.scatter([i for i,x in enumerate(data)],data)
    fig1.show()
    fig1.savefig(filename)

 
pagenumbers={ 
80:164,
85:651,
98:576,
103:160,
106:220,
107:162,
109:640,
115:340,
118:468,
120:402,
123:430,
132:522,
141:400,
144:494,
148:492,
152:334,
153:417,
155:415,
156:273,
159:416,
160:498,
163:108,
165:564,
166:341,
167:505,
174:526,
176:136,
178:320, 
179:185,
180:298,
183:292,
184:356,
186:259,
187:247,
190:252,
191:468,
192:758,
194:294,
196:329,
201:440,
202:316,
203:204,
204:406,
209:138,
210:340,
212:476,
216:296,
219:206,
220:262,
225:370,
226:334,
227:504
}
 
#output 
#print("number of books",len(session.query(Paperhive.bookID).distinct().all()))

#totalpages = sum([pagenumbers[key] for key in pagenumbers.keys()])
#print("total number of pages",totalpages)

#print("number of pages with comments",len(session.query(Paperhive.bookID,Paperhive.pagenumber).distinct().all()))

#totalcomments=len(session.query(Paperhive.bookID,Paperhive.commentID).distinct().all())
#print("number of comments",totalcomments) 

#print("number of different proofreaders",len(session.query(Paperhive.proofreaderID).distinct().all()))

#print("avg number of comments per page",(0.0+totalcomments)/totalpages)

#for bookID in pagenumbers:
    #numberofcomments = totalcomments=len(session.query(Paperhive)\
                                            #.filter(Paperhive.bookID==bookID)\
                                            #.all()
                                            #)
    ##print("{}: {} comments; {:.2f} per page".format(bookID, numberofcomments,  (0.0+numberofcomments)/pagenumbers[bookID]))
    
##booklength    
#booklengths = [pagenumbers[key] for key in pagenumbers]
#boxplot(booklengths,0,max(booklengths)+10,'Book lengths in pages',"booklengths.png")
##scatter(booklengths,0,max(booklengths)+10,'Book lengths in pages',"booklengths_s.png")
#power(booklengths,0,max(booklengths)+10,'Book lengths in pages',"booklengths_p.png")

##amount of comments
#numberofcommentsd = dict(session.query(Paperhive.bookID,func.count(Paperhive.commentID)).group_by(Paperhive.bookID).all())
#numberofcommentslist = [numberofcommentsd[key] for key in numberofcommentsd]
#boxplot(numberofcommentslist,0,max(numberofcommentslist)+10,'Comments per book',"commentsperbook.png")
##scatter(numberofcommentslist,0,max(numberofcommentslist)+10,'Comments per book',"commentsperbook_s.png")
#power(numberofcommentslist,0,max(numberofcommentslist)+10,'Comments per book',"commentsperbook_p.png")

##comment density
#commentsperpage = {}
#for key in pagenumbers:
    #commentsperpage[key] = numberofcommentsd[key]/pagenumbers[key]

#commentsperpagelist = [commentsperpage[key] for key in commentsperpage]
#boxplot(commentsperpagelist,0,max(commentsperpagelist)+1,'Comments per page per book',"commentsperpageperbook.png")
##scatter(commentsperpagelist,0,max(commentsperpagelist)+1,'Comments per page per book',"commentsperpageperbook_s.png")
#power(commentsperpagelist,0,max(commentsperpagelist)+1,'Comments per page per book',"commentsperpageperbook_p.png")


##number of proofreaders (long tail) 
#proofreadersperbook = sorted(session.query(func.count(distinct(Paperhive.proofreaderID)), Paperhive.bookID ).group_by(Paperhive.bookID).all(),reverse=True)
#proofreadersperbooklist = [x[0] for x in proofreadersperbook]
#boxplot(proofreadersperbooklist,0,max(proofreadersperbooklist)+1,'Proofreaders per book',"proofreadersperbook.png") 
#barplot(proofreadersperbooklist,0,max(proofreadersperbooklist)+1,'Proofreaders per book',"proofreadersperbook_b.png") 
##scatter(proofreadersperbooklist,0,max(proofreadersperbooklist)+1,'Proofreaders per book',"proofreadersperbook_s.png") 
#power(proofreadersperbooklist,0,max(proofreadersperbooklist)+1,'Proofreaders per book',"proofreadersperbook_p.png") 
    
##Comments for each page    
#commentsforeachpage = session.query(Paperhive.bookID,Paperhive.pagenumber,func.count(Paperhive.commentID)).group_by(Paperhive.bookID, Paperhive.pagenumber).all()
#print("highest number of comments: book %s on page %s has %s comments"% sorted(commentsforeachpage, key=lambda x: x[2])[-1])
#commentsforeachpagelist = sorted(x[2] for x in commentsforeachpage)
#boxplot(commentsforeachpagelist,0,max(commentsforeachpagelist)+1,'Comments per page',"commentsperpage.png")  
#power(commentsforeachpagelist,0,max(commentsforeachpagelist)+1,'Comments per page',"commentsperpage_p.png")  

##books per proofreader 
#booksperproofreader = sorted(session.query(func.count(distinct(Paperhive.bookID)), Paperhive.proofreaderID ).group_by(Paperhive.proofreaderID).all(),reverse=True)
#booksperproofreaderlist = [x[0] for x in booksperproofreader]
#power(booksperproofreaderlist,0,max(booksperproofreaderlist)+1,'Books per proofreader',"booksperproofreader_p.png") 


##pages per proofreader #TODO
#pagesperproofreader = sorted(session.query(func.count(Paperhive.pagenumber), Paperhive.proofreaderID).distinct(Paperhive.bookID,Paperhive.pagenumber).group_by(Paperhive.pagenumber,Paperhive.bookID).all(),reverse=True)
#pagesperproofreaderlist = [x[0] for x in pagesperproofreader]
#power(pagesperproofreaderlist,0,max(pagesperproofreaderlist)+1,'Pages per proofreader',"pagesperproofreader_p.png") 

##comments per proofreader 
#commentsperproofreader = sorted(session.query(func.count(Paperhive.commentID), Paperhive.proofreaderID).group_by(Paperhive.proofreaderID).all(),reverse=True)
#commentsperproofreaderlist = [x[0] for x in commentsperproofreader]
#power(commentsperproofreaderlist,0,max(commentsperproofreaderlist)+1,'Comments per proofreader',"commentsperproofreader_p.png") 

##longest streak
#proofreaderbookpagetuples = session.query(Paperhive.proofreaderID,Paperhive.bookID,Paperhive.pagenumber).distinct().all()
#proofreaderbookpagetuples.sort()
#maxstreak = 0   
#streaktext = ''
#proofreaders = [x[0] for x in proofreaderbookpagetuples]
#bookIDs= [x[1] for x in proofreaderbookpagetuples]
#pages = [x[2] for x in proofreaderbookpagetuples]
#d = {}
#for proofreader in proofreaders:
    #d[proofreader] = {}
    #for bookID in bookIDs:
        #d[proofreader][bookID] = []
#for pr, b, pg in proofreaderbookpagetuples: 
        #d[pr][b].append(pg) 
#for pr in d:
    #for b in d[pr]:
        #maxcount = 0
        #pagelist = sorted(d[pr][b])
        #count = 1
        #for i, p in enumerate(pagelist):
            #try:
                #if pagelist[i+1] == pagelist[i]+1:
                    #count += 1
                    #if count > maxcount:
                        #maxcount = count
                #else:
                    #count = 1
            #except IndexError:
                #pass
        #if maxcount > maxstreak:
            #streaktext = "Proofreader %s has %s consecutive pages with comments in book %s" %( pr,maxcount,b)            
            #maxstreak = maxcount
#print(streaktext)        
    
##avg title length
#titles = [x[0] for x in session.query(Paperhive.title).all()]
#bodies = [x[0] for x in session.query(Paperhive.body).all()]
 
#titlelengths = [len(x) for x in titles]
#bodylengths = [len(x) for x in bodies if x!='']
 
#avgtitlelength = sum(titlelengths)/len(titlelengths)
#avgbodylength = sum(bodylengths)/len(bodylengths)


#print("Average title length:",avgtitlelength)
#print("Average body length:",avgbodylength)

#boxplot(titlelengths,0,max(titlelengths)+1,'Title length',"titlelength.png")  
#barplot(titlelengths,0,max(titlelengths)+1,'Title length',"titlelength_b.png")  

#boxplot(bodylengths,0,max(bodylengths)+1,'Body length',"bodylength.png")  
#power(bodylengths,0,max(bodylengths)+1,'Body length',"bodylength_p.png") 

#mostfrequentcomments = ['"%s": %s'%x 
                            #for x in 
                            #session.query(Paperhive.title,
                                          #func.count(distinct(Paperhive.commentID)).label('count')
                                          #).group_by(Paperhive.title)\
                                        #.order_by('count')\
                                        #.all()[-50:][::-1]
                        #]
#print("Most frequent comments")                            
#print("\n".join(["\t%s"%x for x in mostfrequentcomments]))                            

#cluster
fourtuple = session.query(Paperhive.bookID,Paperhive.proofreaderID,Paperhive.title,Paperhive.body).all()
d = dict(zip(pagenumbers.keys(),[{} for x in pagenumbers])) 
for book, pr, title, body in fourtuple:
    try:
        d[book][pr].append(len(title)+len(body))
    except KeyError:
        d[book][pr]=[len(title)+len(body)]
fig1, ax1 = plt.subplots()
#plt.ylim(bottom,top)
ax1.set_title("count and avg length of comments (ranked)")
mastercountvalues = []
masteravgvalues  = []
for book in d:  
    counts = []
    avgs = []
    countranks = []
    lengthranks = []
    
    countrankd  = {}
    avgrankd  = {}
    
    for pr in d[book]: 
        commentcount = len(d[book][pr])
        avgcommentlength = sum(d[book][pr])/len(d[book][pr]) 
        counts.append(commentcount)
        countranks.append((commentcount,pr))
        avgs.append(avgcommentlength)
        lengthranks.append((avgcommentlength,pr))        
    #print(countranks)
    countranks.sort()
    for i, c in enumerate(countranks): 
        pr = c[1]
        countrankd[pr] = i+.5 #store rank of this proofreader 
    lengthranks.sort() 
    for i, c in enumerate(lengthranks): 
        pr = c[1]
        avgrankd[pr] = i+.5 #store rank of this proofreader 
    factor = 100/len(countrankd)
    countvalues = [countrankd[key]*factor for key in countrankd]    
    avgvalues = [avgrankd[key]*factor for key in countrankd]   
    mastercountvalues += countvalues
    masteravgvalues += avgvalues
plt.ylim(0,101)
plt.xlim(0,101)
ax1.scatter(mastercountvalues,masteravgvalues)
plt.plot(np.unique(mastercountvalues), np.poly1d(np.polyfit(mastercountvalues, masteravgvalues, 1))(np.unique(mastercountvalues)),color='red')
        
        #plt.text(countvalues[i], avgvalues[i], [x[:3] for x in countrankd.keys()][i], fontsize=9)
fig1.show()
fig1.savefig("allscatter.png")


fivetuple = session.query(Paperhive.bookID,Paperhive.proofreaderID,Paperhive.pagenumber,Paperhive.title,Paperhive.body).all()

d = {}
for book, proofreader, pagenumber, title, body in fivetuple: 
    try:
        d[(book,proofreader)]
    except KeyError:        
        d[(book,proofreader)] = {}
    try:
        d[(book,proofreader)][pagenumber]
    except KeyError:
        d[(book,proofreader)][pagenumber] = []
    d[(book,proofreader)][pagenumber].append(len(title)+len(body))

# We store the relative length of a comment (e.g. 1.37) as compared to the average
# The relative position of a comment is computed as the index in the list of comments
# and as the page position in the relevant stretch. Both relative metrics are normalized to 0..1
# All correspondences are copied from the individual books to masterlists for plotting

masterratios = []
masterprogress = []
masterpageprogress = []

#Proofreaders can work on more than one chapter. 
#If there are more than 20 pages between two adjacent comments by the same proofreader,
#this is considered as establishing a new stretch and the counter is reset

for key in d:     
    pagenumbers = sorted(d[key].keys())
    
    #default: there is only one stretch for this book for this proofreader
    stretches = [[pagenumbers]]
    
    #store where adjacent comments are far away so that we split the stretches
    splitters = []
    for i,number in enumerate(pagenumbers):
        try:
            if pagenumbers[i+1] > pagenumbers[i] + 20: 
                splitters.append(i+1)
        except IndexError: #reached end of list, perform split
            stretches = [pagenumbers[i:j] for i, j in zip([0] + splitters, splitters + [None])] 
    for stretch in stretches:
        startpage = stretch[0]
        stretchlength = stretch[-1]-stretch[0]+1
        stretchcomments = [] #store all comments for this stretch without nesting 
        #consolidatedpagecomments = []
        pageswithcomments = [] #store the pagenumbers for the consolidated comments
        for pagenumber in stretch:
            pagecomments = d[key][pagenumber]
            stretchcomments += pagecomments            
            #append n times the pagenumber to make sure the comments list and the page number list match
            commentsthispage = len(pagecomments)
            pageswithcomments += [(pagenumber+1-startpage) for x in range(commentsthispage)]  
            
        #compute general statistics    
        totalstretchcomments = len(stretchcomments)
        totallengthcomments = sum(stretchcomments)
        avglengthcomment = totallengthcomments/totalstretchcomments
        
        #compute value for individual comments
        ratios = [(x/avglengthcomment) for x in stretchcomments] 
        #compute progress as measured as index of comment list
        progress = [n/len(stretchcomments) for n, x in enumerate(stretchcomments)]
        #compute progress as measured according to page numbers
        pageprogress = [p/stretchlength for p in pageswithcomments]
        
        #copy over
        masterratios += ratios
        masterprogress += progress 
        masterpageprogress += pageprogress 
        
fig1, ax1 = plt.subplots()
plt.ylim(0,5)
plt.xlim(0,1)
ax1.set_title("relative comment length per stretch")
ax1.scatter(masterprogress,masterratios,s=.1)
plt.plot(np.unique(masterprogress), np.poly1d(np.polyfit(masterprogress, masterratios, 1))(np.unique(masterprogress)),color='red')
fig1.show()
fig1.savefig("stretches.png")


fig1, ax1 = plt.subplots()
plt.ylim(0,5)
plt.xlim(0,1)
ax1.set_title("relative comment length per stretch according to position of page")
ax1.scatter(masterpageprogress,masterratios,s=.1)
plt.plot(np.unique(masterpageprogress), np.poly1d(np.polyfit(masterpageprogress, masterratios, 1))(np.unique(masterpageprogress)),color='red')
fig1.show()
fig1.savefig("stretchespages.png") 
 

    