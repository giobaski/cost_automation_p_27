#!/usr/bin/env python
# -*- coding: utf-8 -*-


import arcpy
from datetime import datetime
from openpyxl import Workbook
import crm_tables
import my_functions
# import cost_automation_second



# ფუნქცია, რომელიც მასალების ფასებს აბრუნებს CRM_ცხრილიდან:
# def material_price_search_in_table(material_name):
#     #კურსორისთვის საჭირო ველების ჩამონათვალი
#     fields = ['Category', 'Name', 'Price', 'Nomenclature']
#     table = r'D:\Arcpy_pro_scripting\silk_projects\cost automation\საპროექტო_ფორმა_14\New File Geodatabase.gdb\material'
#
#     with arcpy.da.SearchCursor(table, fields) as material_cursor:
#         for row in material_cursor:
#             if row[1] == material_name:
#                 price = row[2]
#                 return row
#
# print(material_price_search_in_table("ცემენტი"))


c = my_functions.material_price_search_in_table('ცემენტი')['Price']
print(c)


