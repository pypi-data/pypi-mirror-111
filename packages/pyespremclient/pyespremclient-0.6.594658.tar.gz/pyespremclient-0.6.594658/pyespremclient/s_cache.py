
#####################################################################
#
# ESPREM Client Misc
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
import json
import hashlib
import time

from . import s_log , s_config 

cache_dirpath = "/tmp/pyespremclient_cache/"

#####################################################################


def is_enabled( ) :

    s_log.write_msg("pyespremclient_cache="+s_config.get_key( "pyespremclient_cache" ))
    
    if( s_config.get_key( "pyespremclient_cache" ) == "on" ) :
        return True

    return False

def available( request_list ) :

    if( not is_enabled( ) ) : return False

    #return False

    request_str = request_list[ 0 ] + json.dumps( request_list[ 1 ] )
    cache_hash = hashlib.sha256( request_str.encode('utf-8') ).hexdigest( )
    cache_filepath = cache_dirpath + cache_hash + ".json"
    s_log.write_msg("cache_filepath="+cache_filepath)

    return os.path.isfile( cache_filepath ) 

# The response
def update( request_list , response_orig ) :
    if( not is_enabled( ) ) : return False
    # Create/Recreate cache directory
    init_directory( )
    request_str = request_list[ 0 ] + json.dumps( request_list[ 1 ] )
    cache_hash = hashlib.sha256( request_str.encode('utf-8') ).hexdigest( )
    cache_filepath = cache_dirpath + cache_hash + ".json"
    response = response_orig.copy( )
    response["_pyesprem_cache_time_"]=int(time.time())
    with open( cache_filepath , "w" ) as f :
        f.write( json.dumps( response ) )

def get_data( request_list ) :
    if( not is_enabled( ) ) : return False
    request_str = request_list[ 0 ] + json.dumps( request_list[ 1 ] )
    cache_hash = hashlib.sha256( request_str.encode('utf-8') ).hexdigest( )
    cache_filepath = cache_dirpath + cache_hash + ".json"
    with open( cache_filepath , "r" ) as f :
        return( json.load( f ) )


def init_directory( ) :

    if( not os.path.isdir( cache_dirpath ) ) :
        os.makedirs( cache_dirpath )

#####################################################################

init_directory( )
    