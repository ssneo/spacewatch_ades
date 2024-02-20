




def get_telescope_header_info():
    #the ADES header has new name: For each MPC code, the values for these static fields are below
    header_info = {}
    header_info['691'] = {}


    header_info['691']['submitter'] = {}
    #submitter_name is a required field
    header_info['691']['submitter']['name'] = 'M. J. Brucker' #this is the name in the obs80 CON line: If this is changed, a different program code will be issued for this observatory
    #submitter_institution is an optional field. A value of None will be ignored
    header_info['691']['submitter']['institution'] = 'University of Arizona' #this is the obs80 CON line: If this is changed, a different program code will be issued for this observatory

    header_info['691']['observatory'] = {}
    #mpcCode is a required field (3 or 4 char.)
    header_info['691']['observatory']['mpcCode'] = '691' #mpcCode
    #observatory_name is an optional field. A value of None will be ignored. (max string length = 100)
    header_info['691']['observatory']['name'] = 'Kitt Peak' #Observatory Name

    #fundingSource is an optional field. A value of None will be ignored
    header_info['691']['fundingSource'] = 'NASA' #Funding Source

    header_info['691']['telescope'] = {}
    #telescope_name is an optional field. A value of None will be ignored. (max string length = 100)
    header_info['691']['telescope']['name'] = 'SW 0.9m' #telescope Name
    #telescope_design is a required field. (max string length = 25)
    header_info['691']['telescope']['design'] = 'NEED_TO_UPDATE_VALUE' #telescope Design
    #telescope_aperture is a required field. (positive decimal number with no more than a total of 6 characters)
    header_info['691']['telescope']['aperture'] = '0.9' #telescope aperture
    #telescope_detector is a required field: Only allowed values are in the documentation
    header_info['691']['telescope']['detector'] = 'CCD' #camera type, only specific values allowed
    #telescope_fRatio is an optional value. Value of None will be ignored. (postive decimal number with no more than a total of 6 characters)
    header_info['691']['telescope']['fRatio'] = '3' #fRatio
    #telescope_filter  is an optional value. A value of None will be ignored. (max string length = 25)
    header_info['691']['telescope']['filter'] = 'V+R+I' #filter #only specific values allowed
    #telescope_arraySize is an optional value. A value of None will be ignored. (max string length=25)
    header_info['691']['telescope']['arraySize'] = None #arraySize
    #telescope_pixelScale is an optional value. A value of None will be ignored. (positive decimal number with no more than total of 6 characters)
    header_info['691']['telescope']['pixelScale'] = None #pixelScale




    return header_info

