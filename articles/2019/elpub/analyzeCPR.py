import glob  
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import distinct

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
80:159,
85:637,
98:576,
103:151,
106:210,
107:157,
109:606,
115:325,
118:446,
120:387,
123:405,
132:522,
141:391,
144:490,
148:326,
152:321,
153:406,
155:407,
156:263,
159:407,
160:468,
163:101,
165:541,
166:329,
167:499,
174:526,
176:136,
178:315,
179:164,
180:290,
183:281,
184:350,
186:255,
187:236,
190:247,
191:443,
192:754,
194:253,
196:318,
201:414,
202:312,
203:191,
204:389,
209:134,
210:336,
212:468,
216:280,
219:202,
220:257,
225:357,
226:322,
227:480
}
 
#output 
#print("number of books")  
#print(len(session.query(Paperhive.bookID).distinct().all()))
#print("total number of pages")  
#totalpages = sum([pagenumbers[key] for key in pagenumbers.keys()])
#print(totalpages)
#print("number of pages with comments") 
#print(len(session.query(Paperhive.bookID,Paperhive.pagenumber).distinct().all()))
#print("number of comments") 
#totalcomments=len(session.query(Paperhive.bookID,Paperhive.commentID).distinct().all())
#print(totalcomments) 
#print("number of different proofreaders")
#print(len(session.query(Paperhive.proofreaderID).distinct().all()))
#print("avg number of comments per page")
#print((0.0+totalcomments)/totalpages)

#for bookID in pagenumbers:
    #numberofcomments = totalcomments=len(session.query(Paperhive)\
                                            #.filter(Paperhive.bookID==bookID)\
                                            #.all()
                                            #)
    #print("{}: {} comments; {:.2f} per page".format(bookID, numberofcomments,  (0.0+numberofcomments)/pagenumbers[bookID]))
    
#booklength    
booklengths = [pagenumbers[key] for key in pagenumbers]
boxplot(booklengths,0,max(booklengths)+10,'Book lengths in pages',"booklengths.png")
scatter(booklengths,0,max(booklengths)+10,'Book lengths in pages',"booklengths_s.png")

#amount of comments
numberofcommentsd = dict(session.query(Paperhive.bookID,func.count(Paperhive.commentID)).group_by(Paperhive.bookID).all())
numberofcommentslist = [numberofcommentsd[key] for key in numberofcommentsd]
boxplot(numberofcommentslist,0,max(numberofcommentslist)+10,'Comments per book',"commentsperbook.png")
scatter(numberofcommentslist,0,max(numberofcommentslist)+10,'Comments per book',"commentsperbook_s.png")
power(numberofcommentslist,0,max(numberofcommentslist)+10,'Comments per book',"commentsperbook_p.png")

#comment density
commentsperpage = {}
for key in pagenumbers:
    commentsperpage[key] = numberofcommentsd[key]/pagenumbers[key]

commentsperpagelist = [commentsperpage[key] for key in commentsperpage]
boxplot(commentsperpagelist,0,max(commentsperpagelist)+1,'Comments per page per book',"commentsperpageperbook.png")
scatter(commentsperpagelist,0,max(commentsperpagelist)+1,'Comments per page per book',"commentsperpageperbook_s.png")
power(commentsperpagelist,0,max(commentsperpagelist)+1,'Comments per page per book',"commentsperpageperbook_p.png")


#number of proofreaders (long tail)#TODO gives implausible result
proofreadersperbook = sorted(session.query(func.count(distinct(Paperhive.proofreaderID)), Paperhive.bookID ).group_by(Paperhive.bookID).all(),reverse=True)
proofreadersperbooklist = [x[0] for x in proofreadersperbook]
boxplot(proofreadersperbooklist,0,max(proofreadersperbooklist)+1,'Proofreaders per book',"proofreadersperbook.png") 
scatter(proofreadersperbooklist,0,max(proofreadersperbooklist)+1,'Proofreaders per book',"proofreadersperbook_s.png") 
power(proofreadersperbooklist,0,max(proofreadersperbooklist)+1,'Proofreaders per book',"proofreadersperbook_p.png") 
    
#Comments for each page    
commentsforeachpage = session.query(Paperhive.bookID,Paperhive.pagenumber,func.count(Paperhive.commentID)).group_by(Paperhive.bookID, Paperhive.pagenumber).all()
print("highest number of comments: book %s on page %s has %s comments"% sorted(commentsforeachpage, key=lambda x: x[2])[-1])

#books per proofreader 

booksperproofreader = sorted(session.query(func.count(distinct(Paperhive.bookID)), Paperhive.proofreaderID ).group_by(Paperhive.proofreaderID).all(),reverse=True)
booksperproofreaderlist = [x[0] for x in booksperproofreader]
power(booksperproofreaderlist,0,max(booksperproofreaderlist)+1,'Books per proofreader',"booksperproofreader_p.png") 
 


#proofreader crossed page (xy chart)

    