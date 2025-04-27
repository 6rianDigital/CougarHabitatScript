####################################################################
## Program: PROG5000 Assignment 1 - "North Mountain Cougar Habitat #
##                                   Suitability Analysis"         #
## Programmer: Brian Gauthier                                      #
## Date: October 20, 2024                                          #
## Purpose: To query and display results for cougar habitat        #
##          suitability based on stand type selected               #
####################################################################

## import QInputDialog
from PyQt5.QtWidgets import QInputDialog


## get the active layer in Layers window
forest2024Lyr = iface.activeLayer()


## check if layer is valid & get unique species type from SP1 field
if not forest2024Lyr:
    print("No active layer found")
else:
    species_types = []
    for feature in forest2024Lyr.getFeatures():
        species = str(feature['SP1'])
        if species not in species_types and species not in ['NULL']:
            species_types.append(species)
            
    ## repeat until user cancels
    while True:
        ## prompt user for species type selection
        species_selected, ok = QInputDialog.getItem(None,"Select Species Type",
        "Please select a species type:", species_types, 0, False)
        
        if not ok:
            print("User canceled the input.")
            break
        
        print(f"Selected Species Type: {species_selected}")
    

        ## select forest polygons based on an the selected species type (SP1)
        SP1_expression = f'"SP1" = \'{species_selected}\''
        forest2024Lyr.selectByExpression(SP1_expression, QgsVectorLayer.SetSelection) 


        ## store the selected features in a selection object variable
        forestSel = forest2024Lyr.selectedFeatures()
        print(f"Number of selected features: {len(forestSel)}")


        ## initialize variables for suitability categories
        low_count = 0
        medium_count = 0
        high_count = 0

        low_area = []
        medium_area =[]
        high_area = []
    

        ## loop/iterate the selection & cast attrubutes to appropriate types
        for currFeature in forestSel:
            diam_stand = float(currFeature['AVDI'])
            height_stand = float(currFeature['HEIGHT'])
            cover_stand = str(currFeature['COVER_TYPE'])
            stand_area = float(currFeature['Shape_Area'])
    
            ## conditional statements for stand diameter
            if diam_stand < 20:
                diam_rating = 0.75
            elif diam_stand <= 30:
                diam_rating = 1.75
            else:
                diam_rating = 2.5
      

            ## conditional statements for stand height
            if height_stand < 10:
                height_rating = 1.25
            elif height_stand <= 20:
                height_rating = 2.5
            else:
                height_rating = 3.75


            ## conditional statement for stand cover type
            if cover_stand == "SW":
                cover_rating = 1
            elif cover_stand == "MW":
                cover_rating = 2
            elif cover_stand == "HW":
                cover_rating = 3.75
            else:
                cover_rating = 0 ## Null or unclassified cover type
   

            ## calculate suitability rating
            suitability_rating = diam_rating + height_rating + cover_rating

            if suitability_rating < 5:
                low_count += 1
                low_area.append(stand_area)
            elif suitability_rating > 8:
                high_count += 1
                high_area.append(stand_area)
            else:
                medium_count += 1
                medium_area.append(stand_area)
        
       


        ## calculate minimum, maximum, total, and average areas for each category
        def calculate_area_stats(area_list):
            if area_list:
                total_area = sum(area_list)
                count = len(area_list)
                return min(area_list), max(area_list), total_area, total_area / count
            return 0, 0, 0, 0
        
        low_min, low_max, low_total, low_avg = calculate_area_stats(low_area)
        medium_min, medium_max, medium_total, medium_avg = calculate_area_stats(medium_area)
        high_min, high_max, high_total, high_avg = calculate_area_stats(high_area)
    
    
        ## print report
        print("="*68)
        print("\t\tNorth Mountain Cougar Habitat Suitability Analysis")
        print(f"\t\t\t\t{len(forestSel)} of {species_selected} polygons in Study Area.")
        print("="*68)

        print(f"Low Suitability:")
        print(f"               - Number of polygons  : {low_count:>12.0f}")
        print(f"               - Minimum polygon area:     {low_min:>12.3f}")
        print(f"               - Maximum polygon area:     {low_max:>12.3f}")
        print(f"               - Total area          :     {low_total:>12.3f}")
        print(f"               - Average polygon area:     {low_avg:>12.3f}")
   
        print(f"\nMedium Suitability:")
        print(f"               - Number of polygons : {medium_count:>12.0f}")
        print(f"               - Minimum polygon area:    {medium_min:>12.3f}")
        print(f"               - Maximum polygon area:    {medium_max:>12.3f}")
        print(f"               - Total area          :    {medium_total:>12.3f}")
        print(f"               - Average polygon area:    {medium_avg:>12.3f}")
    
        print(f"\nHigh Suitability:")
        print(f"               - Number of polygons : {high_count:>12.0f}")
        print(f"               - Minimum polygon area:    {high_min:>12.3f}")
        print(f"               - Maximum polygon area:    {high_max:>12.3f}")
        print(f"               - Total area          :    {high_total:>12.3f}")
        print(f"               - Average polygon area:    {high_avg:>12.3f}")
        print("="*68)

 

