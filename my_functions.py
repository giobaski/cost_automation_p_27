#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy

# ფუნქცია, რომელიც მასალების ფასებს აბრუნებს CRM_ცხრილიდან:
def material_price_search_in_table(material_name):
    #კურსორისთვის საჭირო ველების ჩამონათვალი
    fields = ['Category', 'Name', 'Price', 'Nomenclature']
    table = r'D:\Arcpy_pro_scripting\silk_projects\cost automation\საპროექტო_ფორმა_14\New File Geodatabase.gdb\material'
    with arcpy.da.SearchCursor(table, fields) as material_cursor:
        for row in material_cursor:
            if row[1] == material_name:
                material={}
                material['Name']= row[1]
                material['Price']= row[2]
                material['Nomenclatura']= row[3]
                return material




# ფუნქცია აბრუნებს საპროექტო ლეიერში დახაზული ელემენტების "საბტაიპი/დომეინების" უნიკალურ სიას. მაგ. ['11', '13']
def unique(featureLayer, fields):
    list = []
    with arcpy.da.SearchCursor(featureLayer, fields) as cursor:
        for row in cursor:
            a = row[0] #subtype_field
            b = row[1] #domain_field
            c = str(a) + str(b) # "12"
            if c not in list:
                list.append(c)
    return list
    del cursor



# უნიკალური ელემენტების რაოდენობა ###{'სუბ+დომეინი': რაოდენობა} მაგ. {'11': 3, '13': 1}
def count_to_dict(unique_domains_list, featureLayer,fields):
    elements = {}
    for i in unique_domains_list:
        count = 0
        with arcpy.da.SearchCursor(featureLayer, fields) as cursor:
            for row in cursor:
                a = row[0]
                b = row[1]
                c = str(a) + str(b)
                if c == i:
                    count += 1
                    elements[i] = count
        del cursor
    return elements


####
def length_to_dict(unique_domains_list, featureLayer, fields):
    elements = {}
    for i in unique_domains_list:
        length = 0
        with arcpy.da.SearchCursor(featureLayer, fields) as cursor:
            for row in cursor:
                a = row[0]
                b = row[1]
                c = str(a) + str(b)
                if c == i:
                    length += row[3]
                    elements[i] = round(length,2)
        del cursor
    return elements