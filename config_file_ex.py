from plumbum import cli

with cli.ConfigINI('.myapp_rc.txt') as conf:
    one = conf['three']
    two = conf.get('one', default='2')
    three = conf.get('OTHER.a')
    
    # changing the configuration file
    conf['OTHER.c'] = 78
print(one, two, three)