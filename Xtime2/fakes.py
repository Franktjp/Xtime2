# -*- coding: utf-8 -*-
import random

from faker import Faker
from datetime import date
# from sqlalchemy.exc import IntegrityError
from Xtime2.models import Admin, User, Tag, Movie

from Xtime2.extensions import db

fake = Faker()


def fake_admin():
    admin = Admin(
        username='admin',
        name='Franktjp'
    )
    admin.set_password('123')
    db.session.add(admin)
    db.session.commit()


def fake_user():
    user1 = User(
        name='邰阶平',
        username='Franktjp',
        email='Franktjp@1.com'
    )
    user1.set_password('12345')
    user2 = User(
        name='黄药师',
        username='黄老邪',
        email='huanglaoxie@1.com'
    )
    user2.set_password('12345')
    user3 = User(
        name='丘处机',
        username='傻逼',
        email='shabi@1.com'
    )
    user3.set_password('12345')
    user4 = User(
        name='金轮法王',
        username='哟西',
        email='yoxi@1.com',
        phone='19946255605',
        gender=1,
        birthday=date(1999, 11, 24),
        signature='嘤嘤嘤',
        introduction='嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤怪'
    )
    user4.set_password('12345')

    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()


def fake_movie():
    # 影片是应该通过管理员(root管理员或普通管理员)添加，测试使用假数据
    tag1 = Tag(name='剧情')
    tag2 = Tag(name='喜剧')
    tag3 = Tag(name='短片')
    tag4 = Tag(name='爱情')
    tag5 = Tag(name='动作')
    tag6 = Tag(name='惊悚')
    tag7 = Tag(name='悬疑')
    tag8 = Tag(name='冒险')
    tag9 = Tag(name='动画')
    tag10 = Tag(name='科幻')
    movie1 = Movie(
        name='名侦探柯南：绯色的子弹',
        image='/static/img/movie/名侦探柯南.png',
        desc='《名侦探柯南：绯色的子弹》是《名侦探柯南》系列的第24部剧场版，由永冈智佳\
             担任导演，作品以东京世界运动会的开幕为背景，围绕融合日本先进技术打造的最\
             高时速1000km的“真空超导磁悬浮列车”展开故事。 在万众瞩目的关头，汇集知名\
             赞助商的酒会现场遭遇突发事件，知名企业高官接连遭到绑架，主导案件的赤井秀一\
             与FBI探员们正在幕后监视，而在柯南的抽丝剥茧下，竟发现这起案件与15年前FBI\
             侦破的美国连续绑架事件存在关联。',
        release_date=date(2021, 4, 17),
        mins=110,
        score=6.2
    )
    movie2 = Movie(
        name='肖申克的救赎',
        image='/static/img/movie/肖申克的救赎.jpg',
        desc='银行家安迪因被陷害杀害妻子与她的情夫，被判两个终身监禁。入狱后，影片便以\
        黑人狱友瑞德冷静的旁白来推进。监狱数十年如一日的改造会使原本自由的心灵习惯了牢笼\
        的禁锢，而这也将是安迪的命运？'
        '20世纪40年代末，小有成就的青年银行家安迪（蒂姆·罗宾斯 饰）因涉嫌杀害妻子及她的\
        情人而锒铛入狱。在这座名为肖申克的监狱内，希望似乎虚无缥缈，终身监禁的惩罚无疑注定\
        了安迪接下来灰暗绝望的人生。未过多久，安迪尝试接近囚犯中颇有声望的瑞德（摩根·弗里\
        曼 饰），请求对方帮自己搞来小锤子。以此为契机，二人逐渐熟稔，安迪也仿佛在鱼龙混杂、\
        罪恶横生、黑白混淆的牢狱中找到属于自己的求生之道。他利用自身的专业知识，帮助监狱管\
        理层逃税、洗黑钱，同时凭借与瑞德的交往在犯人中间也渐渐受到礼遇。表面看来，他已如瑞\
        德那样对那堵高墙从憎恨转变为处之泰然，但是对自由的渴望仍促使他朝着心中的希望和目标\
        前进。而关于其罪行的真相，似乎更使这一切朝前推进了一步……',
        release_date=date(1995, 10, 26),
        mins=142,
        score=9.3
    )
    movie3 = Movie(
        name='指环王-王者无敌',
        image='/static/img/movie/指环王-王者无敌.jpg',
        desc='为了完成摧毁魔戒的使命，佛罗多与山姆、咕噜姆继续前往末日火山，他将受到魔戒\
        的诱惑及人性的考验；同时，刚铎国首都米那斯提力斯危在旦夕，阿拉贡拾起王者之剑，在帕\
        兰诺平原展开血之战役。远征队奋力迎向魔戒圣战……'
        '甘道夫和阿拉贡在罗翰国军队与精灵兵的帮助下，取得圣盔谷的胜利，和树胡们一起打败了白\
        袍巫师萨鲁曼的皮蓬和梅利，也赶来与阿拉贡他们会合。遭受重创的索伦并没有善罢干休，准备\
        打一场真正的决战把人类彻底消灭，实现他统治世界的野心。甘道夫知道形势已经到了最后关头，\
        他带着皮平前往刚铎首都米纳斯提力斯，联络人类各路军马，在此决战。 　　另外一边，弗罗多\
        在山姆的陪伴下，继续赶往厄运山的火焰口，完成他们把魔戒投进毁灭之洞的使命。但是，和他们\
        同路的咕噜已经暗生祸心，他要夺回魔戒，在使计摆脱山姆后，咕噜把弗罗多带进了一个死亡黑洞。\
         　　还在罗翰国逗留的阿拉贡，收到了甘道夫的信号，他立刻带上国王塞奥顿和伊奥温，率领罗翰国\
         的军队赶往刚铎首都米纳斯提里斯。半路上，阿拉贡遇到了他的岳父精灵王艾尔隆，后者把当年\
         砍断魔王索伦手臂的纳西尔圣剑交付给阿拉贡，只有依靠这把神剑才可打败索伦，并且统一整个\
         中土世界。 　　阿拉贡拿着纳西尔圣剑前往死亡之谷，唤醒那里被死神禁锢的死亡战士们，使他\
         们成为了新的人类战士，此时，他的好位好友精灵莱戈拉斯和矮人金利也赶了上来，带着浩浩荡荡\
         的大军来到米纳斯提里斯与甘道夫他们汇集在一起。 　　魔王索伦的黑暗军团终于杀到了米纳斯\
         提力斯，在白城前面广袤的佩兰诺平原上，一场决战终于开始了：汹涌的魔兵、巨型的象兵，刀与\
         枪对垒、魔法与神杖相抗，震天的呐喊……惨烈壮观的决战之后，人类大军终于又一次打败了黑暗军\
         团。 　　但是，最后的胜利还没有来到，唯有把魔戒毁灭掉才能够完成人类的最后使命。弗罗多在\
         忠心的山姆帮助下来到厄运山，在他要把魔戒投入火焰的紧急时刻，最可怕的事情发生了……',
        release_date=date(2021, 5, 14),
        mins=201,
        score=8.4
    )
    movie4 = Movie(
        name='哥斯拉大战金刚',
        image='/static/img/movie/哥斯拉大战金刚.jpg',
        desc='',
        release_date=date(2021, 5, 14),
        mins=201,
        score=8.4
    )
    movie5 = Movie(
        name='巴乔：神奇的马尾辫',
        image='/static/img/movie/巴乔：神奇的马尾辫.jpg',
        desc='　这是一部球星罗伯特巴乔22年职业生涯的记录，包括他作为球员艰难的首场比赛\
        以及他和一些教练之间的严重分歧。',
        release_date=date(2021, 5, 26),
        mins=91
    )
    movie6 = Movie(
        name='阿甘正传',
        image='/static/img/movie/阿甘正传.jpg',
        desc='阿甘的智商只有75，但凭借跑步的天赋，他顺利大学毕业。在越南战场，他结识了\
        “捕虾迷”布巴和丹中尉。回国后，阿甘机缘巧合累积了大量资产。不过，钱并不是阿甘所看\
        重的东西。阿甘和珍妮青梅竹马，可珍妮有自己的梦想……',
        release_date=date(1994, 9, 22),
        mins=142,
        score=9.1
    )

    # 多对多数据添加
    movie1.tags = [tag5, tag8, tag9]
    movie2.tags = [tag1]
    movie3.tags = [tag1, tag7, tag10]
    movie4.tags = [tag5, tag8]
    movie5.tags = [tag1, tag8]
    movie6.tags = [tag1, tag4]

    # 数据库事务
    db.session.add_all([tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9, tag10])
    db.session.add_all([movie1, movie2, movie3, movie4, movie5, movie6])
    db.session.commit()

def fake_comment():
    pass


def fake_topic():
    pass


def fake_review():
    pass
