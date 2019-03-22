#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy,os

import SQL_sub_domain_samushao, my_functions

cwd = os.getcwd()
workspace = os.path.join(cwd, "საპროექტო_ფორმა_14\New File Geodatabase.gdb\Data")
arcpy.env.workspace = workspace
# arcpy.env.overwriteOutput = True

print(workspace)

# STEP 1: გლობალური ცვლადების გამოცხადება
obieqti = 'obieqti'
xazi = 'Xazi'

# პარამეტრების გამოცხადება
CRM_ID = arcpy.GetParameterAsText(0)
# CRM_ID = '777'

# Create Feature Layers
arcpy.MakeFeatureLayer_management(obieqti,'obieqti_layer', """ "CRM_ID" = {} OR "CRM_ID" is Null """.format(CRM_ID))
arcpy.MakeFeatureLayer_management(xazi,'xazi_layer', """ "CRM_ID" = {} OR "CRM_ID" is Null """.format(CRM_ID))


# კურსორისთვის საჭირო ველების ჩამონათვალი
fields = ['SubType', 'Type','CRM_ID', 'SHAPE@LENGTH' ]


#ფუნქცია დააბრუნებს უნიკალურ ['სუბ+დომეინი', 'სუბ+დომეინი'] ლისტს. მაგ. ['11', '13']
unique_obieqti_domains = my_functions.unique('obieqti_layer',fields)
unique_xazi_domains = my_functions.unique('xazi_layer', fields)
print(unique_obieqti_domains)
print(unique_xazi_domains)

#საპროექტო ობიექტი_შეჯამება
obieqti_counted_by_domain_types = my_functions.count_to_dict(unique_obieqti_domains,'obieqti_layer', fields)

#საპროექტო ხაზი_შეჯამება
xazi_counted_by_domain_types = my_functions.length_to_dict(unique_xazi_domains,'xazi_layer', fields)

print("obieqti_counted_by_domain_types:")
print(obieqti_counted_by_domain_types)

print("xazi_counted_by_domain_types:")
print(xazi_counted_by_domain_types)
print("\n")




# დომეინ კოდებს მიანიჭებს შესაბამის სახელწოდებებს და გახდის წაკითხვადს
# {'შესასრულებელი სამუშაო': 'რაოდენობა'}

# ეს იქნება გისიდან საბოლოო ინფორმაციის ამოღება
gis_obieqti = {}
for key, value in obieqti_counted_by_domain_types.items():
    job_name = SQL_sub_domain_samushao.subtype_obieqti[key]
    count = value
    gis_obieqti[job_name] = count
print("gis_obieqti with name: ")
print(gis_obieqti)
print("\n")


gis_xazi = {}
for key, value in xazi_counted_by_domain_types.items():
    job_name = SQL_sub_domain_samushao.subtype_xazi[key]
    count = value
    gis_xazi[job_name] = count
print("gis_xazi with name: ")
print(gis_xazi)
print("\n")


#ოთხივე ბაზაში დახაზული ელემენტების გაერთიანებული დიქშენერი, რომელიც გადაეცემა საბოლოო სკრიპტს
gis_results = {}
gis_results = gis_obieqti.copy()
gis_results.update(gis_xazi)
print("GIS_RESULTS:", gis_results)
print("This is the End of Gis side script \n")

