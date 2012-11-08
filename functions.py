"""
Some handy util functions
"""

import simplejson as json
import httplib
from datetime import datetime
from bson import objectid

def api_response(status,response,handler=None,code=200,errors=[]):
    if handler: handler.set_status(code)
    return dict(status=status,response=response,errors=errors)

def db_error(handler):
    return api_response('error','database error',handler,500)

def set_vars(handler,**kwargs):
    """
    Sets the API request parameters and their desired default values
    handler - the RequestHandler object for the request
    kwargs - key/value pairs of the request parameter and its default value
    """
    vars = Vars()
    for arg in kwargs:
        setattr(vars,arg,handler.get_argument(arg,default=kwargs[arg]))
    return vars

class Vars(object):
    """Empty object allowing for dot-declaration"""
    pass

class MongoEncoder(json.JSONEncoder):      
    def default(self,o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, objectid.ObjectId):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)

def prepare(response):
    return json.loads(json.dumps(response, cls = MongoEncoder))

def mult(base, gain, level):
	# if (as == True):

	value = (base+(gain*level))
	return value 
