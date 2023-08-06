
#####################################################################
#
# ESPREM Client 
#
# Project   : PYESPREMCLIENT
# Author(s) : Zafar Iqbal < zaf@saparc.gr >
# Copyright : (C) 2021 SPARC PC < https://sparc.space/ >
#
# All rights reserved. No warranty, explicit or implicit, provided.
# SPARC PC is and remains the owner of all titles, rights
# and interests in the Software.
#
#####################################################################

import os
import re
import io
import json
import atexit
#from pathlib import Path

#####################################################################

from . import s_log , s_config , s_net , s_cache , s_misc

####################################################################


def config_set_key( config_key , config_val ) :
    s_config.set_key( config_key , config_val )

def config_init_fromfile( config_path , config_key ) :
    return s_config.init_fromfile( config_path , config_key )

####################################################################

def do_request( request_endpoint , request_params , request_id = 0 , request_timeout_in = 60 ) :

    if( s_cache.available( [ request_endpoint , request_params ] ) ) :
        s_log.write_msg( "CACHE HIT" )
        return s_cache.get_data( [ request_endpoint , request_params ] )
    s_log.write_msg( "CACHE MISS" )
    
    ####################################################################

    request_timeout = int( s_config.get_key( "pyespremclient_timeout" , 10 ) )
    s_log.write_msg( "request_timeout=" + str( request_timeout )  )

    ####################################################################

    response = s_net.get_response( request_endpoint , request_params , request_id , request_timeout ) 

    if( "code" in response ) :
        res_str = json.dumps( response , indent = 4 )
        s_log.write_msg( res_str )
        return( response )
        #assert False , "code"

    if( "_error" in response ) :
        res_str = json.dumps( response , indent = 4 )
        s_log.write_msg( res_str )
        return( response )
        #assert False , "_error"

    ####################################################################

    s_cache.update( [ request_endpoint , request_params ] , response )

    ####################################################################

    return( response )

####################################################################

def log_msg( msg ) :
    s_log.write_msg( msg )

