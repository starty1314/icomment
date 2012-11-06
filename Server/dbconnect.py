# 3rd Part mysql to Python driver, which can help to exchange data between mysql and python
import MySQLdb
# To convert data and send to the client
import json
# To generate the message posting time and user registering time
import time


# To register a new user, it will support password,email,register IP address in the future
# In current version, it only supports to register a user name
# Arguments Explaination:
# 						user_name : user_name is a user's login name, it will become unique in the future version depending the design
#			  						which means, it is not unique, you can use the same name to register as many times as you can in current version

def user_register(user_name):

	# To connect to local mysql server by using MySQLdb library
	conn = MySQLdb.connect(host='localhost',user='root',passwd='toor',db='icomment',port=3306)
	# To get current cursor
	cur = conn.cursor()
	# To generate user registering time, format is year-month-day hour:minute:second
	reg_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	# To generate a sql query text
	sql = 'insert into users values(null,\''+user_name+'\',\'password1\',\'email1\',1,\'' + reg_time + '\')'
	# To execute the generated sql text
	cur.execute(sql)
	# To commit the actions, if not, it will not execute anything
	conn.commit()
	# To close the current cursor
	cur.close()
	# To kill the connection
	conn.close()
	# To return something
	return 'Register sucessfully'

#user_register('test')

# To store user's comment into the database
# Arguments Explaination:
# 						user_name : user_name is the user's login name, its purpose is to get userID index
# 						message : current user's comment
# 						md5 : md5 is an unique ID of the supported website

def store_comment(user_name,message,md5):

	# To connect to local mysql server by using MySQLdb library
	conn = MySQLdb.connect(host='localhost',user='root',passwd='toor',db='icomment',port=3306)
	# To get current cursor
	cur = conn.cursor()
	# To generate user's message posting time, format is year-month-day hour:minute:second
	post_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

	# This set of codes is to get the current user indexID
	# To generate a sql query text
	sql = 'select indexID from users where uName = \'' + user_name + '\''
	# To execute the generated sql text
	cur.execute(sql)
	# To get one set of data from the return results
	uID = cur.fetchone()
	# To convert format from tuple to string
	uID = str(uID)
	# To split out the user ID from the return results
	uID = uID[1: + uID.find("L",1,-1)]

	# This set of codes is to get the supported website indexID
	# To generate a sql query text
	sql = 'select indexID from url where md5 = \'' + md5 + '\''
	# To execute the generated sql text
	cur.execute(sql)
	# To get one set of data from the return results
	urlID = cur.fetchone()
	# To convert format from tuple to string
	urlID = str(urlID)
	# To split out the supported website indexID from the return results
	urlID = urlID[1: + urlID.find("L",1,-1)]


	# To generate a sql query text
	sql = 'insert into comments values(null,\'' + int(urlID) + '\',\''+message+'\',\'' + post_time + '\',' + int(uID) + ')'
	# To execute the generated sql text
	cur.execute(sql)
	# To commit the actions, if not, it will not execute anything
	conn.commit()
	# To close the current cursor
	cur.close()
	# To kill the connection
	conn.close()
	# To return something
	return 'store sucessfully!'

#store_comment('bb','test','F7ADF3E718EBFFFB')

# To return client all the comments history of current website(need to disscus) 
# Arguments Explaination:
# 						url : url link
# 						md5 : md5 is an unique ID of the supported website

def get_all_history(url,md5):

	# To connect to local mysql server by using MySQLdb library
	conn = MySQLdb.connect(host='localhost',user='root',passwd='toor',db='icomment',port=3306)
	# To create a temp list to contain history
	info = []
	# To create a list to contain history
	historylist = []
	# To get current cursor
	cur = conn.cursor()
	# To generate a sql query text
	sql = 'select md5 from url where md5 = \'' + md5 + '\''
	# To execute the generated sql text
	cur.execute(sql)
	# To get one set of data from the return results
	result = cur.fetchone()

	# To judge if the current url exists in the database
	# If there is the current url, create a record( a room ) for it
	# The return reuslt is empty
	if result == None:
		# To generate a sql query text
		sql = 'insert into url values(null,\'' + url + '\',\'' + md5 + '\')'
		# To execute the generated sql text
		cur.execute(sql)
		# To commit the actions, if not, it will not execute anything
		conn.commit()
		# To return an alert
		return 'create a new room for ' + url
	# If there is the room, then to get all the history from it, currently it only gets the latest 2 comments
	else:
		# To generate a sql query text
		sql = 'select c.commentContent,us.uName from comments c, url u,users us where u.md5 = \'' + md5 + '\' and u.indexId = c.urlID and c.uID = us.indexID order by c.commentTime desc limit 0,2'
		#sql = 'select c.commentTime, c.commentContent,us.uName from comments c, url u,users us where u.md5 = \'' + md5 + '\' and u.indexId = c.urlID and c.uID = us.indexID order by c.commentTime desc limit 0,2'
			
		# To execute the generated sql text
		cur.execute(sql)
		# To get all sets of data from the return results
		allhistory = cur.fetchall()
		# To store all the column names in the list
		column_names = [d[0] for d in cur.description]
		
		# To store all the data in to list info
		for row in cur:
 			# To build dict and convert to json format
  			info = json.dumps(dict(zip(column_names, row)))
  			# To append every piece data into list historylist
  			historylist.append(info)
  		
  		print historylist
  		# To return historylist object
  		return historylist

#get_all_history('1','F7ADF3E718EBFFFB')

# To check if system supports the current website
# Arguments Explaination:
# 						url : url link, formant: www.xxx.com

def check_url(url):
	
	# To connect to local mysql server by using MySQLdb library
	conn = MySQLdb.connect(host='localhost',user='root',passwd='toor',db='icomment',port=3306)
	# To get current cursor
	cur = conn.cursor()
	# To generate a sql query text
	sql = 'select url from supportURL where url = \'' + url + '\''
	# To execute the generated sql text
	cur.execute(sql)
	# To get one set of data from the return results
	result = cur.fetchone()
	# To create a list to true result
	info_Ture = {"Supported":"True"}
	# To create a list to false result
	info_False = {"Unsupported":"False"}

	# To judge which result should be returned
	if result == None:
		return info_False
	else:
		return info_Ture

#check_url('www.cnn.com')

def test ():
	conn = MySQLdb.connect(host='localhost',user='root',passwd='toor',db='icomment',port=3306)
	# To get current cursor
	cur = conn.cursor()
	# To generate a sql query text
	sql = 'select commentTime from comments where uID = 1'
	# To execute the generated sql text
	cur.execute(sql)
	# To get one set of data from the return results
	result = cur.fetchone()
	print result[0]
	t = str(result[0])
	print json.dumps(t)

#test()