import db
from config import DB_CONFIG


# 需要预先调用，且只调用一次
db.create_engine(**DB_CONFIG)

def get_lab_info():
    """
    获取国家重点实验室信息
    :return:
    """
    lab_info = []
    sql = "select id,org,institution from main_lab"
    results = db.select(sql)
    for result in results:
        lab_info.append((result['id'],result['org'],result['institution']))
    return lab_info



def get_institution_info():
    """
    获取院系信息
    :return:
    """
    institution_info = []
    sql = "select ID,SCHOOL_NAME,NAME from es_institution"
    results = db.select(sql)
    for result in results:
        institution_info.append((result['ID'],result['SCHOOL_NAME'],result['NAME']))
    return institution_info


def institution_lab_insert(lab_info,institution_info):
    """
    写入数据库
    :param lab_info:
    :param institution_info:
    :return:
    """
    institution_lab = []
    #匹配国家重点实验室和其对应院系
    for institution in institution_info:
        for lab in lab_info:
            if lab[1] == institution[1] and lab[2] == institution[2]:
                institution_lab.append((institution[0],lab[0]))
    #将国家重点实验室和院系的对应信息写入数据库
    for relationship_tuple in institution_lab:
        sql = "insert into institution_lab_new (institution_id,lab_id) values (?,?)"
        db.insert(sql, relationship_tuple)



if __name__== "__main__":
    #国家重点实验室信息
    lab_info = get_lab_info()
    #学院信息
    institution_info = get_institution_info()
    #将数据写入数据库
    institution_lab_insert(lab_info,institution_info)









