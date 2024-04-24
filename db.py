import sqlite3


# 알림받기중인 아티스트 정보 select
def select_data(id):
    con = sqlite3.connect('./webScrap.db')
    cur = con.cursor()
    cur.execute("select artist_list from user where id = ?", (id,))
    result = cur.fetchone()
    data = str(*result)
    data = data.split('/')
    con.close()
    return data


# 해당아티스트 구독중인 유저정보 select
def select_sub_userid(id):
    con = sqlite3.connect('./webScrap.db')
    cur = con.cursor()
    cur.execute("select id from user where artist_list like '%'||(select realname from artist where id =?)||'%'", (id,))
    result = cur.fetchall()
    data = []
    for i in result:
        data.append(*i)
    con.close()
    return data



# 알림받기중인 아티스트 정보 select
def select_data(id):
    con = sqlite3.connect('./webScrap.db')
    cur = con.cursor()
    cur.execute("select artist_list from user where id = ?", (id,))
    result = cur.fetchone()
    data = str(*result)
    data = data.split('/')
    con.close()
    return data




# 해당 아티스트를 구독하는 id select
def select_userid(artist):
    con = sqlite3.connect('./webScrap.db')
    cur = con.cursor()
    cur.execute("select id from user where artist_list like ?", (artist,))
    result = cur.fetchall()
    data = []
    for i in result:
        data.append(*i)
    con.close()
    return data



# 새로운 알림 insert
def insert_noti(id, content, origin_content):
    if id =='':
        #print('null값')
        return 0
    try:
        con = sqlite3.connect('./webScrap.db')
        cur = con.cursor()
        cur.execute("insert into noti values(datetime('now','localtime'), ?, ?, ?, ' ')", (id, content, origin_content))
        con.commit()
        con.close()
        return 1
    except:
        #print('이미 존재하는 데이터')
        return 0


# 팀, 닉네임으로 아티스트 id select
def select_id(team, nickname):
    con = sqlite3.connect('./webScrap.db')
    cur = con.cursor()
    cur.execute("select id FROM artist where team = ? and nickname = ?", (team, nickname,))
    result = cur.fetchone()
    con.close()
    if result is None:
        return 0
    else:
        return str(*result)


# 닉네임을 조회했는데 없을 경우 팀 전체 id 조회
# 팀 전체 id select
def select_team_id(team):
    con = sqlite3.connect('./webScrap.db')
    cur = con.cursor()
    cur.execute("select id from artist where team like ?", (team,))
    result = cur.fetchall()
    data = []
    for i in result:
        data.append(*i)
    con.close()
    return data


# 변경된 닉네임으로 테이블 업데이트
def update_nickname(nickname, id):
    con = sqlite3.connect('./webScrap.db')
    cur = con.cursor()
    cur.execute("update artist set nickname = ? where id = ?", (nickname, id,))
    con.commit()
    con.close()
    return 1


# 보내지지않은 알림 select
def select_noti():
    con = sqlite3.connect('./webScrap.db')
    cur = con.cursor()
    cur.execute("select id||content as content from noti order by sysdate desc limit 100")
    result = cur.fetchall()
    data = []
    for i in result:
        data.append(*i)
    con.close()
    return data


# 메시지 원본 select
def select_origin_content(content):
    con = sqlite3.connect('./webScrap.db')
    cur = con.cursor()
    cur.execute("select origin_content from noti where id||content = ?", (content, ))
    result = cur.fetchone()
    con.close()
    return str(*result)

