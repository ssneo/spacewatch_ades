
import sys

def convert_ast_cat( obs80_value ):

    #print (obs80_value)

    if obs80_value == 'GAIA-DR2':
        return "Gaia2"
    
    else:
        print (f'Error: Unable to convert catalog to proper ADES: {obs80_value}')
        sys.exit()