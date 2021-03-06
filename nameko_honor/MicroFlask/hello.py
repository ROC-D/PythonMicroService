# -*- coding: UTF-8 -*-
from nameko.rpc import rpc
import pymysql

class Compute(object):
    name = "test"

    @rpc
    def test(self):
        return "hello"

    @rpc
    def compute(self):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select TEACHER_ID from es_honor where HONOR like '%院士%' "
        cursor.execute(sql)
        teacher_id = cursor.fetchall()
        return teacher_id

    @rpc
    def compute1(self,id):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,charset='utf8')
        cursor = db.cursor()
        sql = "select NAME from es_teacher where ID = %s "
        cursor.execute(sql,(id))
        teacher_name = cursor.fetchone()
        return teacher_name

    @rpc
    def compute2(self):
        teacher_name = []
        teacher_id = self.compute()
        for i in teacher_id:
            teacher_name.append(self.compute1(i))
        return teacher_name

    @rpc
    def get_institutionId(self,schoolName,institutionName):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306, charset='utf8')
        cursor = db.cursor()
        sql = "select ID from es_institution where SCHOOL_NAME = %s and NAME = %s "
        cursor.execute(sql, (schoolName,institutionName))
        institution_id = cursor.fetchall()
        return institution_id

    @rpc
    def get_schoolId(self,schoolName):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select SCHOOL_ID from es_institution where SCHOOL_NAME = %s"
        cursor.execute(sql, (schoolName))
        school_id = cursor.fetchone()
        return school_id

    @rpc
    def get_teacher_name_and_insId(self,school_id):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select NAME,INSTITUTION_ID,HOMEPAGE from es_teacher where SCHOOL_ID = %s and ACADEMICIAN > 1"
        cursor.execute(sql, (school_id))
        teacher = cursor.fetchall()
        return teacher

    @rpc
    def get_institution_name(self,institution_ID):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select NAME from es_institution where ID = %s "
        cursor.execute(sql, (institution_ID))
        institution_id = cursor.fetchone()
        return institution_id

    @rpc
    def get_academicianName(self,institution_id):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306, charset='utf8')
        cursor = db.cursor()
        sql = "select NAME, HOMEPAGE from es_teacher where INSTITUTION_ID = %s and ACADEMICIAN > 0 "
        cursor.execute(sql, (institution_id))
        teacher_name = cursor.fetchall()
        return teacher_name

    @rpc
    def get_institutionNamebyschoolName(self,schoolname):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select NAME from es_institution where SCHOOL_NAME = %s "
        cursor.execute(sql, (schoolname))
        institution_name = cursor.fetchall()
        return institution_name

class document(object):
    name = "document"

    # 根据学校名，学院名获取学院ID
    @rpc
    def get_institutionId(self, schoolName, institutionName):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select ID from es_institution where SCHOOL_NAME = %s and NAME = %s "
        cursor.execute(sql, (schoolName, institutionName))
        institution_id = cursor.fetchone()
        institution_id = institution_id[0]
        return institution_id

    # 根据学院id获取学院中所有老师的ID,姓名，是否院士，是否杰出青年，是否长江学者
    @rpc
    def get_teacher_info(self, institutionId):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select ID,NAME,ACADEMICIAN,OUTYOUTH,CHANGJIANG from es_teacher where INSTITUTION_ID = %s"
        cursor.execute(sql, (institutionId))
        teacherInfo = cursor.fetchall()
        return teacherInfo

    # 根据学校名，学院名获取重点实验室名
    @rpc
    def get_lab(self, school_name, institution_name):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "SELECT name FROM main_lab where org= %s and institution = %s "
        cursor.execute(sql, (school_name, institution_name))
        lab = cursor.fetchall()
        lab_name = []
        for i in lab:
            b = i[0].index("（")
            lab_name.append(i[0][0:b])
        return lab_name

    # 获取领头人领域
    @rpc
    def get_fields(self, institution_id, teacher_name):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "SELECT FIELDS FROM es_teacher where INSTITUTION_ID = %s and NAME = %s "
        cursor.execute(sql, (institution_id, teacher_name))
        fields = cursor.fetchone()
        return fields

    # 根据学院id获取重点学科代码，评价
    @rpc
    def get_maindis(self, institution_id):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = '''SELECT DISCIPLINE_CODE,EVALUATION FROM es_relation_in_dis where INSTITUTION_ID = %s and (EVALUATION = 'A+' or EVALUATION = 'A')'''
        cursor.execute(sql, (institution_id))
        maindis = cursor.fetchall()
        return maindis

    # 根据老师id获取合著老师姓名，合著数量
    @rpc
    def get_relation(self, teacher_id):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select teacher2_name,paper_num from teacher_teacher where teacher1_id = %s"
        cursor.execute(sql, (teacher_id))
        teacher_list = cursor.fetchall()
        return teacher_list

    # 根据学科代码获取学科名
    @rpc
    def get_discipline(self, discipline_code):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "SELECT NAME FROM es_discipline where CODE = %s"
        cursor.execute(sql, (discipline_code))
        discipline_name = cursor.fetchone()
        discipline_name = discipline_name[0]
        return discipline_name

    # 根据老师名，学院id,获取老师ID
    @rpc
    def get_teacher_id(self, name, institution):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "SELECT ID FROM es_teacher where NAME = %s and INSTITUTION_ID = %s"
        cursor.execute(sql, (name, institution))
        teacher_id = cursor.fetchone()
        return teacher_id

    # 根据学校名获取带头人姓名，项目名，项目年份
    @rpc
    def get_project(self, org):
        db = pymysql.connect(host='47.104.236.183', db='eds_spider', user='root', password='SLX..eds123', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "SELECT PERSON,PROJECT_NAME,FUNDS,YEAR FROM eval_project where ORG = %s and FUNDS is not NULL"
        cursor.execute(sql, (org))
        project = cursor.fetchall()
        project_list = []
        for i in project:
            project_list.append(i)
        return project_list

    # 根据作者id,年份获取论文所有作者，论文名
    @rpc
    def get_paper_info_1(self, author_id, year):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "SELECT author,name from eds_paper_clean where author_id = %s and year = %s"
        cursor.execute(sql, (author_id, year))
        paper = cursor.fetchall()
        paperlist = []
        for i in paper:
            paperlist.append(i[0])
        return paperlist

    # 根据作者id,获取论文所有作者，论文名
    @rpc
    def get_paper_info_2(self, author_id):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "SELECT author,name from eds_paper_clean where author_id = %s"
        cursor.execute(sql, (author_id))
        paper = cursor.fetchall()
        # paperlist = []
        # for i in paper:
        #     paperlist.append(i[0])
        return paper

    # 根据老师ID，年份获取荣誉
    @rpc
    def get_honor_1(self, teacher_id, year):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select HONOR from es_honor where TEACHER_ID = %s and year = %s"
        cursor.execute(sql, (teacher_id, year))
        honor = cursor.fetchall()
        return honor

    # 根据老师ID，年份获取荣誉
    @rpc
    def get_honor_2(self, teacher_id):
        db = pymysql.connect(host='47.106.83.33', db='eds_base', user='root', password='111111', port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = "select HONOR from es_honor where TEACHER_ID = %s"
        cursor.execute(sql, (teacher_id))
        honor = cursor.fetchall()
        return honor

    # 创建文档
    @rpc
    def createdocument(info):
        document = Document()
        # 创建段落
        p = document.add_paragraph("")
        # 设置段落左右居中
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # 设置段落的段前间距
        p.paragraph_format.space_before = Pt(5)
        # 设置段落得断后间距
        p.paragraph_format.space_after = Pt(5)
        # 设置行间距
        p.paragraph_format.line_spacing = Pt(8)
        # 设置段落间距的格式为最小值
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.AT_LEAST
        run = p.add_run(info["school_name"] + "科研简报" + info["institution_name"] + info["data"])
        # 设置字体
        run.font.name = u'宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
        # 颜色设置，这里是用RGB颜色
        run.font.color.rgb = RGBColor(0, 0, 0)
        # 设置字体大小
        run.font.size = Pt(21)
        # 字体是否加粗
        run.bold = True
        # 无下划线
        run.underline = WD_UNDERLINE.NONE

        # 创建表格
        table = document.add_table(rows=1, cols=1)
        # 表格风格
        table.style = "Table Grid"

        for row in table.rows:
            # 设置每行表格高度
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

        # 在表格中写入文字
        run = table.cell(0, 0).paragraphs[0].add_run("一、院系概况")
        # 设置表格中字体
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        # 字体大小
        run.font.size = Pt(15)
        # 字体大小
        run.font.color.rgb = RGBColor(91, 155, 213)
        # 是否加粗
        run.bold = True
        # 字上下居中
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=2)
        # 表格风格
        table.style = "Table Grid"

        for row in table.rows:
            # 设置每行表格高度
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

        run = table.cell(0, 0).paragraphs[0].add_run("国家重点学科")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(237, 125, 49)
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        run = table.cell(0, 1).paragraphs[0].add_run("评价")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(237, 125, 49)
        table.cell(0, 1).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # 创建表格
        table = document.add_table(rows=len(info["discipline_name"]), cols=2)
        # 表格风格
        table.style = "Table Grid"

        for row in table.rows:
            # 设置每行表格高度
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

        key = []
        value = []
        for i in info["discipline_name"].keys():
            key.append(i)
        for i in info["discipline_name"].values():
            value.append(i)
        count = len(info["discipline_name"])

        for i in range(0, count):
            run = table.cell(i, 0).paragraphs[0].add_run(key[i])
            run.font.name = u'微软雅黑'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0, 0, 0)
            table.cell(i, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

            run = table.cell(i, 1).paragraphs[0].add_run(value[i])
            run.font.name = u'微软雅黑'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0, 0, 0)
            table.cell(i, 1).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        run = table.cell(0, 0).paragraphs[0].add_run("科研平台")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(237, 125, 49)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        run = table.cell(0, 0).paragraphs[0].add_run(info["mainlab"])
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        run = table.cell(0, 0).paragraphs[0].add_run("院系成员")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(237, 125, 49)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # 插入图片
        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(390)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

        item = table.cell(0, 0)
        p = item.paragraphs[0]
        p.add_run().add_picture(info["picture"], Pt(380), Pt(380))
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        run = table.cell(0, 0).paragraphs[0].add_run("二、科研项目")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(91, 155, 213)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=5)
        table.cell(0, 0).merge(table.cell(0, 1))
        table.cell(0, 2).merge(table.cell(0, 3)).merge(table.cell(0, 4))
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

        run = table.cell(0, 0).paragraphs[0].add_run("项目名称")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(237, 125, 49)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        run = table.cell(0, 2).paragraphs[0].add_run(info["project_name"])
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        table.cell(0, 2).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        run = table.cell(0, 0).paragraphs[0].add_run("项目成员")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(237, 125, 49)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=4, cols=5)
        table.style = "Table Grid"
        for i in range(0, 4):
            table.cell(i, 0).merge(table.cell(i, 1))
            table.cell(i, 2).merge(table.cell(i, 3)).merge(table.cell(i, 4))

        run = table.cell(0, 0).paragraphs[0].add_run("院士")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        run = table.cell(0, 2).paragraphs[0].add_run(
            i + "，" for i in info["academician_list"][0: (len(info["academician_list"]) - 1)])
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        table.cell(0, 2).paragraphs[0].paragraph_format.space_before = Pt(2)
        table.cell(0, 2).paragraphs[0].paragraph_format.space_after = Pt(6)
        table.cell(0, 2).paragraphs[0].paragraph_format.line_spacing = Pt(30)
        table.cell(0, 2).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        run1 = table.cell(0, 2).paragraphs[0].add_run(info["academician_list"][len(info["academician_list"]) - 1])
        run1.font.name = u'微软雅黑'
        run1._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run1.font.size = Pt(12)

        run = table.cell(1, 0).paragraphs[0].add_run("长江学者")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        run.bold = True
        table.cell(1, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        run = table.cell(1, 2).paragraphs[0].add_run(
            i + "，" for i in info["changjiang_list"][0: (len(info["changjiang_list"]) - 1)])
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        table.cell(1, 2).paragraphs[0].paragraph_format.space_before = Pt(2)
        table.cell(1, 2).paragraphs[0].paragraph_format.space_after = Pt(6)
        table.cell(1, 2).paragraphs[0].paragraph_format.line_spacing = Pt(30)
        table.cell(1, 2).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        run1 = table.cell(1, 2).paragraphs[0].add_run(info["changjiang_list"][len(info["changjiang_list"]) - 1])
        run1.font.name = u'微软雅黑'
        run1._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run1.font.size = Pt(12)

        run = table.cell(2, 0).paragraphs[0].add_run("杰出青年")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        run.bold = True
        table.cell(2, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        run = table.cell(2, 2).paragraphs[0].add_run(
            i + "，" for i in info["outyouth_list"][0: (len(info["outyouth_list"]) - 1)])
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        table.cell(2, 2).paragraphs[0].paragraph_format.space_before = Pt(2)
        table.cell(2, 2).paragraphs[0].paragraph_format.space_after = Pt(6)
        table.cell(2, 2).paragraphs[0].paragraph_format.line_spacing = Pt(30)
        table.cell(2, 2).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        run1 = table.cell(2, 2).paragraphs[0].add_run(info["outyouth_list"][len(info["outyouth_list"]) - 1])
        run1.font.name = u'微软雅黑'
        run1._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run1.font.size = Pt(12)

        run = table.cell(3, 0).paragraphs[0].add_run("其他成员")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        run.bold = True
        table.cell(3, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        run = table.cell(3, 2).paragraphs[0].add_run(
            i + "，" for i in info["other_list"][0: (len(info["other_list"]) - 1)])
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        table.cell(3, 2).paragraphs[0].paragraph_format.space_before = Pt(2)
        table.cell(3, 2).paragraphs[0].paragraph_format.space_after = Pt(6)
        table.cell(3, 2).paragraphs[0].paragraph_format.line_spacing = Pt(30)
        table.cell(3, 2).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        run1 = table.cell(3, 2).paragraphs[0].add_run(info["other_list"][len(info["other_list"]) - 1])
        run1.font.name = u'微软雅黑'
        run1._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run1.font.size = Pt(12)

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        run = table.cell(0, 0).paragraphs[0].add_run("项目成果")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(237, 125, 49)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        run = table.cell(0, 0).paragraphs[0].add_run("论文成果")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        run = table.cell(0, 0).paragraphs[0].add_run(
            "《" + i + "》\n" for i in info["paper"][0: (len(info["paper"]) - 1)])
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        table.cell(0, 0).paragraphs[0].paragraph_format.space_before = Pt(2)
        table.cell(0, 0).paragraphs[0].paragraph_format.space_after = Pt(6)
        table.cell(0, 0).paragraphs[0].paragraph_format.line_spacing = Pt(30)
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        run1 = table.cell(0, 0).paragraphs[0].add_run("《" + info["paper"][len(info["paper"]) - 1] + "》" + "  等")
        run1.font.name = u'微软雅黑'
        run1._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run1.font.size = Pt(12)

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        run = table.cell(0, 0).paragraphs[0].add_run("专利成果")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        run = table.cell(0, 0).paragraphs[0].add_run(i for i in info["invention"][0: (len(info["invention"]) - 1)])
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        table.cell(0, 0).paragraphs[0].paragraph_format.space_before = Pt(2)
        table.cell(0, 0).paragraphs[0].paragraph_format.space_after = Pt(6)
        table.cell(0, 0).paragraphs[0].paragraph_format.line_spacing = Pt(30)
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        run1 = table.cell(0, 0).paragraphs[0].add_run(info["invention"][len(info["invention"]) - 1] + "  等")
        run1.font.name = u'微软雅黑'
        run1._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run1.font.size = Pt(12)
        run2 = table.cell(0, 0).paragraphs[0].add_run("\n")
        run2.font.name = u'微软雅黑'
        run2._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run2.font.size = Pt(12)

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        for row in table.rows:
            row.height = Pt(30)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        run = table.cell(0, 0).paragraphs[0].add_run("获奖成果")
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        run.bold = True
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        run = table.cell(0, 0).paragraphs[0].add_run(i for i in info["award"][0: (len(info["award"]) - 1)])
        run.font.name = u'微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run.font.size = Pt(12)
        table.cell(0, 0).paragraphs[0].paragraph_format.space_before = Pt(2)
        table.cell(0, 0).paragraphs[0].paragraph_format.space_after = Pt(6)
        table.cell(0, 0).paragraphs[0].paragraph_format.line_spacing = Pt(30)
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        run1 = table.cell(0, 0).paragraphs[0].add_run(info["award"][len(info["award"]) - 1])
        run1.font.name = u'微软雅黑'
        run1._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')
        run1.font.size = Pt(12)

        # 保存文档
        document.save("3.docx")



