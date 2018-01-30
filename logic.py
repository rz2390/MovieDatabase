import datetime

from sql_dao import find_student, update_student, follow, unfollow, find_student_by_nickname, \
    find_my_followings, find_my_followers, find_all_schools, create_student, insert_moment, unlike_moment, like_moment, \
    comment_trend, comment_moment, post_trend, like_trend, unlike_trend, post_circle, join_circle, find_circles_join, \
    find_moments, find_comments_of_moment, find_trend_comments, find_trends_in_circles, find_circles_not_join


def login(student_id, password):
    student = find_student(student_id)
    if student is not None and student['password'] == password:
        return student
    else:
        return None


def get_schools_l():
    return find_all_schools()


def get_student_l(user_id):
    return find_student(user_id)


def create_student_l(student):
    student['since'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    create_student(student)
    return find_student(get_student_by_name(student['nick_name'])['user_id'])


def get_student_by_name(nick_name):
    return find_student_by_nickname(nick_name)


def update_student_l(student):
    user_id = student['user_id']
    student.pop('user_id', None)
    update_student(user_id, student)


def follow_l(user_id, following_id):
    follow(user_id, following_id, datetime.datetime.now())
    return


def unfollow_l(user_id, following_id):
    unfollow(user_id, following_id)
    return


def my_following(user_id):
    return find_my_followings(user_id)


def my_follower(user_id):
    return find_my_followers(user_id)


def get_my_moment(user_id):
    moments = find_moments(user_id)
    for i in range(0, len(moments)):
        moments[i]['time'] = moments[i]['time'].strftime("%Y-%m-%d %H:%M")
    print(moments)
    return moments


def like_moment_l(moment_id, user_id):
    like_moment({"moment_id": moment_id, "user_id": user_id, "time": str(datetime.datetime.now())})
    return


def unlike_moment_l(moment_id, user_id):
    unlike_moment(user_id, moment_id)
    return


def comment_moment_l(comment):
    comment['time'] = str(datetime.datetime.now())
    comment['to_user'] = get_student_by_name(comment['to_user'])['user_id']
    comment_moment(comment)
    return


def create_moment_l(moment):
    moment['time'] = str(datetime.datetime.now())
    insert_moment(moment)
    return


def get_comment_momment_l(moment_id):
    comments = find_comments_of_moment(moment_id)
    return comments


def get_my_trend_l(user_id):
    trends = find_trends_in_circles(user_id)
    for i in range(0, len(trends)):
        trends[i]['content'] = trends[i]['content'][0:150]
        trends[i]['time'] = str(trends[i]['time'].strftime("%Y-%m-%d %H:%M:%S"))
    return trends


def get_trend_l(trend_id, user_id=-1):
    trend = find_trend_comments(trend_id, user_id)
    return trend


def like_trend_l(trend_id, user_id):
    like_trend({"trend_id": trend_id, "user_id": user_id, "time": str(datetime.datetime.now())})
    return


def unlike_trend_l(trend_id, user_id):
    unlike_trend(user_id, trend_id)
    return


def create_trend_l(trend):
    trend['time'] = str(datetime.datetime.now())
    post_trend(trend)
    return


def comment_trend_l(comment):
    comment['time'] = str(datetime.datetime.now())
    comment_trend(comment)
    return


def get_my_circle(user_id):
    return find_circles_join(user_id)


def create_circle_l(circle):
    post_circle(circle)
    return


def get_all_circle_l(user_id, school_id):
    return find_circles_not_join(user_id, school_id)


def join_circle_l(circle_id, user_id):
    join_circle(user_id, circle_id, str(datetime.datetime.now()))
    return
