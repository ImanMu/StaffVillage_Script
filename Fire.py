###############################-------------- JUNCTION --------------#####################################

import arcpy 
import os

GDB_6A = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Fire 6A and 6B.gdb"
GDB_6B = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Fire_6B.gdb"
###################################################### FITTINGS 
input_fc = "Fitting"
input6A_fc = os.path.join(GDB_6A, input_fc)
input6B_fc = os.path.join(GDB_6B, input_fc)

output_fc = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Corrected.gdb\Junction_Combined"
arcpy.management.Merge([input6A_fc, input6B_fc], output_fc)

###################################################### APPURTENANCE
input_fc1 = "Appurtenance"
input6A_fc1 = os.path.join(GDB_6A, input_fc1)
input6B_fc1 = os.path.join(GDB_6B, input_fc1)

output_fc1 = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Corrected.gdb\Appurtenance_Combined"
arcpy.management.Merge([input6A_fc1, input6B_fc1], output_fc1)



target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
targetFc_name = "usfnJunctionP"
targetFc = os.path.join(target_GDB, targetFc_name)
schema_type = "No_Test"

arcpy.env.workspace = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Corrected.gdb"
input_fc = "Junction_Combined"
input_fc1 = "Appurtenance_Combined"

input_lyr = "DismJoint_Layer"
  
arcpy.management.TruncateTable(targetFc)

################---------  selecting Dismantling JOINT
arcpy.management.MakeFeatureLayer(input_fc1, "DismJoint_Layer", "aec_Desc LIKE '%Dismantling joint%'")

# hn add field mappings objects --->
fms = arcpy.FieldMappings()
fms.addTable(targetFc)

##### Asser ID field
fm_assetID = arcpy.FieldMap()
fm_assetID.addInputField(input_fc, "AMAALA_Elements_Operations_AMA8")
assetID_field = fm_assetID.outputField
assetID_field.name = 'AssetID'
fm_assetID.outputField = assetID_field

##### Elevation field
fm_elev = arcpy.FieldMap()
fm_elev.addInputField(input_fc, "Elevation")
elev_field = fm_elev.outputField
elev_field.name = 'Elevation'
fm_elev.outputField = elev_field

##### Drawing Ref
fm_DrwID = arcpy.FieldMap()
fm_DrwID.addInputField(input_fc, "AMAALA_Elements_Operations_AM31")
DrwID_field = fm_DrwID.outputField
DrwID_field.name = 'Ref_Drawing_ID'
fm_DrwID.outputField = DrwID_field

##### Description field
fm_description = arcpy.FieldMap()
fm_description.addInputField(input_fc, "aec_Desc")
desc_field = fm_description.outputField
desc_field.name = 'Description'
fm_description.outputField = desc_field

##### Diameter 
fm_Diam = arcpy.FieldMap()
fm_Diam.addInputField(input_fc, "aec_NomDia")
Diam_field = fm_Diam.outputField
Diam_field.name = 'Remarks'
fm_Diam.outputField = Diam_field

fms.addFieldMap(fm_elev)
fms.addFieldMap(fm_assetID)
fms.addFieldMap(fm_description)
fms.addFieldMap(fm_Diam)

arcpy.management.Append(input_fc, targetFc, schema_type, fms)
arcpy.management.Append(input_lyr, targetFc, schema_type, fms)
############################------------FIELD CALCULATING------------##################################
########----Matching fields between all feature classes

fields=[
["AssetStatus", "8"],
["AssetCondition", "13"],
["StreetName", '"Tabuk, Alwajh"'],
["ProximityToNetwork", "5"],
["PipeType", "1"],
    
["dataSource", '"Amaala"'],
["G_Elevation_Source","3"],
    
["Manufacture", '"AVK SAUDI, CSA ITALY, AVK CHINA" if "Dismantling joint" in !Description! else "NAFFCO / SHIELD"'], 
["Material", '1 if "Dismantling joint" in !Description! else 8'],

["Diameter1",
        '''
        int(__import__("re").findall(r"\\d+", !Remarks!)[0])
        if !Remarks! and __import__("re").findall(r"\\d+", !Remarks!)
        else 160 if "Dismantling joint" in !Description! 
        else None
        '''.replace("\n", " ").strip()],

["Diameter2", '90 if "Reducer" in !Description! else !Diameter1! if "Tee" in !Description! else None'],
["Diameter3", '!Diameter1! if "Tee" in !Description! else None'],
    
    ["AssetType", '''
        2 if !Description!.split(" ")[0].strip() == "Bend"
        else 18 if "Elbow" in !Description!
        else 9 if "Tee" in !Description!
        else 34 if "Flange" in !Description!
        else 7 if "Reducer" in !Description!
        else 36 if "Segmented Bend" in !Description!
        else 35 if "Sweep Bend" in !Description!
        else 33 if "Dismantling joint" in !Description!
        else None
    '''.replace("\n", " ").strip()],
    
["LocationType", '3 if !AssetType! == "7" or !AssetType! == "34" or !AssetType! == "33" else 14'],
["NominalPressure", "16"],
    
# month/day/year Date convention
#Design
["DesignCompany", "39"],
["DesignGDate", "datetime.datetime.strptime('01/01/2021', '%m/%d/%Y')"],
["DesignHDate", '"17 Jumada al-Awwal 1442 AH"'],
# Construction 
["ConstructionCompany", "56"],
["ConstructionGDate", "datetime.datetime.strptime('04/01/2022', '%m/%d/%Y')"],
["ConstructionHDate", '"29 Shaaban 1443"'],
# Inservice  
["InServiceGDate", "datetime.datetime.strptime('12/01/2025', '%m/%d/%Y')"],
["InServiceHDate", '"10 Jumada II 1447"'],
["BIM360_Link",'"https://acc.autodesk.com/docs/files/projects/9b55ab58-f9b7-46ae-8007-eacfa358f9d2?folderUrn=urn%3Aadsk.wipprod%3Afs.folder%3Aco.IGKlmPvgQ3mZTADghgoYDg&viewModel=detail&moduleId=folders"'],
["ProjectID", '"1SV10110"'],
["Pressure", "None"],
]

arcpy.management.CalculateFields(targetFc, "Python", fields)

############################------------FIELD GEOMETRY CALCULATING------------##################################
#UTM37Ncoor = arcpy.Describe(input_fc).spatialReference

# Calculate Geomerty
geometryProperty = [
["Xcoordinate", "POINT_X"],
["Ycoordinate", "POINT_Y"],
]
arcpy.management.CalculateGeometryAttributes(targetFc, geometryProperty)


arcpy.management.Delete("DismJoint_Layer")

print("Done JUNCTION POINTS from FITTING && Appurtenance successfully")

###############################-------------- CHECK VALVE && ISO --------------#####################################
import arcpy 
import os

arcpy.env.workspace = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Corrected.gdb"
input_fc = "Appurtenance_Combined"

target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
checkV_targetFc_name = "usfnCheckValveP"
isolationV_targetFc_name = "usfnIsolationValveP"
checkV_targetFc = os.path.join(target_GDB, checkV_targetFc_name)
isolationV_targetFc = os.path.join(target_GDB, isolationV_targetFc_name)
schema_type = "No_Test"

#nms7 ay records feh el table we Truncate Table tool bt5ly el object_ID yrg3 ybd2 mn 1    
arcpy.management.TruncateTable(checkV_targetFc)
arcpy.management.TruncateTable(isolationV_targetFc)

arcpy.management.MakeFeatureLayer(input_fc, "CheckV_Layer", "aec_Desc LIKE '%Check Valve%'")
arcpy.management.MakeFeatureLayer(input_fc, "IsolationV_Layer", "aec_Desc LIKE '%Gate Valve%'")

############################------------FIELD MAPPINGS------------##################################
# hn add field mappings objects --->
fms = arcpy.FieldMappings()
fms.addTable(checkV_targetFc)

fms2 = arcpy.FieldMappings()
fms2.addTable(isolationV_targetFc)

##### Asser ID field
fm_assetID = arcpy.FieldMap()
fm_assetID.addInputField(input_fc, "AMAALA_Elements_Operations_AMA8")
assetID_field = fm_assetID.outputField
assetID_field.name = 'AssetID'
fm_assetID.outputField = assetID_field

##### Elevation field
fm_elev = arcpy.FieldMap()
fm_elev.addInputField(input_fc, "Elevation")
elev_field = fm_elev.outputField
elev_field.name = 'Elevation'
fm_elev.outputField = elev_field

##### Description field
fm_description = arcpy.FieldMap()
fm_description.addInputField(input_fc, "aec_Desc")
desc_field = fm_description.outputField
desc_field.name = 'Description'
fm_description.outputField = desc_field

##### Drawing Ref
fm_DrwID = arcpy.FieldMap()
fm_DrwID.addInputField(input_fc, "AMAALA_Elements_Operations_AM31")
DrwID_field = fm_DrwID.outputField
DrwID_field.name = 'Ref_Drawing_ID'
fm_DrwID.outputField = DrwID_field

fms.addFieldMap(fm_elev)
fms.addFieldMap(fm_assetID)
fms.addFieldMap(fm_description)
fms.addFieldMap(fm_DrwID)

fms2.addFieldMap(fm_elev)
fms2.addFieldMap(fm_assetID)
fms2.addFieldMap(fm_description)
fms2.addFieldMap(fm_DrwID)

arcpy.management.Append("CheckV_Layer", checkV_targetFc, schema_type, fms)
arcpy.management.Append("IsolationV_Layer", isolationV_targetFc, schema_type, fms2)

fields=[
["AssetStatus", "8"],
["AssetCondition", "13"],
["StreetName", '"Saudi Arabia"'],
["ProximityToNetwork", "5"],
["PipeType", "1"],
    
["dataSource", '"Amaala"'],
["G_Elevation_Source","3"],

["Diameter", '100 if "Check Valve" in !Description! else 160 if "Gate" in !Description! else None'],
["LocationType", "3"],
["AssetType", '3 if "Check Valve" in !Description! else 6'],
["NominalPressure", "16"],

["Manufacture", '"AVK SAUDI, CSA ITALY, AVK CHINA"'], 
["Material", "4"],
    
# month/day/year Date convention
#Design
["DesignCompany", "39"],
["DesignGDate", "datetime.datetime.strptime('01/01/2021', '%m/%d/%Y')"],
["DesignHDate", '"17 Jumada al-Awwal 1442 AH"'],
# Construction 
["ConstructionCompany", "56"],
["ConstructionGDate", "datetime.datetime.strptime('04/01/2022', '%m/%d/%Y')"],
["ConstructionHDate", '"29 Shaaban 1443"'],
# Inservice  
["InServiceGDate", "datetime.datetime.strptime('12/01/2025', '%m/%d/%Y')"],
["InServiceHDate", '"10 Jumada II 1447"'],
["BIM360_Link",'"https://acc.autodesk.com/docs/files/projects/9b55ab58-f9b7-46ae-8007-eacfa358f9d2?folderUrn=urn%3Aadsk.wipprod%3Afs.folder%3Aco.IGKlmPvgQ3mZTADghgoYDg&viewModel=detail&moduleId=folders"'],

#Calculating Fixed values fields instead of mapping them
["ProjectID", '"1SV10110"'],
]


arcpy.management.CalculateFields(checkV_targetFc, "Python", fields)
arcpy.management.CalculateFields(isolationV_targetFc, "Python", fields)

############################------------FIELD GEOMETRY CALCULATING------------##################################
# Calculate Geomerty
geometryProperty = [
["Xcoordinate", "POINT_X"],
["Ycoordinate", "POINT_Y"],
]

arcpy.management.CalculateGeometryAttributes(checkV_targetFc, geometryProperty)
arcpy.management.CalculateGeometryAttributes(isolationV_targetFc, geometryProperty)

arcpy.management.Delete("CheckV_Layer")
arcpy.management.Delete("IsolationV_Layer")

print("Done CheckV and IsolationV POINTS from Appurtenance successfully")

###############################-------------- CHAMBER POLYGON --------------#####################################
import arcpy 
import os

GDB_6A = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Fire 6A and 6B.gdb"
GDB_6B = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Fire_6B.gdb"
###################################################### GRAVITY  
input_fc = "GravityNetwork"
input6A_fc = os.path.join(GDB_6A, input_fc)
input6B_fc = os.path.join(GDB_6B, input_fc)

output_fc = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Corrected.gdb\GravityNetwork_Combined"
arcpy.management.Merge([input6A_fc, input6B_fc], output_fc)

###################################################### STRUCTURE  
input_fc1 = "Structure"
input6A_fc1 = os.path.join(GDB_6A, input_fc1)
input6B_fc1 = os.path.join(GDB_6B, input_fc1)

output_fc1 = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Corrected.gdb\Structure_Combined"
arcpy.management.Merge([input6A_fc1, input6B_fc1], output_fc1)


target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
targetFc_name = "usfnChamberPolygonS"
targetFc = os.path.join(target_GDB, targetFc_name)
schema_type = "No_Test"

arcpy.env.workspace = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Corrected.gdb"
input_fc = "GravityNetwork_Combined"
input_fc1 = "Structure_Combined"
poly_fc = "ZValueFc"
schema_type = "No_Test"

#nms7 ay records feh el table we Truncate Table tool bt5ly el object_ID yrg3 ybd2 mn 1    
arcpy.management.TruncateTable(targetFc)
arcpy.ddd.MultiPatchFootprint(input_fc, "ChamberPoly")
arcpy.management.JoinField("ChamberPoly", "Handle", input_fc1, "Handle")
arcpy.ddd.FeatureTo3DByAttribute("ChamberPoly", "ZValueFc", "Elevation")

arcpy.management.AddField(poly_fc, "calc_Depth", "Double")
fields=[
["calc_Depth", "!Z_Max! - !Z_Min!"],
]
arcpy.management.CalculateFields(poly_fc, "Python", fields)

############################------------FIELD MAPPINGS------------##################################
# hn add field mappings objects --->
fms = arcpy.FieldMappings()
fms.addTable(targetFc)

##### Asser ID field
fm_assetID = arcpy.FieldMap()
fm_assetID.addInputField(poly_fc, "AMAALA_Elements_Operations_AMA8")
assetID_field = fm_assetID.outputField
assetID_field.name = 'AssetID'
fm_assetID.outputField = assetID_field

##### Elevation field
fm_elev = arcpy.FieldMap()
fm_elev.addInputField(poly_fc, "Elevation")
elev_field = fm_elev.outputField
elev_field.name = 'Elevation'
fm_elev.outputField = elev_field

##### Description field
fm_description = arcpy.FieldMap()
fm_description.addInputField(poly_fc, "aec_Desc")
desc_field = fm_description.outputField
desc_field.name = 'Description'
fm_description.outputField = desc_field

##### depth field
fm_depth = arcpy.FieldMap()
fm_depth.addInputField(poly_fc, "calc_Depth")
depth_field = fm_depth.outputField
depth_field.name = 'Depth'
fm_depth.outputField = depth_field

##### Drawing Ref
fm_DrwID = arcpy.FieldMap()
fm_DrwID.addInputField(poly_fc, "AMAALA_Elements_Operations_AM31")
DrwID_field = fm_DrwID.outputField
DrwID_field.name = 'Ref_Drawing_ID'
fm_DrwID.outputField = DrwID_field

fms.addFieldMap(fm_elev)
fms.addFieldMap(fm_assetID)
fms.addFieldMap(fm_description)
fms.addFieldMap(fm_depth)
fms.addFieldMap(fm_DrwID)

arcpy.management.Append(poly_fc, targetFc, schema_type, fms)

############################------------FIELD CALCULATING------------##################################
fields=[
["LocationType", "3"],
["StreetName", '"Saudi Arabia"'],
["AssetStatus", "8"],   
["AssetCondition", "13"],
["ProximityToNetwork", "5"],
["AssetType", "3"],
["ChamberShape", "2"],
    
["dataSource", '"Amaala"'],
["G_Elevation_Source","3"],

["Length", "2000"],
["Width", "1500"],
["Diameter", "160"],    
# month/day/year Date convention
#Design
["DesignCompany", "39"],
["DesignGDate", "datetime.datetime.strptime('01/01/2021', '%m/%d/%Y')"],
["DesignHDate", '"17 Jumada al-Awwal 1442 AH"'],
# Construction 
["ConstructionCompany", "56"],
["ConstructionGDate", "datetime.datetime.strptime('04/01/2022', '%m/%d/%Y')"],
["ConstructionHDate", '"29 Shaaban 1443"'],
# Inservice  
["InServiceGDate", "datetime.datetime.strptime('12/01/2025', '%m/%d/%Y')"],
["InServiceHDate", '"10 Jumada II 1447"'],
["BIM360_Link",'"https://acc.autodesk.com/docs/files/projects/9b55ab58-f9b7-46ae-8007-eacfa358f9d2?folderUrn=urn%3Aadsk.wipprod%3Afs.folder%3Aco.IGKlmPvgQ3mZTADghgoYDg&viewModel=detail&moduleId=folders"'],

#Calculating Fixed values fields instead of mapping them
["ProjectID", '"1SV10110"'],
]

arcpy.management.CalculateFields(targetFc, "Python", fields)

############################------------FIELD GEOMETRY CALCULATING------------##################################
# Calculate Geomerty
geometryProperty = [
    ["Xcoordinate", "CENTROID_X"],
    ["Ycoordinate", "CENTROID_Y"],
]
arcpy.management.CalculateGeometryAttributes(targetFc, geometryProperty)

arcpy.management.Delete("ZValueFc")
arcpy.management.Delete("ChamberPoly")

print("Done CHAMBER POLYGON from GRAVITY NETWORK successfully")

###############################-------------- CHAMBER POINT --------------#####################################

import arcpy 
import os

arcpy.env.workspace = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Fire 6A and 6B.gdb"
target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\AMAALA GIS Schema_08July2026\TRSDC DB.gdb"
targetFc_name = "usfnChamberP"
targetFc = os.path.join(target_GDB, targetFc_name)
input_fc = "Structure"
schema_type = "No_Test"

#nms7 ay records feh el table we Truncate Table tool bt5ly el object_ID yrg3 ybd2 mn 1    
arcpy.management.TruncateTable(targetFc)

############################------------FIELD MAPPINGS------------##################################
# hn add field mappings objects --->
fms = arcpy.FieldMappings()
fms.addTable(targetFc)

##### Asser ID field
fm_assetID = arcpy.FieldMap()
fm_assetID.addInputField(input_fc, "AMAALA_Elements_Operations_AMA8")
assetID_field = fm_assetID.outputField
assetID_field.name = 'AssetID'
fm_assetID.outputField = assetID_field

##### Elevation field
fm_elev = arcpy.FieldMap()
fm_elev.addInputField(input_fc, "Elevation")
elev_field = fm_elev.outputField
elev_field.name = 'Elevation'
fm_elev.outputField = elev_field

##### chamberName field
fm_chName = arcpy.FieldMap()
fm_chName.addInputField(input_fc, "aec_Name")
elev_chName = fm_chName.outputField
elev_chName.name = 'ChamberName'
fm_chName.outputField = elev_chName

fms.addFieldMap(fm_elev)
fms.addFieldMap(fm_assetID)
fms.addFieldMap(fm_chName)

arcpy.management.Append(input_fc, targetFc, schema_type, fms)

############################------------FIELD CALCULATING------------##################################
fields=[
["LocationType", "3"],
["StreetName", '"Saudi Arabia"'],
["AssetStatus", "8"],   
["AssetCondition", "13"],
["ProximityToNetwork", "5"],
["AssetType", "3"],
["ChamberShape", "2"],
["dataSource", '"CAD"'],
["Length", "2500"],
["Width", "2000"],
    
# month/day/year Date convention
#Design
["DesignCompany", "39"],
["DesignGDate", "datetime.datetime.strptime('8/20/2026', '%m/%d/%Y')"],
["DesignHDate", '"Rabi I 7, 1448 AH"'],
# Construction 
["ConstructionCompany", "56"],
["ConstructionGDate", "datetime.datetime.strptime('8/20/2026', '%m/%d/%Y')"],
["ConstructionHDate", '"Rabi I 7, 1448 AH"'],
# Inservice  
["InServiceGDate", "datetime.datetime.strptime('12/01/2025', '%m/%d/%Y')"],
["InServiceHDate", '"Jumada II 10, 1447 AH"'],

#Calculating Fixed values fields instead of mapping them
["Ref_Drawing_ID",'"1SV10110-110C08-BEC-62-XX-MOD-UW-10201"'],
["ProjectID", '"1SV10110"'],
]

arcpy.management.CalculateFields(targetFc, "Python", fields)

############################------------FIELD GEOMETRY CALCULATING------------##################################
# Calculate Geomerty
geometryProperty = [
    ["Xcoordinate", "POINT_X"],
    ["Ycoordinate", "POINT_Y"],
]
arcpy.management.CalculateGeometryAttributes(targetFc, geometryProperty)

arcpy.management.MakeFeatureLayer(targetFc, "lyr")
arcpy.management.AddJoin("lyr", "AssetID", "ZValueFc", "AMAALA_Elements_Operations_AMA8")

fields=[
["Depth", "!calc_Depth!"],
]
arcpy.management.CalculateFields("lyr", "Python", fields)
arcpy.management.RemoveJoin("lyr")
arcpy.management.Delete("lyr")

print("Done CHAMBER POINT from Structure successfully")


###############################-------------- PIPES LINES --------------#####################################
import arcpy 
import os

arcpy.env.workspace = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Fire 6A and 6B.gdb"
target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\AMAALA GIS Schema_08July2026\TRSDC DB.gdb"
targetFc_name = "usfnLateralLinesL"
targetFc = os.path.join(target_GDB, targetFc_name)
input_fc = "PressurePipe"
schema_type = "No_Test"

#nms7 ay records feh el table we Truncate Table tool bt5ly el object_ID yrg3 ybd2 mn 1    
arcpy.management.TruncateTable(targetFc)

############################------------FIELD MAPPINGS------------##################################
# hn add field mappings objects --->
fms = arcpy.FieldMappings()
fms.addTable(targetFc)

##### Asser ID field
fm_assetID = arcpy.FieldMap()
fm_assetID.addInputField(input_fc, "AMAALA_Elements_Operations_AMA8")
assetID_field = fm_assetID.outputField
assetID_field.name = 'AssetID'
fm_assetID.outputField = assetID_field

##### Elevation field
fm_elev = arcpy.FieldMap()
fm_elev.addInputField(input_fc, "Elevation")
elev_field = fm_elev.outputField
elev_field.name = 'Elevation'
fm_elev.outputField = elev_field

##### Diameter field
fm_diam = arcpy.FieldMap()
fm_diam.addInputField(input_fc, "aec_NomDia")
diam_field = fm_diam.outputField
diam_field.name = 'Diameter'
fm_diam.outputField = diam_field

##### Pipe's Start Centerline elevation
fm_strtElev = arcpy.FieldMap()
fm_strtElev.addInputField(input_fc, "aec_StrtCtlnElev")
strtElev_field = fm_strtElev.outputField
strtElev_field.name = 'StartPipeElevation'
fm_strtElev.outputField = strtElev_field

##### Pipe's End Centerline elevation
fm_endElev = arcpy.FieldMap()
fm_endElev.addInputField(input_fc, "aec_EndCtlnElev")
endElev_field = fm_endElev.outputField
endElev_field.name = 'EndPipeElevation'
fm_endElev.outputField = endElev_field

##### Pipe's End Centerline elevation
fm_desc = arcpy.FieldMap()
fm_desc.addInputField(input_fc, "aec_Desc", 0, 17)
desc_field = fm_desc.outputField
desc_field.name = 'Description'
fm_desc.outputField = desc_field

fms.addFieldMap(fm_elev)
fms.addFieldMap(fm_assetID)
fms.addFieldMap(fm_diam)
fms.addFieldMap(fm_strtElev)
fms.addFieldMap(fm_endElev)
fms.addFieldMap(fm_desc)

arcpy.management.Append(input_fc, targetFc, schema_type, fms)

############################------------FIELD CALCULATING------------##################################
fields=[
["AssetStatus", "8"],   
["AssetCondition", "13"],
["AssetType", "8"],
["Material", '"HDPE"'],
["Manufacture", '"NAFFCO / SHIELD"'],
["dataSrouce", '"CAD"'],
    
["Description", "'Simulated pipe' if !AssetID! is None else !Description!"],
# month/day/year Date convention
#Design
["DesignCompany", "39"],
["DesignGDate", "datetime.datetime.strptime('8/20/2026', '%m/%d/%Y')"],
["DesignHDate", '"Rabi I 7, 1448 AH"'],
# Construction 
["ConstructionCompany", "56"],
["ConstructionGDate", "datetime.datetime.strptime('8/20/2026', '%m/%d/%Y')"],
["ConstructionHDate", '"Rabi I 7, 1448 AH"'],
# Inservice  
["InServiceGDate", "datetime.datetime.strptime('12/01/2025', '%m/%d/%Y')"],
["InServiceHDate", '"Jumada II 10, 1447 AH"'],

#Calculating Fixed values fields instead of mapping them
["Ref_Drawing_ID",'"1SV10110-110C08-BEC-62-XX-MOD-UW-10201"'],
["ProjectID", '"1SV10110"'],
["ProximityToNetwork", "5"],
["StreetName", '"Saudi Arabia"'],
]

arcpy.management.CalculateFields(targetFc, "Python", fields)

############################------------FIELD GEOMERTY CALCULATING------------##################################
geometryProperty = [
["StartXcoordinate", "LINE_START_X"],
["StartYcoordinate", "LINE_START_Y"],
["EndXcoordinate", "LINE_END_X"],
["EndYcoordinate", "LINE_END_Y"]
]

arcpy.management.CalculateGeometryAttributes(targetFc, geometryProperty)

print("Done WaterLateral Lines Successfully")

#############################-------------- FIRE SIEMES --------------###################################
import arcpy 
import os

arcpy.env.workspace = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Fire 6A and 6B\Fire 6A and 6B.gdb"
target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\AMAALA GIS Schema_08July2026\TRSDC DB.gdb"
targetFc_name = "usfnFireHoseConnectionP"
targetFc = os.path.join(target_GDB, targetFc_name)
input_fc = "Appurtenance"
schema_type = "No_Test"

#nms7 ay records feh el table we Truncate Table tool bt5ly el object_ID yrg3 ybd2 mn 1    
arcpy.management.TruncateTable(targetFc)
arcpy.management.MakeFeatureLayer(input_fc, "FIRE_SIEMES", "aec_Desc LIKE '%FIRE SIEMES%'")

############################------------FIELD MAPPINGS------------##################################
# hn add field mappings objects --->
fms = arcpy.FieldMappings()
fms.addTable(targetFc)

##### Asser ID field
fm_assetID = arcpy.FieldMap()
fm_assetID.addInputField(input_fc, "AMAALA_Elements_Operations_AMA8")
assetID_field = fm_assetID.outputField
assetID_field.name = 'AssetID'
fm_assetID.outputField = assetID_field

##### Elevation field
fm_elev = arcpy.FieldMap()
fm_elev.addInputField(input_fc, "Elevation")
elev_field = fm_elev.outputField
elev_field.name = 'Elevation'
fm_elev.outputField = elev_field

##### Description field
fm_description = arcpy.FieldMap()
fm_description.addInputField(input_fc, "aec_Desc")
desc_field = fm_description.outputField
desc_field.name = 'Description'
fm_description.outputField = desc_field

fms.addFieldMap(fm_elev)
fms.addFieldMap(fm_assetID)
fms.addFieldMap(fm_description)

arcpy.management.Append("FIRE_SIEMES", targetFc, schema_type, fms)

############################------------FIELD CALCULATING------------##################################
fields=[
["AssetStatus", "8"],   
["AssetCondition", "13"],
["AssetType", "3"],
["PipeType", "7"],
["Material", "3"],
["Manufacture", '"NAFFCO / SHIELD"'],
["dataSource", '"CAD"'],
["Height", "1.35"],

# month/day/year Date convention
#Design
["DesignCompany", "39"],
["DesignGDate", "datetime.datetime.strptime('8/20/2026', '%m/%d/%Y')"],
["DesignHDate", '"Rabi I 7, 1448 AH"'],
# Construction 
["ConstructionCompany", "56"],
["ConstructionGDate", "datetime.datetime.strptime('8/20/2026', '%m/%d/%Y')"],
["ConstructionHDate", '"Rabi I 7, 1448 AH"'],
# Inservice  
["InServiceGDate", "datetime.datetime.strptime('12/01/2025', '%m/%d/%Y')"],
["InServiceHDate", '"Jumada II 10, 1447 AH"'],

#Calculating Fixed values fields instead of mapping them
["Ref_Drawing_ID",'"1SV10110-110C08-BEC-62-XX-MOD-UW-10201"'],
["ProjectID", '"1SV10110"'],
["ProximityToNetwork", "5"],
["StreetName", '"Saudi Arabia"'],
]

arcpy.management.CalculateFields(targetFc, "Python", fields)

############################------------FIELD GEOMETRY CALCULATING------------##################################
# Calculate Geomerty
geometryProperty = [
    ["Xcoordinate", "POINT_X"],
    ["Ycoordinate", "POINT_Y"],
]
arcpy.management.CalculateGeometryAttributes(targetFc, geometryProperty)

arcpy.management.Delete("FIRE_SIEMES")
print("Done FIRE_SIEMES from Structure successfully")



