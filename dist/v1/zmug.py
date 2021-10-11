import mariadb
import os
mdb_user=""
mdb_password=""
mdb_ip=""
mdb_database=""



voidtag=['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']

def console(info):
  if "'" in info or '"' in info:
    info=info.replace("'","").replace('"',"")
  code="<script>console.log('"+info+"')</script>"
  print(code)

def getURL():
  url=os.environ["REQUEST_URI"]
  return url

def getdata(url):
  if url == '/':
    url = '`/`'
  try:
    conn = mariadb.connect(
      user=mdb_user,
      password=mdb_password,
      host=mdb_ip,
      port=3306,
      database=mdb_database
    )
  except mariadb.Error as e:
      print("Error connecting to MariaDB Platform: ",e)

  cur=conn.cursor(named_tuple=True)
  try:
    cur.execute("SELECT * FROM "+url)
    response=cur.fetchall()
  except Exception as e:
    console(e.args[0])
    pass  
  return response

def build(response):
  try:
    data,content,i,cleaner,ctrl_id=response,'',0,[],[]
    while i<len(data):
      parent_id,parent_tag,tag,id,cls,att_typ,att_val,text,clean_id=data[i].parent,data[i].parent_tag,data[i].tag,data[i].id,data[i].cls,data[i].att_typ,data[i].att_val,data[i].text,data[i].clean_id
      ctrl_id.append(id)
      # create tag
      el=newEl(tag,id,cls,att_typ,att_val,text)
      if parent_tag!=None:
        try:
          content=getParent(content,parent_tag,parent_id)
        except Exception as e:
          console("Errore in getElID "+e.args[0])
        content=content[0]+el+content[1]
      else:
        content=content+el
      if clean_id is 1:
        cleaner.append(id)
      i+=1
    #console(content)
    #for ct in ctrl_id:
      #console(ct)
      #content=content.replace("ctrl_id='"+ct+"'","")
    #for id in cleaner:
      #content=content.replace("id='"+id+"'","")
    #content=re.sub("ctrl_id=.*\'","",content)
    print(content)
  except Exception as e:
    console("Errore nel while di costruzione "+e.args[0])
    pass  

def getParent(content,tag,id):
  
  tempco0=content.split("</"+tag+" ctrl_id='"+id+"'>",maxsplit=1)
  if len(tempco0)>1:
    splitted=[tempco0[0],"</"+tag+" ctrl_id='"+id+"'>"+tempco0[1]]
    return splitted
  else:
    console(tag)
    console(tempco0[0])

def newEl(tag,id,cls,att_typ,att_val,text):
  opentag="<"+tag
  closetag="</"+tag
  
  if id!=None:
    opentag=opentag+" id='"+id+"'"
    closetag=closetag+" ctrl_id='"+id+"'"
  if cls!=None:
    cls=cls.replace(","," ")
    if type(cls) is list:
      for cl in cls:
        con_cls=' '+cl
    else:
      con_cls=cls
    opentag=opentag+" class='"+con_cls+"' "
  if att_typ!=None and att_val!=None:
    t,con_att=0,''
    att_typ=att_typ.split(",")
    att_val=att_val.split(",")
    while t<len(att_typ):
      con_att=con_att+" "+att_typ[t]+"='"+att_val[t]+"' "
      t+=1
    opentag=opentag+con_att

  opentag=opentag+">"
  closetag=closetag+">"
#  if tag is in voidtag:
  if tag not in voidtag:
    if text!=None:
      concat=opentag+text+closetag
    else:
      concat=opentag+closetag
  else:
    concat=opentag
  return concat

def header():
  print("Content-Type: text/html")
  print("")
  print("<!DOCTYPE html>")

def start():
  header()
  url=getURL()
  response=getdata(url)
  build(response)
