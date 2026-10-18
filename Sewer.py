###############################-------------- PIPES LINES --------------#####################################
import arcpy 
import os  

GDB_6A = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Sewer 6A and 6B.gdb"
GDB_6B = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Sewer_6B.gdb"
input_fc = "Pipe"
input6A_fc = os.path.join(GDB_6A, input_fc)
input6B_fc = os.path.join(GDB_6B, input_fc)

output_fc = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Corrected.gdb\Pipes_Combined"

arcpy.management.Merge([input6A_fc, input6B_fc], output_fc)

target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
targetFc_name = "uswwLateralLineL"
targetFc = os.path.join(target_GDB, targetFc_name)
schema_type = "No_Test"

arcpy.env.workspace = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Corrected.gdb"
input_fc = "Pipes_Combined"

#nms7 ay records feh el table we Truncate Table tool bt5ly el object_ID yrg3 ybd2 mn 1    
arcpy.management.TruncateTable(targetFc)

######## ADDING FIXED IDs
arcpy.management.AddField(targetFc, "FIXED_ID", "LONG")

############################------------FIELD MAPPINGS------------##################################
# hn add field mappings objects --->
fms = arcpy.FieldMappings()
fms.addTable(targetFc)

##### Asser ID field
fm_assetID = arcpy.FieldMap()
fm_assetID.addInputField(input_fc, "AMAALA_Elements_Operations_AMA8")
assetID_field = fm_assetID.outputField
assetID_field.name = 'Description'
fm_assetID.outputField = assetID_field

##### Elevation field
fm_elev = arcpy.FieldMap()
fm_elev.addInputField(input_fc, "Elevation")
elev_field = fm_elev.outputField
elev_field.name = 'Elevation'
fm_elev.outputField = elev_field

##### Pipe's Start Centerline elevation
fm_strtElev = arcpy.FieldMap()
fm_strtElev.addInputField(input_fc, "aec_StrtCrwnElev")
strtElev_field = fm_strtElev.outputField
strtElev_field.name = 'StartPipeElevation'
fm_strtElev.outputField = strtElev_field

##### Pipe's End Centerline elevation
fm_endElev = arcpy.FieldMap()
fm_endElev.addInputField(input_fc, "aec_EndCrwnElev")
endElev_field = fm_endElev.outputField
endElev_field.name = 'EndPipeElevation'
fm_endElev.outputField = endElev_field

##### Description
fm_desc = arcpy.FieldMap()
fm_desc.addInputField(input_fc, "aec_Desc")
desc_field = fm_desc.outputField
desc_field.name = 'Description'
fm_desc.outputField = desc_field

##### Drawing Ref
fm_DrwID = arcpy.FieldMap()
fm_DrwID.addInputField(input_fc, "AMAALA_Elements_Operations_AM31")
DrwID_field = fm_DrwID.outputField
DrwID_field.name = 'Ref_Drawing_ID'
fm_DrwID.outputField = DrwID_field

##### Diameter 
fm_Diam = arcpy.FieldMap()
fm_Diam.addInputField(input_fc, "aec_InnDia")
Diam_field = fm_Diam.outputField
Diam_field.name = 'Diameter'
fm_Diam.outputField = Diam_field

##### Fixed_ID 
fm_FID = arcpy.FieldMap()
fm_FID.addInputField(input_fc, "OBJECTID")
FID_field = fm_FID.outputField
FID_field.name = 'FIXED_ID'
fm_FID.outputField = FID_field

fms.addFieldMap(fm_elev)
fms.addFieldMap(fm_assetID)
fms.addFieldMap(fm_strtElev)
fms.addFieldMap(fm_endElev)
fms.addFieldMap(fm_desc)
fms.addFieldMap(fm_DrwID)
fms.addFieldMap(fm_Diam)
fms.addFieldMap(fm_FID)

arcpy.management.Append(input_fc, targetFc, schema_type, fms)

############################------------FIELD CALCULATING------------##################################
fields=[
["AssetStatus", "8"],   
["AssetCondition", "13"],
["AssetType", "4"],
["Material", "1"],
["dataSource", '"Amaala"'],
["G_Elevation_Source","3"],
   
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
["ProximityToNetwork", "3"],
["StreetName", '"Tabuk, Alwajh"'],
]

arcpy.management.CalculateFields(targetFc, "Python", fields)

############################------------FIELD GEOMERTY CALCULATING------------##################################
geometryProperty = [
["StartXCoordinate", "LINE_START_X"],
["StartYCoordinate", "LINE_START_Y"],
["EndXCoordinate", "LINE_END_X"],
["EndYCoordinate", "LINE_END_Y"]
]

arcpy.management.CalculateGeometryAttributes(targetFc, geometryProperty)

print("Done appending Sewer Pipe Lines Successfully")

###############################-------------- Manhole Multipatch --------------#####################################
import arcpy 
import os

GDB_6A = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Sewer 6A and 6B.gdb"
GDB_6B = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Sewer_6B.gdb"
input_fc = "MultiPatch"
input6A_fc = os.path.join(GDB_6A, input_fc)
input6B_fc = os.path.join(GDB_6B, input_fc)
output_fc = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Corrected.gdb\MultiPatch_Combined"
arcpy.management.Merge([input6A_fc, input6B_fc], output_fc)

target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
targetFc_name = "uswwEquipmentS"
targetFc = os.path.join(target_GDB, targetFc_name)
schema_type = "No_Test"
MH_lyr = "MH_lyr"

arcpy.env.workspace = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Corrected.gdb"
input_fc = "MultiPatch_Combined"

#nms7 ay records feh el table we Truncate Table tool bt5ly el object_ID yrg3 ybd2 mn 1    
arcpy.management.TruncateTable(targetFc)

##################################---------  selecting only manholes #########################################
arcpy.management.MakeFeatureLayer(input_fc, "MH_lyr", "AMAALA_Elements_Description_AMA LIKE '%Structures%'")

##################################------------FIELD MAPPINGS------------########################################
# hn add field mappings objects --->
fms = arcpy.FieldMappings()
fms.addTable(targetFc)

fm_assetID = arcpy.FieldMap()
fm_assetID.addInputField(MH_lyr, "AMAALA_Elements_Operations_AMA8")
assetID_field = fm_assetID.outputField
assetID_field.name = 'AssetID'
fm_assetID.outputField = assetID_field

fm_desc = arcpy.FieldMap()
fm_desc.addInputField(MH_lyr, "AMAALA_Elements_Operations_AM30")
desc_field = fm_desc.outputField
desc_field.name = 'Description'
fm_desc.outputField = desc_field

##### Drawing Ref
fm_DrwID = arcpy.FieldMap()
fm_DrwID.addInputField(MH_lyr, "AMAALA_Elements_Operations_AM31")
DrwID_field = fm_DrwID.outputField
DrwID_field.name = 'Ref_Drawing_ID'
fm_DrwID.outputField = DrwID_field

fms.addFieldMap(fm_assetID)
fms.addFieldMap(fm_desc)
fms.addFieldMap(fm_height)
fms.addFieldMap(fm_DrwID)

arcpy.management.Append(MH_lyr, targetFc, schema_type, fms)

############################------------Calculating Max z && Min z && Height for Manhole Feature Class------------##################################
############################------------FIELD GEOMETRY CALCULATING------------##################################
arcpy.management.AddField(targetFc, "Max_Z", "Double")
arcpy.management.AddField(targetFc, "Min_Z", "Double")

geometryProperty = [
    ["Max_Z", "EXTENT_MAX_Z"],
    ["Min_Z", "EXTENT_MIN_Z"],
    ["Xcoordinate", "EXTENT_MAX_X"],
    ["Ycoordinate", "EXTENT_MAX_Y"],
]
arcpy.management.CalculateGeometryAttributes(targetFc, geometryProperty)

############################------------FIELD CALCULATING------------########################################### 
fields=[
["StreetName", '"Tabuk, Alwajh"'],
["AssetStatus", "8"],   
["AssetCondition", "13"],
["dataSource", '"Amaala"'],
["G_Elevation_Source","3"],

["Elevation", "!Min_Z! - !Max_Z!"],
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
["ManufactureName",'"National Marketing Est. Co. Ltd."'],
["OtherDetails",'"Reinforced Concrete"'],
]

arcpy.management.CalculateFields(targetFc, "Python", fields)
arcpy.management.Delete(MH_lyr)
print("Done MANHOLES Multipatch successfully")

###############################-------------- MANHOLE POINT --------------#####################################

import arcpy 
import os

GDB_6A = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Sewer 6A and 6B.gdb"
GDB_6B = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Sewer_6B.gdb"
input_fc = "Structure"
input6A_fc = os.path.join(GDB_6A, input_fc)
input6B_fc = os.path.join(GDB_6B, input_fc)
output_fc = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Corrected.gdb\Structure_Combined"
arcpy.management.Merge([input6A_fc, input6B_fc], output_fc)

target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
targetFc_name = "uswwManholeP"
targetFc = os.path.join(target_GDB, targetFc_name)
schema_type = "No_Test"

joinFc_name = "uswwEquipmentS"
joinFc = os.path.join(target_GDB, joinFc_name)

arcpy.env.workspace = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Corrected.gdb"
input_fc = "Structure_Combined"

#nms7 ay records feh el table we Truncate Table tool bt5ly el object_ID yrg3 ybd2 mn 1    
arcpy.management.TruncateTable(targetFc)

############################------------FIELD MAPPINGS------------##################################
# hn add field mappings objects --->
fms = arcpy.FieldMappings()
fms.addTable(targetFc)

##### Asser ID field ----> didnt work bc Asset ID is long not Text will put it in remarks 
fm_assetID = arcpy.FieldMap()
fm_assetID.addInputField(input_fc, "AMAALA_Elements_Operations_AMA8")
assetID_field = fm_assetID.outputField
assetID_field.name = 'Remarks'
fm_assetID.outputField = assetID_field

##### Elevation field
fm_elev = arcpy.FieldMap()
fm_elev.addInputField(input_fc, "Elevation")
elev_field = fm_elev.outputField
elev_field.name = 'G_Elevation'
fm_elev.outputField = elev_field

##### Elevation field
fm_elev2 = arcpy.FieldMap()
fm_elev2.addInputField(input_fc, "Elevation")
elev_field2 = fm_elev2.outputField
elev_field2.name = 'CoverLevel'
fm_elev2.outputField = elev_field2

##### Description field
fm_desc = arcpy.FieldMap()
fm_desc.addInputField(input_fc, "aec_Desc")
desc_field = fm_desc.outputField
desc_field.name = 'Description'
fm_desc.outputField = desc_field

##### Drawing Ref
fm_DrwID = arcpy.FieldMap()
fm_DrwID.addInputField(input_fc, "AMAALA_Elements_Operations_AM31")
DrwID_field = fm_DrwID.outputField
DrwID_field.name = 'Ref_Drawing_ID'
fm_DrwID.outputField = DrwID_field

fms.addFieldMap(fm_elev)
fms.addFieldMap(fm_elev2)
fms.addFieldMap(fm_assetID)
fms.addFieldMap(fm_desc)
fms.addFieldMap(fm_DrwID)

arcpy.management.Append(input_fc, targetFc, schema_type, fms)

##################################------------JOIN------------########################################
arcpy.management.MakeFeatureLayer(targetFc, "target_lyr")
target_lyr = "target_lyr"
arcpy.management.AddJoin(target_lyr, "Remarks", joinFc , "AssetID")
############################------------FIELD CALCULATING------------##################################
fields=[
["StreetName", '"Tabuk, Alwajh"'],
["AssetStatus", "8"],   
["AssetCondition", "13"],
["ProximityToNetwork", "3"],
["AssetType", "6"],
["dataSource", '"Amaala"'],
["ManholeShape", '1 if "BEC MH" in !uswwEquipmentS.Description! else 3'],
["InvertElevation","!uswwEquipmentS.Min_Z!"],
["Elevation","!uswwEquipmentS.Min_Z! - !uswwEquipmentS.Max_Z!"],
["Depth","!uswwEquipmentS.Max_Z! - !uswwEquipmentS.Min_Z!"],
["G_Elevation_Source","3"],
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
]

arcpy.management.CalculateFields(target_lyr, "Python", fields)
arcpy.management.RemoveJoin(target_lyr)
############################------------FIELD GEOMETRY CALCULATING------------##################################
# Calculate Geomerty
geometryProperty = [
    ["Xcoordinate", "POINT_X"],
    ["Ycoordinate", "POINT_Y"],
]
arcpy.management.CalculateGeometryAttributes(targetFc, geometryProperty)
arcpy.management.Delete(target_lyr)
arcpy.management.DeleteField(joinFc, ["Max_Z", "Min_Z"])
print("Done MANHOLES POINT from Structure successfully")

import arcpy 
import os

# this code took forever so we are gonna run the tool manually then replacing the features with the new ones
##################################------------deleting the intersected Pipes with the multipatch------------########################################
target_GDB = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
targetFc_name = "uswwLateralLineL"
targetFc = os.path.join(target_GDB, targetFc_name)

multipatchFc_name = "uswwEquipmentS"
multipatchFc = os.path.join(target_GDB, multipatchFc_name)
 
arcpy.ddd.Intersect3DLineWithMultiPatch(targetFc, multipatchFc, "ALL", "IntersectPoints", "IntersectLines")
arcpy.management.MakeFeatureLayer("IntersectLines", "Intersect_lyr")

arcpy.management.DeleteField("Intersect_lyr", ["LINE_OID", "FROM_MP_ID", "TO_MP_ID", "DIST_3D", "LENGTH_3D"])

arcpy.management.SelectLayerByLocation("Intersect_lyr", "COMPLETELY_WITHIN", multipatchFc, "", "NEW_SELECTION")
arcpy.management.DeleteRows("Intersect_lyr")

arcpy.management.TruncateTable(targetFc)
arcpy.management.Append("Intersect_lyr", targetFc, "TEST")
arcpy.management.Delete("Intersect_lyr")
print("Done removing the intersected pipes with Manholes successfully")

################################ extracting Pipes End-points #################################
import arcpy
import os

gdb = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Corrected.gdb"
target_gdb = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"

pipes = os.path.join(gdb, "Pipes_Combined")
manholes = os.path.join(gdb, "Structure_Combined")
endpoints = os.path.join(gdb, "Pipe_Endpoints")

arcpy.management.CreateFeatureclass(gdb, "Pipe_Endpoints", "POINT", spatial_reference=arcpy.Describe(pipes).spatialReference)
arcpy.management.AddField(endpoints, "PIPE_ID", "TEXT")
arcpy.management.AddField(endpoints, "END_TYPE", "TEXT")
arcpy.management.AddField(endpoints, "ELEVATION", "DOUBLE")

with arcpy.da.SearchCursor(
    pipes,
    ["OBJECTID", "SHAPE@", "aec_StrtCtlnElev", "aec_EndCtlnElev"]
) as pipe_cursor:

    with arcpy.da.InsertCursor(
        endpoints,
        ["SHAPE@", "PIPE_ID", "END_TYPE", "ELEVATION"]
    ) as endpoint_cursor:

        for pipe_id, geom, start_elev, end_elev in pipe_cursor:

            start_point = geom.firstPoint
            end_point = geom.lastPoint

            endpoint_cursor.insertRow([
                arcpy.PointGeometry(start_point, geom.spatialReference),
                pipe_id,
                "Outlet",
                start_elev
            ])

            endpoint_cursor.insertRow([
                arcpy.PointGeometry(end_point, geom.spatialReference),
                pipe_id,
                "Inlet",
                end_elev
            ])
            
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(manholes)
fieldmappings.addTable(endpoints)

while fieldmappings.findFieldMapIndex("ELEVATION") != -1:
    fieldmappings.removeFieldMap(
        fieldmappings.findFieldMapIndex("ELEVATION")
    )

fm_elev = arcpy.FieldMap()
fm_elev.addInputField(endpoints, "ELEVATION")

elev_out = fm_elev.outputField
elev_out.name = "PIPE_ELEVATION"
fm_elev.outputField = elev_out

fieldmappings.addFieldMap(fm_elev)

keep_fields = [
    "OBJECTID",
    "PIPE_ID",
    "END_TYPE",
    "PIPE_ELEVATION"
]

for field in list(fieldmappings.fields):
    if field.name not in keep_fields:
        index = fieldmappings.findFieldMapIndex(field.name)
        fieldmappings.removeFieldMap(index)
        
arcpy.analysis.SpatialJoin(target_features=manholes, join_features=endpoints, out_feature_class="spatial_join", join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_COMMON", match_option="INTERSECT", field_mapping=fieldmappings)

print("Done Spatial Join successfully")

###############################-------------- mapping the pipe elevations --------------#####################################
import arcpy
import os
from collections import defaultdict

# --------------------------------------------------
# 1. CONFIGURATION: change these to match your data
# --------------------------------------------------

target_gdb = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
gdb = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Corrected.gdb"

manholes_fc = os.path.join(target_gdb, "uswwManholeP")
spatial_join_fc = os.path.join(gdb, "spatial_join")

# Check paths before opening cursors.
for fc in [manholes_fc, spatial_join_fc]:
    if not arcpy.Exists(fc):
        raise ValueError(f"Dataset not found: {fc}")

output_fields = [
    "InvertElevation1",
    "InvertElevation2",
    "InvertElevation3",
    "InvertElevation4"
]

connections = defaultdict(lambda: {"inlet": [], "outlet": []})
invalid_ids = set()

# Read endpoint elevations.
with arcpy.da.SearchCursor(
    spatial_join_fc,
    ["TARGET_FID", "END_TYPE", "PIPE_ELEVATION"]
) as cursor:

    for mh_id, end_type, elevation in cursor:
        end_type = str(end_type).strip().lower()

        if end_type not in ("inlet", "outlet") or elevation is None:
            invalid_ids.add(mh_id)
            continue

        connections[mh_id][end_type].append(float(elevation))

# Prepare values before modifying the manholes.
results = {}

for mh_id, group in connections.items():
    inlets = sorted(group["inlet"], reverse=True)
    outlets = group["outlet"]

    if (
        mh_id in invalid_ids
        or len(outlets) > 1
        or len(inlets) + len(outlets) > 4
    ):
        print(f"Skipped manhole {mh_id}: check endpoint records")
        continue

    values = inlets + outlets
    results[mh_id] = values + [None] * (4 - len(values))

# Match original manhole Object ID to spatial-join TARGET_FID.
updated = 0

with arcpy.da.UpdateCursor(
    manholes_fc,
    ["OID@"] + output_fields,
    explicit=True
) as cursor:

    for row in cursor:
        if row[0] in results:
            row[1:] = results[row[0]]
            cursor.updateRow(row)
            updated += 1

print(f"Updated {updated} manholes.")
print(f"IDs with missing elevations or unknown END_TYPE: {len(invalid_ids)}")

############################------------FIELD CALCULATING------------##################################
fields=[
["HighPipeElevation", "!InvertElevation1!"],
]
arcpy.management.CalculateFields(manholes_fc, "Python", fields)

arcpy.management.DeleteField(manholes_fc, "TARGET_FID")

###############################-------------- Moving Manholes Points --------------#####################################
import arcpy
import os

target_gdb = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
manholes_fc = os.path.join(target_gdb, "uswwManholeP")

elevation_fields = [
    "InvertElevation1",
    "InvertElevation2",
    "InvertElevation3",
    "InvertElevation4"
]

updated = 0
skipped = 0

with arcpy.da.UpdateCursor(
    manholes_fc,
    elevation_fields + ["SHAPE@Z"]
) as cursor:

    for row in cursor:

        # Keep only filled values. Zero is a valid elevation.
        values = [value for value in row[:4] if value is not None]

        if not values:
            skipped += 1
            continue

        average_z = sum(values) / len(values)

        # Change only the point's Z coordinate.
        row[4] = average_z
        cursor.updateRow(row)

        updated += 1

print(f"Updated point Z values: {updated}")
print(f"Skipped points with all four fields NULL: {skipped}")

import arcpy
import os
from collections import defaultdict

import arcpy

def extend_pipe_to_manholes(
    pipe_geom,
    start_manhole=None,
    end_manhole=None
):
    if pipe_geom.partCount != 1:
        raise ValueError("This function supports single-part pipes only.")

    vertices = [
        arcpy.Point(p.X, p.Y, p.Z, p.M)
        for p in pipe_geom.getPart(0)
    ]

    def same_xyz(a, b):
        return (a.X, a.Y, a.Z) == (b.X, b.Y, b.Z)

    # Add a new vertex before the original pipe start.
    if start_manhole is not None:
        point = start_manhole.firstPoint

        if not same_xyz(point, vertices[0]):
            vertices.insert(
                0,
                arcpy.Point(
                    point.X,
                    point.Y,
                    point.Z,
                    vertices[0].M
                )
            )

    # Add a new vertex after the original pipe end.
    if end_manhole is not None:
        point = end_manhole.firstPoint

        if not same_xyz(point, vertices[-1]):
            vertices.append(
                arcpy.Point(
                    point.X,
                    point.Y,
                    point.Z,
                    vertices[-1].M
                )
            )
            
            return arcpy.Polyline(
                arcpy.Array(vertices),
                pipe_geom.spatialReference,
                has_z=pipes_have_z,
                has_m=pipes_have_m
            )

# --------------------------------------------------
# 1. INPUTS
# --------------------------------------------------

target_gdb = r"D:\Amaala Staff Village\utilities\Updated Target Schema\Only Filled Data - Corrected\TRSDC DB.gdb"
gdb = r"D:\Amaala Staff Village\utilities\Infra Arcpro Projects\Sewer 6A and 6B\Corrected.gdb"

pipes_fc = os.path.join(target_gdb, "uswwLateralLineL")  # Change this
manholes_fc = os.path.join(target_gdb, "uswwManholeP")
spatial_join_fc = os.path.join(gdb, "spatial_join")

pipe_description = arcpy.Describe(pipes_fc)
pipes_have_z = pipe_description.hasZ
pipes_have_m = pipe_description.hasM

manhole_id_field = "TARGET_FID"
pipe_id_field = "PIPE_ID"
end_type_field = "END_TYPE"

end_type_map = {
    "start": "start",
    "end": "end",
    "outlet": "start",
    "inlet": "end"
}

for fc in [pipes_fc, manholes_fc, spatial_join_fc]:
    if not arcpy.Exists(fc):
        raise ValueError(f"Dataset not found: {fc}")

for fc in [pipes_fc, manholes_fc]:
    if not arcpy.Describe(fc).hasZ:
        raise ValueError(f"Dataset is not Z-enabled: {fc}")


# --------------------------------------------------
# 2. READ MANHOLE GEOMETRIES
# --------------------------------------------------

manholes = {}

with arcpy.da.SearchCursor(
    manholes_fc,
    ["OID@", "SHAPE@"]
) as cursor:

    for oid, geometry in cursor:
        if geometry is not None and geometry.pointCount > 0:
            manholes[oid] = geometry


# --------------------------------------------------
# 3. READ PIPE–MANHOLE CONNECTIONS
# --------------------------------------------------

connections = defaultdict(dict)
invalid_pipes = set()

with arcpy.da.SearchCursor(
    spatial_join_fc,
    [pipe_id_field, manhole_id_field, end_type_field]
) as cursor:

    for pipe_id, manhole_id, end_type in cursor:

        # Skip unmatched spatial-join rows.
        if pipe_id in (None, -1) or manhole_id in (None, -1):
            continue

        # Supports numeric IDs or text containing numeric Object IDs.
        pipe_id = int(pipe_id)
        manhole_id = int(manhole_id)

        end_key = str(end_type).strip().lower()
        pipe_end = end_type_map.get(end_key)

        if pipe_end is None:
            invalid_pipes.add(pipe_id)
            print(f"Pipe {pipe_id}: unknown END_TYPE {end_type!r}")
            continue

        if manhole_id not in manholes:
            invalid_pipes.add(pipe_id)
            print(f"Pipe {pipe_id}: manhole {manhole_id} not found")
            continue

        # Repeated identical rows are harmless.
        # Different manholes assigned to the same end are a conflict.
        previous_id = connections[pipe_id].get(pipe_end)

        if previous_id is not None and previous_id != manhole_id:
            invalid_pipes.add(pipe_id)
            print(
                f"Pipe {pipe_id}: conflicting manholes "
                f"for its {pipe_end}"
            )
            continue

        connections[pipe_id][pipe_end] = manhole_id


# --------------------------------------------------
# 4. EXTEND EACH PIPE USING YOUR FUNCTION
# --------------------------------------------------

updated = 0
skipped = 0
found_pipe_ids = set()

with arcpy.da.UpdateCursor(
    pipes_fc,
    ["FIXED_ID", "SHAPE@"]
) as cursor:

    for row in cursor:
        pipe_id, geometry = row
        found_pipe_ids.add(pipe_id)

        if pipe_id in invalid_pipes:
            skipped += 1
            continue

        if pipe_id not in connections:
            continue

        if (
            geometry is None
            or geometry.pointCount < 2
            or geometry.partCount != 1
            or geometry.hasCurves
        ):
            print(f"Pipe {pipe_id}: empty, multipart, or curved; skipped")
            skipped += 1
            continue

        ends = connections[pipe_id]

        start_manhole = manholes.get(ends.get("start"))
        end_manhole = manholes.get(ends.get("end"))

        row[1] = extend_pipe_to_manholes(
            geometry,
            start_manhole=start_manhole,
            end_manhole=end_manhole
        )

        cursor.updateRow(row)
        updated += 1


# --------------------------------------------------
# 5. SUMMARY
# --------------------------------------------------

missing_pipe_ids = set(connections) - found_pipe_ids

print(f"Processed and saved pipes: {updated}")
print(f"Skipped pipes: {skipped}")
print(f"Table pipe IDs not found in pipe feature class: {len(missing_pipe_ids)}")


