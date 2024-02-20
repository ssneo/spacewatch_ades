
import xml.etree.ElementTree as XMLElement
import xml.dom.minidom as minidom
import sys

# T. Linder, June 2023
# refactored by C. Nugent, September 2023

def generate_xml(header_data, obs_data):
    """
    Takes all the ADES 2022 data and puts it into XML tree.
    Call this program the first time you're creating the
    XML submission, this call includes header information.
    Args:
        header_data: dictionary, required ADES header information
        obs_data: dictionary, with optical-observatory related data
        filename: string, name of output file
    Returns:
        XMLElement, ades, obsData: the xml data
    """
    ades = XMLElement.Element("ades", version="2022")
    obsBlock = XMLElement.SubElement(ades, "obsBlock")

    # ObsBlock Information Section
    obsContext = XMLElement.SubElement(obsBlock, "obsContext")

    # Observatory Information section to the next ####
    observatory = XMLElement.SubElement(obsContext, "observatory")

    for key in header_data['observatory']:
        value = XMLElement.SubElement(observatory, key)
        value.text = header_data["observatory"][key]
    ###################################
        
    # Submitter Information Section 
    submitter = XMLElement.SubElement(obsContext, "submitter")

    for key in header_data['submitter']:
        value = XMLElement.SubElement(submitter, key)
        value.text = header_data["submitter"][key]
    ##################
        

    # observers Information Section 
    observers = XMLElement.SubElement(obsContext, "observers")



    for j in header_data['observers']:
        for key in header_data['observers'][j]:
            #print ('key', key, 'j', j)
            #stop
            value = XMLElement.SubElement(observers, key)
            value.text = header_data["observers"][j][key]
    ##################
        

    # measurers Information Section 
    measurers = XMLElement.SubElement(obsContext, "measurers")

    for j in header_data['measurers']:
        for key in header_data['measurers'][j]:
            value = XMLElement.SubElement(measurers, key)
            value.text = header_data["measurers"][j][key]
    ##################
        
    # telescope Information Section 
    telescope = XMLElement.SubElement(obsContext, "telescope")

    for key in header_data['telescope']:
        if header_data["telescope"][key] != None:
            value = XMLElement.SubElement(telescope, key)
            value.text = header_data["telescope"][key]
    ##################
        
    # software Information Section 
    if 'software' in header_data:
        software = XMLElement.SubElement(obsContext, "software")

        for key in header_data['software']:
            value = XMLElement.SubElement(software, key)
            value.text = header_data["software"][key]
    ##################
        
    # coinvestigators Information Section 
    if 'coinvestigators' in header_data:
        coinvestigators = XMLElement.SubElement(obsContext, "coinvestigators")

        for j in header_data['coinvestigators']:
            for key in header_data['coinvestigators'][j]:
                value = XMLElement.SubElement(coinvestigators, key)
                value.text = header_data["coinvestigators"][j][key]
        ##################
            
    # collaborators Information Section 
    if 'collaborators' in header_data:
        collaborators = XMLElement.SubElement(obsContext, "collaborators")

        for j in header_data['collaborators']:
            for key in header_data['collaborators'][j]:
                value = XMLElement.SubElement(collaborators, key)
                value.text = header_data["collaborators"][j][key]
    ##################
        
    # fundingSource Information Section 
    if 'fundingSource' in header_data:
        fundingSource = XMLElement.SubElement(obsContext, "fundingSource")
        fundingSource.text = header_data["fundingSource"]

    ##################
        
    # comment Information Section
    if 'comment' in header_data: 
        comment = XMLElement.SubElement(obsContext, "comment")

        for j in header_data['comment']:
            for key in header_data['comment'][j]:
                value = XMLElement.SubElement(comment, key)
                value.text = header_data["comment"][j][key]
    ##################


    # obsData Information
    obsData = XMLElement.SubElement(obsBlock, "obsData")
    

    # Set optical values in one neat loop
    for j in obs_data:
        print (obs_data[j])
        optical = XMLElement.SubElement(obsData, "optical")

        if 'permID' in obs_data[j]:
            element = XMLElement.SubElement(optical, 'permID')
            element.text = obs_data[j]['permID']

        if 'provID' in obs_data[j]:
            element = XMLElement.SubElement(optical, 'provID')
            element.text = obs_data[j]['provID']

        if 'trkSub' in obs_data[j]:
            element = XMLElement.SubElement(optical, 'trkSub')
            element.text = obs_data[j]['trkSub']

        #required
        element = XMLElement.SubElement(optical, 'mode')
        element.text = obs_data[j]['mode']

        #required
        element = XMLElement.SubElement(optical, 'stn')
        element.text = obs_data[j]['stn']

        #required
        element = XMLElement.SubElement(optical, 'obsTime')
        element.text = obs_data[j]['obsTime']

        if 'rmsTime' in obs_data[j]:
            element = XMLElement.SubElement(optical, 'rmsTime')
            element.text = obs_data[j]['rmsTime']

        #required
        element = XMLElement.SubElement(optical, 'ra')
        element.text = obs_data[j]['ra']

        #required
        element = XMLElement.SubElement(optical, 'dec')
        element.text = obs_data[j]['dec']

        if 'rmsRA' in obs_data[j]:
            element = XMLElement.SubElement(optical, 'rmsRA')
            element.text = obs_data[j]['rmsRA']

        if 'rmsDEC' in obs_data[j]:
            element = XMLElement.SubElement(optical, 'rmsDEC')
            element.text = obs_data[j]['rmsDEC']

        #required
        element = XMLElement.SubElement(optical, 'mag')
        element.text = obs_data[j]['mag']

        if 'rmsMag' in obs_data[j]:
            element = XMLElement.SubElement(optical, 'rmsMag')
            element.text = obs_data[j]['rmsMag']

    
        #required
        element = XMLElement.SubElement(optical, 'band')
        element.text = obs_data[j]['band']

        #required
        element = XMLElement.SubElement(optical, 'astCat')
        element.text = obs_data[j]['astCat']

    # Pass this back, and then use update_xml to add observations as needed.
    #return XMLElement, ades, obsData

    return ades

def write_xml( ades, output_location ):

    tree = XMLElement.ElementTree(ades)
    xml_string = minidom.parseString(XMLElement.tostring(ades)).toprettyxml()
    with open(output_location, "w", encoding="UTF-8") as files:
        files.write(xml_string)




if __name__ == "__main__":
    ades_dict = {
        "mpcCode": "535",  # MPC-assigned observatory code
        "observatoryName": "Palermo Astronomical Observatory",
        "submitter": "D. Bowie",
        "observers": "B. Yonce",
        "measurers": "D. Bowie",
        "coinvestigators": "F. Apple",
        "telescope_design": "reflector",
        "telescope_aperture": "1.1",
        "telescope_detector": "CCD",
        "fundingSource": "NASA",
        "comment": "None",
    }
    ades_obs_dict = {
        # various codes can be found here:
        # https://www.minorplanetcenter.net/iau/info/ADESFieldValues.html
        #'permID': '04933',#IAU permanent designation
        #'provID': '2022 LB1',#MPC provisional designation (in unpacked form)
        # for unnumbered objects.
        "trkSub": "None",  # Observer-assigned tracklet identifier
        "mode": "CCD",  # Mode of instrumentation (probably CCD)
        "stn": "535",  # Observatory code assigned by the MPC
        # UTC date and time of the observation, ISO 8601 exended format,
        # i.e. yyyy-mm-ddThh:mm:ss.sssZ.
        # The reported time precision should be appropriate for the
        # astrometric accuracy, but no more than 6 digits are permitted
        # after the decimal. The trailing Z indicates UTC and is required.
        # Reccomend use "from astropy.time import Time" and then something like
        # str(time.isot)+'Z' where time is a Time astropy object with the
        # time of your observation.
        "obsTime": "1801-01-01T12:23:34.12Z",
        #'rmsTime': '3' #Random uncertainty in obsTime in seconds as estimated by the observer
        "ra": "3.639",  # decimal degrees in the J2000.0 reference frame
        "dec": "16.290",  # decimal degrees in the J2000.0 reference frame
        # For ra-dec and deltaRA- deltaDec observations, the random component
        # of the RA*COS(DEC) and DEC uncertainty (1σ) in arcsec as estimated
        # by the observer as part of the image processing and astrometric reduction.
        "rmsRA": "0.015",
        "rmsDec": "0.015",
        # Correlation between RA and DEC or between distance and PA that may
        # result from the astrometric reduction.
        #'rmsCorr': '-0.214',
        "astCat": "Gaia2",  # Star catalog used for the astrometric reduction
        # ‘UNK’, will be used for some archival observations to indicate that
        # the astrometric catalog is unknown.
        "mag": "21.91",  # Apparent magnitude in specified band.
        "rmsMag": "0.25",  # Apparent magnitude uncertainty, 1-sigma
        "band": "g",  # Passband designation for photometry.
        "photCat": "Gaia3",  # Star catalog used for the photometric reduction.
        # full list here: https://www.minorplanetcenter.net/iau/info/ADESFieldValues.html
        #'photAp': '13.3', #Photometric aperture radius in arcsec.
        #'logSNR': '0.78', #The log10 of the signal-to-noise ratio of the source
        # in the image integrated on the entire aperture used for the astrometric centroid.
        #'seeing': '0.8', #Size of seeing disc in arcsec, measured at Full-Width,
        # Half-Max (FWHM) of target point spread function (PSF).
        "exp": "20.0",  # Exposure time in seconds.
        #'remarks': 'None' #A comment provided by the observer. This field can be
        # used to report additional information that is not reportable in the notes
        # field, but that may be of relevance for interpretation of the observations.
        # Should be used sparingly by major producers.
    }
    xml_filename = "Catalog.xml"

    # generate the header and the first observation.
    XMLElement, ades, obsData = generate_xml(ades_dict, ades_obs_dict)

    # update your observations dictionary with your new obs, e.g.
    ades_obs_dict["mag"] = 10.1
    # update the xml
    #XMLElement, ades, obsData = update_xml(XMLElement, ades, obsData, ades_obs_dict)

    # write the ADES xml to file
    tree = XMLElement.ElementTree(ades)
    xml_string = minidom.parseString(XMLElement.tostring(ades)).toprettyxml()
    with open(xml_filename, "w", encoding="UTF-8") as files:
        files.write(xml_string)
