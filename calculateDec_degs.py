
def calculateDec_degs( obs, negative_or_positive ):

    dec_degrees = int( obs["dec_degrees"] )
    dec_minutes = int( obs["dec_minutes"] )
    dec_seconds = float( obs["dec_seconds"] )

    if negative_or_positive == 'positive': #greater than or equal
        dec = dec_degrees + (dec_minutes / 60.) + (dec_seconds / 3600.)
    else: #dec is negative
        dec = dec_degrees - (dec_minutes / 60.) - (dec_seconds / 3600.)

    dec_degs = round( dec, 6 )

    return dec_degs