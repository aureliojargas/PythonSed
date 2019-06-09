# setup:
# cd ~/PythonSed
# pip install -e .  # so my edits are live
# ./test.sh  # compare with sedsed --indent output

######################################################

# FIXED (commit: Add # command)
# line comments are lost
#    echo | pythonsed -d -f comment.sed

# FIXED (self.args_sed)
# s command regex and replacement are shown in Python syntax
# - ERE instead of BRE
# - \10 turns \1[0]
# - & turns \g<0>
# - \10 turns \g<1>0
# addresses are ok (AddressRegexp.__str__ uses self.pattern not self.regexp)
# echo aa0 | pythonsed -d -e '/\(x\)\10/ !s/\(a\)\10/\10&/g'
# |001|000|000|\(x\)\10  |None      |!|s|(a)\1[0]            |\g<1>0\g<0>         |g|
# a0aa0

# FIXED (self.delim)
# s/// using another delimiter - using / is hardcoded

# FIXED (remove line breaks but not trailing spaces in pack_script())
# s/// using spaces as delimiters
# echo | pythonsed -d -e 's a b '
# [line: s a b]
# sed.py error: subst: replacement incomplete

# trailing spaces are always removed (not in sedsed)

# partial line comments are lost

# using /address/I turns to /address/i

# do not support spaces before address flag
# echo X | pythonsed -e '/x/ I p'
# sed.py error: unknown function: I

# FIXED (commit: Add # command)
# remove escaping at EOL for comments:
# -#  Not implemented:|···! \
# +#  Not implemented:|···!█

# remove escaping at EOL for s:
# -1 s/^/#include <stdio.h>\
# +1 s/^/#include <stdio.h>

# remove escaping at EOL for a, i, c
# -/^|/ !i\
# -register empty
# +/^|/ !iregister empty

# blank lines are not preserved

import os.path
import sys
#from PythonSed import Sed, SedException
import PythonSed as pysed

sed = pysed.Sed()

#class Command_p(pysed.Command):
#    def apply(self, sed):
#        sed.printline('foo: ' + sed.PS)
#        return self.next

def foo(self, sed):
    sed.printline('foo: ' + sed.PS)
    print('line: ' + sed.reader.line)
    return self.next

# All SED commands grouped by kind
sedcmds = {
    'file':  'rw',
    'addr':  '/$0123456789\\',
    'multi': 'sy',
    'solo':  'nNdDgGhHxpPlq=',
    'text':  'aci',
    'jump':  ':bt',
    'block': '{}',
    'flag':  'gp0123456789w' + 'IiMme'  # default + GNU
}
def dumper(self):

    data = {
        'id': self.function,
        'modifier': '!' if self.negate else '',
        'content': self.str_arguments() or '',
        'addr1': self.address1 or '',
        'addr2': self.address2 or '',
#        'addr1flag': '',  #XXX
#        'addr2flag': '',  #XXX
    }

    # def compose_sed_command(data):
    # spacer on r,w,b,t commands only
    spaceme = sedcmds['file'] + sedcmds['jump']
    spaceme = spaceme.replace(':', '' )  # : label (no space!)
    if data['id'] in spaceme:
        idsep = ' '
    else:
        idsep = ''
    cmd = '%s%s%s%s' % (
        data['modifier'],
        data['id'],
        idsep,
        data['content'])


    # def compose_sed_address(data):
    address1 = str(data['addr1'])
    address2 = str(data['addr2'])

    if address2:
        address = '%s,%s' % (address1, address2)
    else:
        address = address1

    if address:
        address = address + ' '  # address, space, (command)

    return '%s%s' % (
    #return 'cmd: %s%s\nfoo: |%03d|%03d|%03d|%-10s|%-10s|%1s|%1s|%-20s|' % (
            address, cmd,
#            self.num,
#            self.next.num if self.next else 0,
#            self.branch.num if self.branch else 0,
#            self.address1, self.address2,
#            '!' if self.negate else ' ',
#            self.function,
#            self.str_arguments(),
    )

def dumper_address(self):
    if self.ignore_case:
        return '/%s/i' % self.pattern
    else:
        return '/%s/' % self.pattern

def dumper_y(self):
    source_chars, dest_chars = self.args
    return '/%s/%s/' % (source_chars, dest_chars)

def dumper_s(self):
    delim = self.delim
    pattern, repl, count, printit, ignore_case, write, filename = self.args_sed

    # count is 0 for g flag, flag removed if count = 1
    countflag = 'g' if count == 0 else count if count > 1 else ''

    flags = '%s%s%s%s' % (countflag,
                          'p' if printit else '',
                          'i' if ignore_case else '',
                          'w' if write else '')

    args = delim + pattern + delim + repl + delim + flags

    if filename:
        args += ' ' + filename

    return args

def dump_script(self):
    indent_char = ' ' * 4
    indent_level = 0
    for command in self.commands:
        if command.function == '}':
            indent_level -= 1
        print(indent_char * indent_level + str(command))
        if command.function == '{':
            indent_level += 1

#pysed.sed.Command_p.apply = foo
pysed.sed.Command.__str__ = dumper
pysed.sed.AddressRegexp.__str__ = dumper_address
pysed.sed.Command_s.str_arguments = dumper_s
pysed.sed.Command_y.str_arguments = dumper_y
sed.dump_script = dump_script

sed_script = sys.argv[1]
try:
    sed.no_autoprint = True
    sed.regexp_extended = False
    if os.path.isfile(sed_script):
        sed.load_script(sys.argv[1])
    else:
        sed.load_string(sys.argv[1])
    # sed.load_string('2,/foo/I { p; !d; $ { r foo.txt; }; s/\\(foo\\)/\1bar/gIw s.txt;\n# comment\ny/abc/ABC/; }')
    # sed.dump_script()
    dump_script(sed)
    # sed.apply('aurelio.txt')
except pysed.SedException as e:
    print(e.message)
except:
    raise

#Note that `sed.apply()` returns the list of lines printed by the script. As a default, these lines are printed to stdout. `sed.apply()` has an output parameter which enables to inhibit printing the lines (`output=None`) or enables to redirect the output to some text file (`output=somefile.txt`).
