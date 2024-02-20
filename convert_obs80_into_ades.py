

from header_configs import get_telescope_header_info
from create_xml import generate_xml, write_xml
from calculate_JD import calculateJD
from calculate_obs_time import calculateObsTime
from calculateRA_degs import calculateRa_degs
from calculateDec_degs import calculateDec_degs
from determine_Permid_Provid_Values import determinePermidProvidValues
from convert_ast_cat_value import convert_ast_cat
import sys


def create_ades( telescope=None, obs80_file_location=None, xml_or_psv=None, output_file_location=None, output_file_ending=None):

    #telescope: Accepted values are whatever is used as the key words in the header_configs.py file. For example '691'

    header_info = get_telescope_header_info() #get static header information from header_configs.py

    file = open( obs80_file_location, 'r')
    obs80_file = file.readlines()
    file.close()

    header_info, astrometry_catalog = extract_header_values_from_obs80_file( header_info, obs80_file, telescope )

    confirm_header_format( telescope = telescope, header_info=header_info )

    obs_data = extract_data_values_from_obs80_file( obs80_file, astrometry_catalog )

    #for key in header_info:
    #    for key1 in header_info[key]:
    #        print (key1, header_info[key][key1])
    #stop

    for key in obs_data:
        print (key, obs_data[key])
    #stop

    ades = generate_xml( header_info[telescope], obs_data )

    #writing
    write_xml( ades, output_file_location )

    #obs_data = read_extract_values_fro



def extract_header_values_from_obs80_file( header_info, obs80_file, telescope ):

    for i in range( 0, len( obs80_file) ):

        if obs80_file[i][0:3] == 'OBS':
            if 'observers' != header_info[telescope]: #if observers are in the static file, ignore this
                observers = obs80_file[i][4:-1].split(',') #don't count the last return charcater
                header_info[telescope]['observers'] = {}
                for j in range( 0, len( observers ) ):
                    header_info[telescope]['observers'][j] = {}
                    header_info[telescope]['observers'][j]['name'] = observers[j]

        elif obs80_file[i][0:3] == 'MEA':
            if 'measures' != header_info[telescope]: #if measures are in the static file, ignore this
                measurers = obs80_file[i][4:-1].split(',') #names should be seperated by comma #don't count the last return charcater
                header_info[telescope]['measurers'] = {}
                for j in range( 0, len( measurers ) ):
                    header_info[telescope]['measurers'][j] = {}
                    header_info[telescope]['measurers'][j]['name'] = observers[j]

        elif obs80_file[i][0:3] == 'NET':
            astrometry_catalog = obs80_file[i][4:-1] #don't include the final return character

        elif obs80_file[i][0:3] == 'COM':
            if 'comment' in header_info[telescope]: 
                pass
            else:
                header_info[telescope]['comment'] = {}
                

            #how many lines are in the comment section
            number_of_lines = len( header_info[telescope]['comment'] )
            header_info[telescope]['comment'][ number_of_lines ] = {}
            header_info[telescope]['comment'][ number_of_lines ]['line'] = obs80_file[i][4:-1]

    return header_info, astrometry_catalog

def extract_data_values_from_obs80_file( obs80_file, astrometry_catalog ):

    obs = {}
    count = 0

    for i in range( 0, len( obs80_file ) ):

        if obs80_file[i][0:3] != 'COD' and obs80_file[i][0:3] != 'CON' and obs80_file[i][0:3] != 'OBS' and obs80_file[i][0:3] != 'MEA' and obs80_file[i][0:3] != 'TEL' and obs80_file[i][0:3] != 'NET' and obs80_file[i][0:3] != 'BND' and obs80_file[i][0:3] != 'ACK' and obs80_file[i][0:3] != 'COM' and len( obs80_file[i] ) > 80: #length of line is typicaly 81 when you include the return character

            obs80 = obs80_file[i]

            obs[count] = {}
            #from MPCReport.txt File
            #print( self.obs80[i][:-1] )
            
            name = obs80[0:13]
            permid, provid, trksub = determinePermidProvidValues( name )
            if permid != None:
                obs[count]['permID'] = permid
            if provid != None:
                obs[count]['provID'] = provid
            if trksub != None:
                obs[count]['trkSub'] = trksub

            
            if obs80[14] == 'C':
                date_start = 15
            elif obs80[15] == 'C':
                date_start = 16

            time_value = {}
            time_value['year'] = obs80[date_start : (date_start + 4) ]
            time_value['month'] = obs80[ (date_start + 5) : (date_start + 7) ]
            time_value['day'] = obs80[ (date_start + 8) : (date_start + 10) ]
            time_value['time'] = "0." + obs80[ (date_start + 11) : (date_start + 17) ].replace(" ", "") #get rid of the extra spaces
            obsTime = calculateObsTime( time_value ) #this function pull the needed values from the dictionary
            obs[count]['obsTime'] = str( obsTime )

            ra = {}
            ra['ra_hour'] = obs80[32:34]
            ra['ra_minutes'] = obs80[35:37]
            ra['ra_seconds'] = obs80[38:43].replace(" ", "") #get rid of a possible trailing blank space
            ra = calculateRa_degs( ra )
            obs[count]['ra'] = str( ra )

            dec={}
            dec['dec_degrees'] = obs80[44:47]
            dec['dec_minutes'] = obs80[48:50]
            dec['dec_seconds'] = obs80[51:56].replace(" ", "") #get rid of a possible trailing blank space
            dec = calculateDec_degs( dec )
            obs[count]['dec'] = str( dec )

            
            obs[count]['mag'] =obs80[65:70]
            obs[count]['band'] = obs80[70] #filter band
            obs[count]['stn'] = obs80[77:80] #mpc code
            obs[count]['astCat'] = convert_ast_cat( astrometry_catalog )
            obs[count]['mode'] = "CCD"

            #obs[count]['rmsRA'] = #need to determine value
            #obs[count]['rmsDec'] = #need to determine value
            #obs[count]['rmsMag'] = #need to determine value





            count += 1

    return obs

            





def confirm_header_format( telescope=None, header_info=None ):


    for key in header_info:
        if key == 'observatory':
            check_key_value_and_lengths( header_info=header_info, key='observatory', value='mpcCode', required=True, data_type='s3_4')
            check_key_value_and_lengths( header_info=header_info, key='observatory', value='name', required=False, data_type='s_100')

        elif key == 'submitter':
            check_key_value_and_lengths( header_info=header_info, key='submitter', value='name', required=True, data_type='s_100')
            check_key_value_and_lengths( header_info=header_info, key='submitter', value='institution', required=False, data_type='s_100')

        elif key == 'telescope':
            check_key_value_and_lengths( header_info=header_info, key='telescope', value='name', required=False, data_type='s_100')
            check_key_value_and_lengths( header_info=header_info, key='telescope', value='design', required=True, data_type='s_25')
            check_key_value_and_lengths( header_info=header_info, key='telescope', value='aperture', required=True, data_type='pd6')
            check_key_value_and_lengths( header_info=header_info, key='telescope', value='detector', required=True, data_type='s_25')
            check_key_value_and_lengths( header_info=header_info, key='telescope', value='fRatio', required=False, data_type='pd6')
            check_key_value_and_lengths( header_info=header_info, key='telescope', value='filter', required=False, data_type='s_25')
            check_key_value_and_lengths( header_info=header_info, key='telescope', value='arraySize', required=False, data_type='s_25')
            check_key_value_and_lengths( header_info=header_info, key='telescope', value='pixelScale', required=False, data_type='pd6')
            

def check_key_value_and_lengths( header_info=None, key=None, value=None, required=None, data_type=None ):

    if required == True: #check if it is a required field
        if key != header_info:
            print (f"Key: {key} is not found in the header_info dictionary")
            sys.exit()
        if value != None:
            if header_info[key][value] != header_info[key]:
                 print (f"Key Value: {key, value} is not found in the header_info dictionary")
                 sys.exit()

    if data_type == 's3_4':
        if len( header_info[key][value] ) == 3 or len( header_info[key][value] ) == 4:
            pass
        else:
            print (f"Key Value: {key, value} did not have a length of 3 or 4")
            sys.exit()

    elif data_type == 's_100':
        if len( header_info[key][value] ) > 100:
            print (f"Key Value: {key, value} did not have a length less than 100")
            sys.exit()

    elif data_type == 's_25':
        if len( header_info[key][value] ) > 25:
            print (f"Key Value: {key, value} did not have a length less than 25")
            sys.exit()

    elif data_type == 'pd6':
        if len( header_info[key][value] ) > 6:
            print (f"Key Value: {key, value} did not have a length less than 6")
            sys.exit()

        try:
            decimal = float( header_info[key][value] )
            if decimal < 0:
                print (f"Key Value: {key, value} value is not postive")
                sys.exit()

        except:
            print (f"Key Value: {key, value} is not able to be converted into a decimal")
            sys.exit()
        
            
    
    












if __name__ == "__main__": #this allows the code to be ran and a test_output to be generated

    create_ades( telescope='691', obs80_file_location='sample_submission_80_character.txt', xml_or_psv='xml', output_file_location="/users/linder/research/spacewatch_ades/output_xml", output_file_ending="xml")



