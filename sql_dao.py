import json
from sqlalchemy import *
import datetime

DATABASEURI = "postgresql://ky2371:naruhodo@35.196.90.148/proj1part2"
db = create_engine(DATABASEURI)
db.echo = False  # No logging
metadata = MetaData(db)

student = Table('student', metadata, autoload=True)
followership = Table('followership', metadata, autoload=True)
membership = Table('membership', metadata, autoload=True)
circle = Table('circle', metadata, autoload=True)
moment = Table('moment', metadata, autoload=True)
likingmoment = Table('likingmoment', metadata, autoload=True)
momentcomment = Table('momentcomment', metadata, autoload=True)
trend = Table('trend', metadata, autoload=True)
likingtrend = Table('likingtrend', metadata, autoload=True)
trendcomment = Table('trendcomment', metadata, autoload=True)
school = Table('school', metadata, autoload=True)


# return the dict form of attribute and value of one-line sql result
def row2dict(row):
    if row is None:
        return None
    d = {}
    for rs in row.keys():
        d[rs] = row[rs]
    return d


# return the list form of attribute and value of multi=-lines sql results.
# each result in one dict
def multirow2listdict(row):
    if row is None:
        return None
    list = []
    for rs in row:
        dict = {}
        for key in rs.keys():
            dict[key] = rs[key]
        list.append(dict)
    return list


# insert student info into table student
def create_student(info):
    data = []
    statement = "INSERT INTO student ("
    for key in info:
        statement += key
        statement += ','
    statement = statement[0:-1]
    statement += ') VALUES ('
    for key in info:
        statement += "%s"
        data.append(info[key])
        statement += ','
    statement = statement[0:-1]
    statement += ')'
    db.execute(statement, data)
    return


# search student info in student table with student_id
def find_student(id):
    studentinfo = student.select(student.c.user_id == id).alias("studentinfo")
    result = select([studentinfo, school.c.school_name], school.c.school_id==studentinfo.c.school_id)
    resultExe = result.execute()
    rs = resultExe.fetchone()
    s = row2dict(rs)
    return s


# update student info in student table, given the student_id and all the info to be updated
def update_student(id, info):
    data = []
    statement = "UPDATE student SET "
    for key in info:
        statement += key
        statement += '='
        statement += "%s"
        data.append(info[key])
        statement += ','
    statement = statement[0:-1]
    statement += ' WHERE user_id='
    statement += str(id)
    db.execute(statement, data)
    return


# insert new followership
def follow(followerid, followedid, sincetime):
    i = followership.insert()
    i.execute(follower_id=followerid, followed_id=followedid, since=sincetime)
    return


# delete followership
def unfollow(followerid, followedid):
    statement = "DELETE FROM followership WHERE follower_id="
    statement += str(followerid)
    statement += " and followed_id="
    statement += str(followedid)
    db.execute(statement)
    return


# use user_id to find the nickname
def find_student_by_nickname(nickname):
    result = student.select(student.c.nick_name == nickname)
    resultExe = result.execute()
    rs = resultExe.fetchone()
    if rs is None:
        return None
    s = {}
    s['user_id'] = rs.user_id
    return s


# find those users info that I follow
def find_my_followings(userid):
    followingid = followership.select(followership.c.follower_id == userid).alias("follwingid")
    result = student.select(student.c.user_id == followingid.c.followed_id)
    rs = result.execute()
    d = multirow2listdict(rs)
    return d


# find those users info that follow me
def find_my_followers(userid):
    followedid = followership.select(followership.c.followed_id == userid).alias("followedid")
    result = student.select(student.c.user_id == followedid.c.follower_id)
    rs = result.execute()
    d = multirow2listdict(rs)
    return d


# insert new circle
def post_circle(info):
    data = []
    statement = "INSERT INTO circle ("
    for key in info:
        statement += key
        statement += ','
    statement = statement[0:-1]
    statement += ') VALUES ('
    for key in info:
        statement += "%s"
        data.append(info[key])
        statement += ','
    statement = statement[0:-1]
    statement += ')'
    db.execute(statement,data)
    return


# insert new membership record
def join_circle(userid, circleid, sincetime):
    i = membership.insert()
    i.execute(member_id=userid, circle_id=circleid, since=sincetime)
    return


# search circle info using circleid
def find_circle(circleid):
    result = circle.select(circle.c.circle_id == circleid)
    resultExe = result.execute()
    rs = resultExe.fetchone()
    s = row2dict(rs)
    return s


# search circles that the user joined
def find_circles_join(userid):
    circleid = membership.select(membership.c.member_id == userid).alias("circleid")
    result = circle.select(circle.c.circle_id == circleid.c.circle_id)
    rs = result.execute()
    d = multirow2listdict(rs)
    return d


# search circle that the user didn't join in his school
def find_circles_not_join(userid, schoolid):
    data = [schoolid, userid]
    statement = "select c.circle_id, c.circle_name, c.admin_id, c.announcement, c.icon, c.introduction, c.school_id, s.nick_name from circle c, student s where s.user_id = c.admin_id and c.school_id=%s and c.circle_id not in ( select m.circle_id from membership m where m.member_id = %s)"
    rs = db.execute(statement,data)
    d = multirow2listdict(rs)
    return d


# return all the pairs of school id and school name
def find_all_schools():
    s = school.select()
    rs = s.execute()
    d = multirow2listdict(rs)
    return d


# find the moments of mine and the people I follow
def find_moments(userid):
    statement = "SELECT moment.*, s1.nick_name, like_new_moment.like_or_not, like_new_moment.liking_count FROM moment, (SELECT new_moment.moment_id, CASE %s IN (SELECT lm.user_id FROM likingmoment lm WHERE lm.moment_id = new_moment.moment_id) WHEN TRUE THEN 1 ELSE 0 END AS like_or_not, count(likingmoment.user_id) AS liking_count FROM (SELECT moment.* FROM moment, (SELECT DISTINCT followed_id AS user_id FROM followership WHERE followed_id = %s OR follower_id = %s) AS friend WHERE moment.author_id = friend.user_id ORDER BY moment.time) AS new_moment LEFT JOIN likingmoment ON new_moment.moment_id = likingmoment.moment_id GROUP BY new_moment.moment_id) AS like_new_moment, student s1 WHERE moment.moment_id = like_new_moment.moment_id AND moment.author_id = s1.user_id ORDER BY moment.time DESC"
    data = [userid, userid, userid]
    result = db.execute(statement, data)
    d = multirow2listdict(result)
    return d


# insert new moment
def insert_moment(info):
    data = []
    statement = "INSERT INTO moment ("
    for key in info:
        statement += key
        statement += ','
    statement = statement[0:-1]
    statement += ') VALUES ('
    for key in info:
        statement += "%s"
        data.append(info[key])
        statement += ','
    statement = statement[0:-1]
    statement += ')'
    db.execute(statement, data)
    return


# insert new likingmoment
def like_moment(info):
    data = []
    statement = "INSERT INTO likingmoment ("
    for key in info:
        statement += key
        statement += ','
    statement = statement[0:-1]
    statement += ') VALUES ('
    for key in info:
        statement += "%s"
        data.append(info[key])
        statement += ','
    statement = statement[0:-1]
    statement += ')'
    db.execute(statement,data)
    return


# delete likingmoment record
def unlike_moment(userid, momentid):
    statement = "DELETE FROM likingmoment WHERE user_id="
    statement += str(userid)
    statement += " and moment_id="
    statement += str(momentid)
    db.execute(statement)
    return


# insert new record on momentcomment
def comment_moment(info):
    data = []
    statement = "INSERT INTO momentcomment ("
    for key in info:
        statement += key
        statement += ','
    statement = statement[0:-1]
    statement += ') VALUES ('
    for key in info:
        statement += "%s"
        data.append(info[key])
        statement += ','
    statement = statement[0:-1]
    statement += ')'
    db.execute(statement, data)
    return


# give user_id, return all the trends in the circles this user joins with the nick_name of trend authors and the circle_name of circle
def find_trends_in_circles(userid):
    circleid = membership.select(membership.c.member_id == userid).alias("circleid")
    trends = trend.select(circleid.c.circle_id == trend.c.circle_id).alias("trends")
    rs = select([student.c.nick_name, circle.c.circle_name, trends],
                (student.c.user_id == trends.c.author_id) & (circle.c.circle_id == trends.c.circle_id)).order_by(desc(trends.c.time))
    result = rs.execute()
    d = multirow2listdict(result)
    return d


# search all the comments of the moment, given momentid
def find_comments_of_moment(momentid):
    statement = "SELECT S1.nick_name AS \"author_name\", S2.nick_name AS \"to_user\", M.content, M.author_id, M,time FROM student S1, student S2, momentcomment M WHERE M.moment_id = @ AND S1.user_id= M.author_id AND S2.user_id = M.to_user"
    statement = statement.replace("@", str(momentid))
    rs = db.execute(statement)
    result = multirow2listdict(rs)
    return result


# search all the comment of the trend, given trendid
def find_trend_comments(trendid, userid):
    statement = "SELECT x.trend_id, x.nick_name, x.circle_name, x.content, x.image, x.time, x.nick_name, x.author_id, x.circle_id, count(lt1.user_id), CASE # IN (SELECT lt2.user_id FROM likingtrend lt2 WHERE lt2.trend_id = @) WHEN TRUE THEN 1 ELSE 0 END AS like_or_not FROM (SELECT t1.*, c1.circle_name, s1.nick_name FROM trend t1, circle c1, student s1 WHERE t1.trend_id = @ AND t1.circle_id = c1.circle_id AND s1.user_id = t1.author_id) AS x LEFT JOIN likingtrend lt1 ON lt1.trend_id = x.trend_id GROUP BY x.trend_id, x.circle_name, x.nick_name, x.content, x.image, x.time, x.author_id, x.circle_id"
    statement = statement.replace("@", str(trendid))
    statement = statement.replace("#", str(userid))
    print(statement)
    result = {}
    trendone = db.execute(statement)
    result["trend"] = multirow2listdict(trendone)[0]
    trendinfo2 = trend.select(trendid == trend.c.trend_id).alias("trendinfo2")
    commentinfo = trendcomment.select(trendcomment.c.trend_id == trendinfo2.c.trend_id).alias("commentinfo")
    commentinfofull = select([student.c.nick_name, commentinfo], student.c.user_id == commentinfo.c.author_id)
    commentexe = commentinfofull.execute()
    result["comment"] = multirow2listdict(commentexe)
    return result


# insert new trend into table trend
def post_trend(info):
    data = []
    statement = "INSERT INTO trend ("
    for key in info:
        statement += key
        statement += ','
    statement = statement[0:-1]
    statement += ') VALUES ('
    for key in info:
        statement += "%s"
        data.append(info[key])
        statement += ','
    statement = statement[0:-1]
    statement += ')'
    db.execute(statement, data)
    return


# insert new likingtrend record into table likingtrend
def like_trend(info):
    data = []
    statement = "INSERT INTO likingtrend ("
    for key in info:
        statement += key
        statement += ','
    statement = statement[0:-1]
    statement += ') VALUES ('
    for key in info:
        statement += "%s"
        data.append(info[key])
        statement += ','
    statement = statement[0:-1]
    statement += ')'
    db.execute(statement, data)
    return


# delete likingtrend record
def unlike_trend(userid, trendid):
    statement = "DELETE FROM likingtrend WHERE user_id="
    statement += str(userid)
    statement += " and trend_id="
    statement += str(trendid)
    db.execute(statement)
    return


# insert new comment on trend, giving the authorid, trendid, content and time
def comment_trend(info):
    data = []
    statement = "INSERT INTO trendcomment ("
    for key in info:
        statement += key
        statement += ','
    statement = statement[0:-1]
    statement += ') VALUES ('
    for key in info:
        statement += "%s"
        data.append(info[key])
        statement += ','
    statement = statement[0:-1]
    statement += ')'
    db.execute(statement,data)
    return
