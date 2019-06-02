# -*- coding: utf-8 -*-
#李家明，王崇愚，陈难先，李惕碚，顾秉林，范守善，邝宇平
from flask import Flask,request
from flask import render_template
import time
from nameko.standalone.rpc import ClusterRpcProxy
import json

from config import CONFIG   #导入微服务模块

app = Flask(__name__)



@app.route('/general_search')
def general_search():
    return render_template("general_search.html")

@app.route('/general_info',methods=['GET','POST'])
def general_info():
    """
    获得院士，长江，杰青的信息
    获得实验室的信息
    获得重点学科的信息
    获得项目的信息
    """
    if request.method == "POST":
        with ClusterRpcProxy(CONFIG) as rpc:
            school_name = request.form.get('schoolName')
            institution_name = request.form.get('institutionName')
            school_id = rpc.school.get_id_by_school_name(school_name,institution_name)['school_id']
            institution_id = rpc.school.get_id_by_school_name(school_name,institution_name)['institution_id']

            # 获取该学院的重点实验室ID
            lab_ids = rpc.school.get_keylab_id_by_institution(school_name, institution_name)
            if len(lab_ids) == 0:
                lab_num = 0
            # 将重点实验室信息存入list中
            lab_id_list = []
            for lab_id_dic in lab_ids:
                lab_id_list.append(lab_id_dic['id'])
            #国家重点实验室数量
            lab_num = len(lab_id_list)

            #获取学科信息
            evaluation = rpc.school.get_evaluation_by_institution(institution_id).get('evaluation')

            #获取院士，长江，杰青，奖项信息
            #获取es_honor表中所有HONOR的所有内容，即各种奖项和头衔
            honor = rpc.school.get_honor_name()
            honor_list = []
            for honor_dic in honor:
                honor_list.append(honor_dic['HONOR'])
        #下面是先找到院系的老师，然后再去查找每个老师的荣誉，效率很低，不如联表查询
            #获取院系的所有老师id
           #  teacher_ids = rpc.school.get_teacher_ids_by_institution_id(institution_id)
           #  teacher_ids_list = []
           #  for teacher_id_dic in teacher_ids:
           #      teacher_ids_list.append(teacher_id_dic['teacher_id'])
           #
            honor_all = {}
            for honor_name in honor_list:
                honor_all[honor_name] = 0
            teacher_honors = rpc.school.get_honor_by_institution_id(institution_id)
            for teacher_honor_dict in teacher_honors:
                if teacher_honor_dict['honor'] in honor_list:
                    honor_all[teacher_honor_dict['honor']] += 1
            #将同样的头衔、奖项但不同等级（如自然科学奖的一等奖，二等奖合并，计算数目，用于展示)
            honor_all_display = {'院士':0,'长江学者':0,'杰出青年':0,'自然科学奖':0,'技术发明奖':0,'科技进步奖':0}
            for honor_name_1 in honor_all_display:
                for honor_name_2 in honor_all:
                    if honor_name_1 in honor_name_2:
                        honor_all_display[honor_name_1] += honor_all[honor_name_2]

            #获取项目信息
            project_all = {'重点研发计划':0,'自然基金':0}
            teacher_projects = rpc.school.get_project_by_institution_id(institution_id)
            for teacher_project_dict in teacher_projects:
                if teacher_project_dict['TYPE'] in project_all:
                    project_all[teacher_project_dict['TYPE']] += 1

            return render_template("general_info.html",school_name = school_name,institution_name = institution_name,lab_num = lab_num,evaluation = evaluation,honor_all_display = honor_all_display,project_all = project_all)



            #return str(lab_num)+'，'+evaluation+','+str(honor_all_display)+str(project_all)

            #根据学校名，院系名，人名查找荣誉

@app.route('/',methods=['GET','POST'])
def honor_search():
    return render_template("honor_search.html")

@app.route('/honor_info',methods=['GET','POST'])
def honor_info():
    if request.method == "POST":
        with ClusterRpcProxy(CONFIG) as rpc:
            #获取学校id及院系id以及教师名字
            school_name = request.form.get('schoolName')
            institution_name = request.form.get('institutionName')
            school_id = rpc.school.get_id_by_school_name(school_name,institution_name)['school_id']
            institution_id = rpc.school.get_id_by_school_name(school_name,institution_name)['institution_id']
            teachers_name = request.form.get('teachersName')
            if "，" in teachers_name:
                teacherNameList = teachers_name.split("，")
            elif "," in teachers_name:
                teacherNameList = teachers_name.split(",")
            else:
                teacherNameList = teachers_name.split(" ")
            honor_dict = {}

            for teacher_name in teacherNameList:
                honor_dict[teacher_name] = {"title":[],"award":[],"key_research_project":[],"nature_fund":[],"other_project":[]}
            for teacher_name in teacherNameList:
                teacher_honor_list = rpc.school.get_honor_by_institutuion_and_name(institution_id,teacher_name)
                teacher_project_list = rpc.school.get_project_by_school_and_name(school_name,teacher_name)
                teacher_project_jijin_list = rpc.school.get_project_from_jijin_by_school_and_name(school_name,teacher_name)
                for teacher_honor_dict in teacher_honor_list:
                    if "院士" in teacher_honor_dict["honor"] or "长江学者" in teacher_honor_dict["honor"] or "杰出青年" in teacher_honor_dict["honor"]:
                        honor_dict[teacher_name]["title"].append(teacher_honor_dict["honor"])
                    if "奖" in teacher_honor_dict["honor"]:
                        honor_dict[teacher_name]["award"].append(teacher_honor_dict["honor"])
                for teacher_project_dict in teacher_project_list:
                    if teacher_project_dict["type"] == "重点研发计划":
                        honor_dict[teacher_name]["key_research_project"].append(teacher_project_dict["name"])
                    else:
                        honor_dict[teacher_name]["nature_fund"].append(teacher_project_dict["name"])
                for teacher_project_dict in teacher_project_jijin_list:
                    honor_dict[teacher_name]["other_project"].append(teacher_project_dict["title"])
            return  render_template("honor_info.html",honor_dict = honor_dict)


if __name__ == '__main__':
    app.run()
