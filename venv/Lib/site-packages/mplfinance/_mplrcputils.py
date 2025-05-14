#!/usr/bin/env python
"""
rcparams utilities 
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys

__author__ = "Daniel Goldfarb"
__version__ = "0.1.0"
__license__ = "MIT"

def rcParams_to_df(rcp,name=None):
    keys = []
    vals = []
    for item in rcp:
        keys.append(item)
        vals.append(rcp[item])
    df = pd.DataFrame(vals,index=pd.Index(keys,name='rcParamsKey'))    
    if name is not None:
        df.columns = [name]
    else:
        df.columns = ['Value']
    return df

def compare_styles(s1,s2):
    with plt.rc_context():
         plt.style.use('default')
         plt.style.use(s1)
         df1 = rcParams_to_df(plt.rcParams,name=s1)

    with plt.rc_context():
         plt.style.use('default')
         plt.style.use(s2)
         df2 = rcParams_to_df(plt.rcParams,name=s2)
    
    df  = pd.concat([df1,df2],axis=1)
    dif = df[df[s1] != df[s2]].dropna(how='all')
    return (dif,df,df1,df2)

def main():
    """ Main entry point of the app """
    def usage():
        print('\n    Usage: rcparams <command> <arguments> \n')
        print('    Available commands: ')
        print('        rcparams find <findstring>')
        print('        rcparams compare <style1> <style2>')
        print('')
        exit(1)
    commands = ('find','compare')

    if len(sys.argv) < 3 :
        print('\n    Too few arguments!')
        usage()

    command  = sys.argv[1]
    if command not in commands:
        print('\n    Unrecognized command \"'+command+'\"')
        usage()

    if command == 'find':
        findstr = sys.argv[2]
        df = rcParams_to_df(plt.rcParams)
        if findstr == '--all':
            for key in df.index:
                print(key+':',df.loc[key,'Value'])
        else:
            print(df[df.index.str.contains(findstr)])

    elif command == 'compare':
        if len(sys.argv) < 4 :
            print('\n    Need two styles to compare!')
            usage()
        style1 = sys.argv[2]
        style2 = sys.argv[3]
        dif,df,df1,df2 = compare_styles(style1,style2)
        print('\n==== dif ====\n',dif)

    else:
        print('\n    Unrecognized command \"'+command+'\"')
        usage()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
