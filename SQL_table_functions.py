#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arcpy

arcpy.env.workspace = r'D:\Arcpy_pro_scripting\silk_projects\cost automation\საპროექტო_ფორმა_14\New File Geodatabase.gdb'



I_Shesasrulebeli_Samushaoebi = "I_Shesasrulebeli_Samushaoebi"
I_fields = ["ID","NAME","TYPE_ID","DIMENSION_ID","AMOUNT","WORKERS", "TIME",
            "WORKER_TYPE_ID", "SHOW", "LINE_TYPE_ID", "WORK_TYPE_NAME",
            "MAIN_WORK_TYPE_NAME", "DIMENSION_NAME", "WORKER_TYPE_NAME", "ACC_WORK_GROUP"]

II_Samushaota_Moculoba_qvesamushaoebi = "II_Samushaota_Moculoba_qvesamushaoebi"

III_Samushaota_Moculoba_masalebi = "III_Samushaota_Moculoba_masalebi"
III_fields = ["ID", "GROUP_ID", "STUFF_ID", "AMOUNT", "WORK_GROUP_NAME","STUFF_ITEM_NAME"]

V_Shemsrulebelta_kategoriebi = "V_Shemsrulebelta_kategoriebi"
V_fields = ["ID", "NAME","PRICE"]

VII_Masalebi = "VII_Masalebi"
VII_fields = ["ID", "NAME", "GROUP_ID", "PRICE", "DIMENSION_ID", "NOMENCLATURE", "DIMENSION_NAME", "GROUP_NAME"]

VIII_Ganzomilebebi = "VIII_Ganzomilebebi"
VIII_fields = ["ID", "NAME"]

# სამუშაოთა ჩამონათვალი name
# განზომილება dimension
# რაოდენობა
# შემსრულებელთა რაოდენობა
# მუშაკების ფასი
# ერთ.ფასი.ლ
# ჯამური ღირებულება

def dimension(DIMENSION_ID):
    with arcpy.da.SearchCursor(VIII_Ganzomilebebi, VIII_fields) as VIII_cursor:
        for row in VIII_cursor:
            if row[0] == DIMENSION_ID:
                return row[1]

def workersPrice(WORKER_TYPE_ID):
    with arcpy.da.SearchCursor(V_Shemsrulebelta_kategoriebi, V_fields) as V_cursor:
        for row in V_cursor:
            if row[0] == WORKER_TYPE_ID:
                return row[2]

#აბრუნებს მასალების ცხრილიდან ფასი,ნომენკლატურა, რაოდენობა. მასალის ID-ის მიხედვით
def Masalebi(ID):
    with arcpy.da.SearchCursor(VII_Masalebi, VII_fields) as I_cursor:
        d = {}
        for row in I_cursor:
            if row[0] == ID: # "მასალის ID"
                d["NAME"] = row[1]
                d["PRICE"] = row[3]
                d["NOMENKLATURA"] = row[5]
                d["DIMENSION"] = row[6]

                # print(d) #price
                return d
if __name__ == '__main__':
    Masalebi(51)




###ფუნქცია 0 JOB Description
def jobDecription(name, raodenoba=1):
    job_desc = {}
    with arcpy.da.SearchCursor(I_Shesasrulebeli_Samushaoebi, I_fields) as I_cursor:
        for row in I_cursor:
            if row[1] == name:
                job_desc["ID"] = int(row[0])
                DIMENSION_ID = row[3]
                job_desc["DIMENSION"] = dimension(DIMENSION_ID)
                job_desc["raodenoba"] = raodenoba
                job_desc["WORKER_TYPE_NAME"] = row[13]
                job_desc["WORKERS"] = row[5]

                job_desc["AMOUNT"] = row[4]
                WORKER_TYPE_ID = row[7]
                job_desc["WORKERS_PRICE"] = workersPrice(WORKER_TYPE_ID)
                job_desc["WORK_TYPE_NAME"] = row[10] #კატეგორია შესასრულებელი სამუშაოს ტიპი:
                job_desc["MAIN_WORK_TYPE_NAME"] = row[12] #შესასრულებელი სამუშაოს ტიპი:
                job_desc["ACC_WORK_GROUP"] = row[14] #ბუღალტერიის კატეგორია

                #ჯამური ღირებულების გამოთვლა
                WORKERS_PRICE = job_desc["WORKERS_PRICE"]
                amount = job_desc["AMOUNT"]
                time = row[6] #ერთ ერთეულზე საჭირო დრო
                time_for_one = time/amount # ერთ ერთეულზე საჭირო კოეფიციენტის გამოყვანა
                job_desc["TIME"] = time_for_one * raodenoba
                workers = row[5]  #მუშების რაოდენობა
                jami = WORKERS_PRICE * workers * time_for_one * raodenoba
                job_desc["JOB_PRICE"] = round(jami,2)
    # print("JOB_DESC ###", job_desc)
    return job_desc
if __name__ == '__main__':
    a = jobDecription(u"ერთარხიანი სატელეფონო კანალიზაციის მშენებლობა (#PX0.35X0.5) გრუნტზე",1.84)
    print(a)





###ფუნქცია 1 ძირიტადი სამუშაო
def ipoveJob_ID(name):
    with arcpy.da.SearchCursor(I_Shesasrulebeli_Samushaoebi, I_fields) as I_cursor:
        for row in I_cursor:
            if row[1] == name:
                return int(row[0]) # "ID"
if __name__ == '__main__':
    a = ipoveJob_ID(u"ბოძის მონტაჟისათვის შესასრულებელი სამუშაო")
    print("ipovejobid:",a)




###ფუნქცია 2 ქვესამუშაოები
def ipove_qvesamushaoebi(id, raodenoba=1): #II სამუშაოთა მოცულობა (სამონტაჟო/სამშენებლო ქვესამუშაოები)
    with arcpy.da.SearchCursor(II_Samushaota_Moculoba_qvesamushaoebi, "*") as II_cursor:
        newdict = {}
        for row in II_cursor:
            if row[2] == id:
                newdict[row[-1]] = row[4] *raodenoba
        # print(newdict)
        return newdict
if __name__ == '__main__':
    ipove_qvesamushaoebi(1278)





###ფუნქცია 3 მასალები
def ipove_masalebi(id, raodenoba=1): #III სამუშაოთა მოცულობა (სამონტაჟო/სამშენებლო ქვესამუშაოები)
    with arcpy.da.SearchCursor(III_Samushaota_Moculoba_masalebi, III_fields) as III_cursor:
        masalebi = {}
        for row in III_cursor:
            if row[1] == id: #GROUP_ID == ID
                amount = row[3] * raodenoba
                d = Masalebi(row[2])
                price_one = d["PRICE"]
                price_sum = d["PRICE"]* amount
                nomenklatura = d["NOMENKLATURA"]
                list = [amount, price_one, price_sum, nomenklatura]
                masalebi[row[5]] = list
        # print("ipove_masalebi",masalebi)
        return masalebi
if __name__ == '__main__':
    ipove_masalebi(1278)

