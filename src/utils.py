from pathlib import Path
PATH = Path(__file__).parents[1]

def config():
    '''Load keys file `config.yml` and return dict'''
    
    from yaml import safe_load
    
    keys = safe_load(open(PATH.joinpath('config.yml')))
    
    return keys