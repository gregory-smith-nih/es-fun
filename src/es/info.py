import glsutils as gls
import esutils

def info(es, index, mapping):
    response = esutils.info(es)
    gls.jprint(response)