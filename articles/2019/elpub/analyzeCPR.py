import glob  
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
216:280,
219:202,
220:257,
225:357,
226:322,
227:480
}
 
print("number of books")  
print(len(session.query(Paperhive.bookID).distinct().all()))
print("total number of pages")  
totalpages = sum([pagenumbers[key] for key in pagenumbers.keys()])
print(totalpages)
print("number of pages with comments") 
print(len(session.query(Paperhive.bookID,Paperhive.pagenumber).distinct().all()))
print("number of comments") 
totalcomments=len(session.query(Paperhive.bookID,Paperhive.commentID).distinct().all())
print(totalcomments) 
print("number of different proofreaders")
print(len(session.query(Paperhive.proofreaderID).distinct().all()))
print("avg number of comments per page")
print((0.0+totalcomments)/totalpages)

for bookID in pagenumbers:
    numberofcomments = totalcomments=len(session.query(Paperhive)\
                                            .filter(Paperhive.bookID==bookID)\
                                            .all()
                                            )
    print("{}: {} comments; {:.2f} per page".format(bookID, numberofcomments,  (0.0+numberofcomments)/pagenumbers[bookID]))

#proofreader crossed page (xy chart)
#date range 
#echo
#compute
#log
#plot
    