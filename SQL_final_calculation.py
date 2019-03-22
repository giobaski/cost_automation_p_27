#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
import os
import SQL_cost_automation_second
import SQL_table_functions


arcpy.env.workspace = r'D:\Arcpy_pro_scripting\silk_projects\cost automation\საპროექტო_ფორმა_14\New File Geodatabase.gdb'
arcpy.env.overwriteOutput = True



# #GIS-ში დახაზული სამუშაოების ჯამი
# gis_results = {u'ბოძის მონტაჟისათვის შესასრულებელი სამუშაო': 2,
#                u'ერთარხიანი სატელეფონო კანალიზაციის მშენებლობა სავალ ნაწილზე (გრუნტი) (#PX0.35X0.7)': 10.0,
#                u'ერთარხიანი სატელეფონო კანალიზაციის მშენებლობა (#PX0.35X0.5) გრუნტზე': 1.84}


main_jobs = {}
main_sub_jobs = {}
main_masalebi = {} #მაგ:. {u'ქვიშა/შავი': [0.1, 34.03, 3.4030000000000005, 'A0100005947']}
for k, v in SQL_cost_automation_second.gis_results.items():
    job_id = SQL_table_functions.ipoveJob_ID(k) #returns job_id

    sub_jobs = SQL_table_functions.ipove_qvesamushaoebi(job_id, v) #returs sub_jobs and amounts
    main_sub_jobs[k] = sub_jobs

    sub_masalebi = SQL_table_functions.ipove_masalebi(job_id,v ) #returns  masalebi and amounts გამრავლებული რაოდენობაზე

    # იდენტური მასალების შეჯამება და main_masalebi-ში გაერთიანება
    for key in sub_masalebi.keys():
        if key in main_masalebi:
            moculoba = main_masalebi[key][0] + sub_masalebi[key][0]
            erteulis_fasi = sub_masalebi[key][1]
            saerto_fasi = main_masalebi[key][2] + sub_masalebi[key][2]
            nomenklatura = sub_masalebi[key][3]
            list = [moculoba, erteulis_fasi, saerto_fasi, nomenklatura]
            main_masalebi[key] = list
            print("aris:", main_masalebi)
        else:
            main_masalebi[key] = sub_masalebi[key]

        job_description = SQL_table_functions.jobDecription(k,v)
        main_jobs[k] = job_description
    print("job_description: ",job_description)
    print("job_ID: ", job_id)
    print("Sub_jobs:", sub_jobs)
    print("sub_masalebi:", sub_masalebi, "\n")

print("main_jobs: ", main_jobs)
print("main_sub_jobs: ", main_sub_jobs)
print("main_masalebi: ", main_masalebi)










import xlsxwriter
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Results_01.xlsx')
worksheet = workbook.add_worksheet("project_CRM_ID")


# worksheet.set_column('A:H',35, border)
# worksheet.set_column("A:A", 45)
worksheet.set_column("B:B", 50)
worksheet.set_column("A:H", 30)

#Fancy Cell Formatting
size = workbook.add_format({
    'font': {'color': 'red',
             'size': 14}
})

border = workbook.add_format({
    "border":1
})

jami_cell = workbook.add_format({
    "bg_color": "#88b4ef",
    "border":2
})

top_cell = workbook.add_format({
    'bold': True,
    "font_color": "red"
})

bold = workbook.add_format({
    'bold': True
})

header = workbook.add_format({
    'bold': True,
    "border":1
})

worksheet.insert_image('A1', 'logo.png')




#HEADERS
masalebi_header =    ["No.", u"მასალის დასახელება",     u"ნომენკლატურა", u"განზომილება", u"რაოდენობა",                u"ერთ. ფასი ლ.",   u"ჯამური ღირებულება"]
samushaoebi_header = ["No.", u"სამუშაოთა ჩამონათვალი", u"განზომილება",   u"რაოდენობა",   u"შემსრულებლის რაოდენობა", u"მუშაკების ფასი",  u"ერთ. ფასი ლ.",      u"ჯამური ღირებულება"]
saboloo_jami_header = ["No.", u"დასახელება", u"კოეფიციენტი", u"ჯამური ღირებულება(ლ)"]


#TABLE 1: Start from the first cell. Rows and columns are zero indexed.
row = 3
col = 0
header_num = 2


ID = 1
I_jami = 0 #სამუშაოების ჯამური ღირებულება
for key, value in main_jobs.items():
    if value['WORK_TYPE_NAME'] == u'სამშენებლო':
        # Iterate over the data and write it out row by row.
        worksheet.write(1, 0, u"სამშენებლო სამუშაოები: ", top_cell)  # აღწერა

        worksheet.write_row(header_num, 0, samushaoebi_header, header) #Header

        worksheet.write(row, col + 0, ID,border)  # No
        worksheet.write(row, col + 1, key,border)  # სამუშაოთა ჩამონათვალი
        worksheet.write(row, col + 2, value["DIMENSION"],border)  # განზომილება
        worksheet.write(row, col + 3, value["raodenoba"], border)  # რაოდენობა
        worksheet.write(row, col + 4, value["WORKERS"],border)  # შემსრულებლის რაოდენობა
        worksheet.write(row, col + 5, value["WORKERS_PRICE"],border)  # მუშაკების ფასი
        worksheet.write(row, col + 6, round(value["TIME"],2) ,border)  # ერთ. ფასი ლ.
        worksheet.write(row, col + 7, value["JOB_PRICE"],border)  # ჯამური ღირებულება
        row += 1
        I_jami += value["JOB_PRICE"]

        sub_ID = ID + 0.1
        for i in main_sub_jobs[key]:
            worksheet.write(row, col + 0,   sub_ID, border) #No
            worksheet.write(row, col + 1,   i, border) #სამუშაოთა ჩამონათვალი
            row += 1
            sub_ID += 0.1
        ID+=1
        print(row)
print("I jami:", I_jami)
# Write a total using a formula.
worksheet.write(row, 1, u'ჯამი I',top_cell)
worksheet.write(row, 7, '=SUM(H{}:H{})'.format(header_num+1,row), jami_cell)
#შეინახე I ჯამი, საბოლოო ღირებულების ფორმულისთვის
# I_jami = '=SUM(H{}:H{})'.format(header_num+1,row)




#TABLE 2: Start from the first cell. Rows and columns are zero indexed.
row+=3
worksheet.write(row, 0, u"მასალები: ", top_cell) #აღწერა
row+=1
header_num = row
row += 1
col = 0

# Iterate over the data and write it out row by row.
ID = 1
II_jami = 0 #სამუშაოების ჯამური ღირებულება
for key, value in main_masalebi.items():
    worksheet.write_row(header_num,0, masalebi_header, header) #Header

    worksheet.write(row, col + 0,      ID,border) #No
    worksheet.write(row, col + 1,      key,border) #მასალის დასახელება
    worksheet.write(row, col + 2, value[3],border) #ნომენკლატურა
    worksheet.write(row, col + 3, u"განზომილება დასამტებელია",border) #განზომილება
    worksheet.write(row, col + 4, value[0],border) #რაოდენობა
    worksheet.write(row, col + 5, value[1],border) #ერთეულის ფასი
    worksheet.write(row, col + 6, value[2],border) #ჯამური ღირებულება
    II_jami += value[2]
    row += 1
    ID+=1
print(row)
print("II jami:", II_jami)

# Write a total using a formula.
worksheet.write(row, 1, u'ჯამი II',top_cell)
worksheet.write(row, 6, '=SUM(G{}:G{})'.format(header_num+1,row), jami_cell)
#შეინახე II ჯამი, საბოლოო ღირებულების ფორმულისთვის
# II_jami = '=SUM(G{}:G{})'.format(header_num+1,row)




#TABLE 3: Start from the first cell. Rows and columns are zero indexed.
row+=3
worksheet.write(row, 0, u"სამშენებლო სამუშაოების ჯამი: ", top_cell) #აღწერა
row+=1
header_num = row
row += 1
col = 0

# Iterate over the data and write it out row by row.
I_II = I_jami+II_jami
transport = I_II * 0.04
I_II_transport = I_II + transport
gaut_xarji = I_II * 0.03
saerto_jami = I_II_transport + gaut_xarji



worksheet.write_row(header_num,0, saboloo_jami_header, header) #Header

worksheet.write(row, col + 0,   1,border)                   #No.
worksheet.write(row, col + 1,   u"I ჯამი + II ჯამი",border)   #დასახელება
worksheet.write(row, col + 2,   "", border)                  #კოეფიციენტი
worksheet.write(row, col + 3,   I_II,border)       #ჯამური ღირებულება(ლ)
row += 1
worksheet.write(row, col + 0,      2,border) #No.
worksheet.write(row, col + 1,      u"ტრანსპ. ხარჯი",border) #დასახელება
worksheet.write(row, col + 2, u"4%",border) #კოეფიციენტი
worksheet.write(row, col + 3, transport ,border) #ჯამური ღირებულება(ლ)
row += 1
worksheet.write(row, col + 0,      3,border) #No.
worksheet.write(row, col + 1,      u"ჯამი",border) #დასახელება
worksheet.write(row, col + 2, "",border) #კოეფიციენტი
worksheet.write(row, col + 3, I_II_transport ,border) #ჯამური ღირებულება(ლ)
row += 1
worksheet.write(row, col + 0,      3,border) #No.
worksheet.write(row, col + 1,      u"გაუთვ. ხარჯი",border) #დასახელება
worksheet.write(row, col + 2, u"3%",border) #კოეფიციენტი
worksheet.write(row, col + 3, gaut_xarji ,border) #ჯამური ღირებულება(ლ)
row += 1
worksheet.write(row, col + 0,     "") #No.
worksheet.write(row, col + 1,      u"საერთო ჯამი",top_cell) #დასახელება
worksheet.write(row, col + 2, "") #კოეფიციენტი
worksheet.write(row, col + 3, saerto_jami,jami_cell) #ჯამური ღირებულება(ლ)
row += 1
print(row)

#END 3


workbook.close()

os.startfile('Results_01.xlsx')