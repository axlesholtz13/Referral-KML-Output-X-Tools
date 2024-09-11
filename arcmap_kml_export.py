
# ---------------------------------------------------------------------------
# Arc Map Version: 10.8
# arcmap_kml_export.py
# Created: 2023-2024

# Description:Export KML file of a selected TSLs blocks, roads and WTRAs; using xtools add-in. 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# icence ID Input
LicenceID = arcpy.GetParameterAsText(0)
SQL_Expression = "LICENCE_ID = '{}'".format(LicenceID)

# KML Output
KML_output = arcpy.GetParameterAsText(1)
Blocks_shp = KML_output.replace(".kml", ".shp")

# Local variables:
BCTS_Rds_All = "BCTS Rds-All"
BCTS_Blks_ALL_BOUNDARY = "BCTS Blks-ALL BOUNDARY"
BCTS_SU_Basic_Fill = "BCTS SU-Basic Fill"


# Process: Select
arcpy.Select_analysis(BCTS_Blks_ALL_BOUNDARY, Blocks_shp, SQL_Expression)
arcpy.AddMessage("Selecting Queried BCTS Blocks TSL. " + LicenceID)

# Process: Select BCTS Roads By Location
arcpy.SelectLayerByLocation_management(BCTS_Rds_All, "INTERSECT", Blocks_shp, "100 Meters", "NEW_SELECTION", "NOT_INVERT")
arcpy.AddMessage("Selecting BCTS Roads within 100 meters of " + LicenceID)

# Process: Select BCTS WTRA Layer By Location
arcpy.SelectLayerByLocation_management(BCTS_SU_Basic_Fill, "INTERSECT", Blocks_shp, "", "NEW_SELECTION", "NOT_INVERT")
arcpy.AddMessage("Selecting Intersecting WTRAs")

# Process: Select BCTS All Blocks Layer By Attribute
arcpy.SelectLayerByAttribute_management(BCTS_Blks_ALL_BOUNDARY, "NEW_SELECTION", SQL_Expression)
arcpy.AddMessage("All Block Features Selected: " + SQL_Expression)


#-----XTOOLS------
arcpy.AddMessage("Importing xtools toolbox")
# Xtools add-in tool (Export to KML)
arcpy.ImportToolbox("E:/sw_nt/XTools/XTools Pro/Toolbox/XTools Pro.tbx")

arcpy.AddMessage("Exporting KML " + KML_output)
arcpy.XToolsGP_ExportDataToKMLMultiple_xtp("'BCTS SU-Basic Fill';'BCTS Rds-All';'BCTS Blks-ALL BOUNDARY'", KML_output,
"LABEL_BY_LAYER","#","FEATURE","DONT_CREATE_FOLDERS","#","NO_BOUNDARIES","#","#","NO_ALTITUDE","#",
"2000","CLAMPED_TO_GROUND","METERS","EXTRUDE","NO_TIME","#","#","PNG")

arcpy.AddMessage("Deleting " + Blocks_shp)
if arcpy.Exists(Blocks_shp):
	arcpy.management.Delete(Blocks_shp)

