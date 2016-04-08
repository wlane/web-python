#!/usr/local/bin/python
# -*- utf8 -*-


#全局连接池，由全局变量__poop储存，缺省情况下编码为utf8，自动提交事务
@asyncio.coroutine
def create_pool(loop,**kw):
	logging.info('create database connection pool...')
	global __pool
	__pool=yield from aiomysql.create_pool(
	host=kw.get('host','localhost')，
	port=kw.get('port',3306)，
	user=kw['user']，
	password=kw['password']，
	db=kw['db']，
	charset=kw.get['charset','utf8']，
	autocommit=kw.get['autocommit',True]，
	maxsize=kw.get['maxsize',10]，
	minsize=kw.get['minsize',1]，
	loop=loop
	)


#执行select语句,使用带参数的sql，不要拼接字符串，size确定返回语句的数量
@asyncio.coroutine
def select(sql,args,size=None):
	log(sql,args)
	global __pool
	with (yield from __pool) as conn:
    	cur=yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?','%s'),args or ())
		if size:
			rs=yield from cur.fetchmany(size)
		else:
			rs=yield from fetchall()
		yield from cur.close()
		logging.info('rows returned:%s' % len(rs))
		return rs


#执行insert，update，delete语句
@asyncio.coroutine
def execute(sql,args):
	log(sql)
	with(yield from __pool) as conn:
	try:
		cur=yield from conn.cursor
		yield from cur.execute(sql.replace('?','%s'),args)
		affected=cur.rowcount
		yield from cur.close()
	except BaseException as e:
		raise
	return affected



