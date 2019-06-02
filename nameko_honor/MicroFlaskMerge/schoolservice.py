# -*- coding: utf-8 -*-
"""
author: dxy
"""
from nameko.rpc import rpc
import json

import db
from config_for_service import DB_CONFIG


# 需要预先调用，且只调用一次
db.create_engine(**DB_CONFIG)


class School(object):
    name = "school"



    @rpc
    def get_id_by_school_name(self, school_name, institution_name):
        """
        根据学校的名字和学院名获取对应的学校id和学院id，若不存在则返回空的字典
        :param school_name: 学校名
        :param institution_name: 学院名
        :return: {school_id: 1, institution_id: 1}
        """
        sql = ("select SCHOOL_ID as school_id, ID as institution_id"
               " from es_institution where SCHOOL_NAME = ? and NAME=?")
        # 查找
        results = db.select(sql, school_name, institution_name)
        if len(results) == 0:
            return {}
        else:
            return results[0]

    @rpc
    def get_keylab_id_by_institution(self,school_name,institution_name):
        """
        用于查找国家重点实验室ID
        :param school_name:学校名
        :param institution_name: 院系名
        :return: 国家重点实验室ID
        """
        if institution_name != '':
            sql = ("select id from main_lab where org = ? and institution = ?")
            results = db.select(sql,school_name,institution_name)
            return results
        else:
            sql = ("select id from main_lab where org = ?")
            results = db.select(sql, school_name)
            return results


    @rpc
    def get_keylab_name_by_institution(self,lab_id):
        """
        用于根据国家重点实验室ID查询其信息
        :param lab_id:国家重点实验室ID
        :return: 国家重点实验室信息
        """
        sql  = ("select name,org as school_name,institution as institution_name from main_lab where id=?")
        results = db.select(sql,lab_id)
        return results[0]

    @rpc
    def get_evaluation_by_institution(self,institution_id):
        """
        用于根据院系ID查询该院系学科信息
        :param institution_id:
        :return:
        """
        sql = ("select EVALUATION as evaluation from es_relation_in_dis where ID = ?")
        results = db.select(sql,institution_id)
        if len(results) == 0:
            return {}
        else:
            return results[0]


    @rpc
    def get_honor_name(self):
        """
        获取honor中所有头衔，奖项名
        """
        sql = "select distinct HONOR from es_honor"
        results = db.select(sql)
        return results

    @rpc
    def get_honor_by_institution_id(self,institution_id):
        """
        获取一个院系的honor
        """
        sql = "select es_honor.HONOR as honor from es_teacher join es_honor where es_teacher.ID = es_honor.TEACHER_ID and es_teacher.INSTITUTION_ID = ?"
        results = db.select(sql,institution_id)
        return results

    @rpc
    def get_honor_by_institutuion_and_name(self,institution_id,name):
        """
        由院系ID和教师姓名获取这个教室的头衔及获奖情况
        """
        sql = "select es_honor.HONOR as honor from es_teacher join es_honor where es_teacher.ID = es_honor.TEACHER_ID and es_teacher.INSTITUTION_ID = ? and es_teacher.NAME = ?"
        results = db.select(sql,institution_id,name)
        return results


    @rpc
    def get_project_by_institution_id(self,institution_id):
        """
        获取院系的项目
        """
        sql = "SELECT eval_project.TYPE as TYPE FROM eval_project join es_teacher where eval_project.PERSON = es_teacher.`NAME` and es_teacher.INSTITUTION_ID = ?"
        results = db.select(sql,institution_id)
        return results

    @rpc
    def get_project_by_school_and_name(self,school_name,teacher_name):
        """
        从eval_project表获取教师的项目
        """
        sql = "select TYPE as type,PROJECT_NAME as name from eval_project where PERSON = ? and ORG = ?"
        results = db.select(sql,teacher_name,school_name)
        return results

    @rpc
    def get_project_from_jijin_by_school_and_name(self,school_name,teacher_name):
        """
        从jijin表取得教师的项目
        """
        sql = "SELECT title FROM `jijin` where name = ? and org = ?"
        results = db.select(sql,teacher_name,school_name)
        return results




