#python
from six import string_types

import numpy as np
import json
import subprocess
import datetime
import os
import glob
import sys
import platform
import errno
import glob
import sys


def get_root():
        ''' return the root location of git rep
        '''
        gitroot = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
        return gitroot

def get_platform_suffix():
        ''' return according to run time system ['osx', 'pi', 'linux','win']
        'Linux-4.4.34-v7+-armv7l-with-debian-8.0'
        'Linux-3.13.0-76-generic-x86_64-with-debian-jessie-sid'
        'Darwin-16.1.0-x86_64-i386-64bit'
        '''
        if sys.platform=='darwin':
            return 'osx'
        elif 'armv7' or 'armv7l' in platform.platform():
            return 'pi'
        elif sys.platform=='linux2':
            return 'linux'
        else:
            return 'win'


def get_config(mode='realtime'):
    '''Read the json config file, overwrite by user if exists.
    Sets the mode
    '''
    the_root = get_root()
    with open(the_root+'/config_common.json') as f: config = json.loads(f.read())
    try:
            byos = the_root+'/config_%s.json'%get_platform_suffix()
            with open(byos) as f: config2 = json.loads(f.read())
            for key in config2:
                    config[key]=config2[key]
    except Exception as e:
            #print e, "Could find os config", byos
            pass

    try:
            byuser = the_root+'/config_%s.json'%os.environ['USER']
            with open(byuser) as f: config2 = json.loads(f.read())
            for key in config2:
                    config[key]=config2[key]
    except:
            pass

    config['ROOT'] = the_root

    config = recursive_replace(config, config)
    config = recursive_replace(config, config) #Second Move

    #Flatten models parama to root config
    if "models" in config:
        model_architecture = config['model_architecture']
        if model_architecture in config['models']:
            model = config['models'][model_architecture]
            for key, val in model.items():
                config[key] = val

    #config['latest_checkpoint']=get_latest_checkpoint_path(config['train_dir'])

    try:
        os.makedirs(config['train_dir'])
    except Exception as e:
        pass # Probably already exists


    mapping = Mapping() #Easy wrrapper to allow attributes as well as dict
    mapping.update(config)
    return mapping


def recursive_replace(config, item):
    if isinstance(item, string_types):
        if '~' in item:
            item = os.path.expanduser(item)
        for other_key, other_val in config.items():
            if '$(%s)'%other_key in item:
                item = item.replace('$(%s)'%other_key, other_val)
        return item
    elif isinstance(item, list):
        other = list()
        for subitem in item:
            other.append(recursive_replace(config, subitem))
        return other
    elif isinstance(item, dict):
        other = dict()
        for key, val in item.items():
            other[key] = recursive_replace(config, val)
        return other
    else:
        return item



def get_list_of_folders_in_dir(data_dir):
    dirs_ = sorted([d.split('/')[-1] for d in glob.glob('%s/*'%data_dir) if os.path.isdir(d) and d[-1]!='_'])
    #wanted_words = ','.join(dirs_)
    return dirs_

def isarray(P):
     return isinstance(P, (list, tuple, np.ndarray))


def clean_str(s):
        ''' Get a clean string rep that can be used as a key for dictionary
        '''
        if s is None:
            return ''
        try:
            return str(s)
        except:
            return s.encode('utf-8')


def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:    # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
            else:
                    raise

def exception_description():
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


def get_latest_checkpoint_path(train_dir):
    import tensorflow as tf
    latest_ck_path = None
    try:
        states = tf.train.get_checkpoint_state(train_dir)
        if states is None:
            print ("Error, got none while trying to recover %s"%train_dir)
        latest_ck_path = states.all_model_checkpoint_paths[-1]
    except Exception as e:
        print(e)
    return latest_ck_path


class Mapping(dict):
    ''' Wrapper to allow both dict and attributes '''
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))



if __name__=='__main__':
        import os, sys, argparse
        gitroot = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
        config = get_config()
        for key, val in config.items():print (key, '\t\t', val)

