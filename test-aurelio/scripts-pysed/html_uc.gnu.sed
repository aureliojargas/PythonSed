#! /bin/sed -f
# html_uc.sed -- turn html tags to uppercase
# Just to be sure
s/Â°/&deg;/g
# Multiple lines are handled by storing a flag in hold space
# Fool the regexps below by adding a leading < (we'll remove
# it later)
x
/^j/ {
    x
    s/^/</
    x
}
x
# put Â° before each tag name
s/<[ 	]*/&Â°/g
# put Â° before each attribute name
t attr
:attr
s/\(<[^>]*[ 	]\+\)\([A-Za-z/]\+=[^> 	]\+\)/\1Â°\2/g
s/\(<[^>]*[ 	]\+\)\([A-Za-z/]\+="[^"]*"\)/\1Â°\2/g
s/\(<[^>]*[ 	]\+\)\([A-Za-z/]\+\)/\1Â°\2/g
t attr
# add conversion table: Â°Â° table
# table format: <to-char> <from-char>
# characters not in the table stop the conversion
s,$,Â°Â°//AAaBBbCCcDDdEEeFFfGGgHHhIIiJJjKKkLLlMMmNNnOOoPPpQQqRRrSSsTTtUUuVVvWWwXXxYYyZZz,
# substitute every char that's part of a tag or attribute and which follows a Â°
# also moves Â° after the char
t a
:a
s/Â°\(.\)\(.*Â°Â°.*\)\(.\)\1/\3Â°\2\3\1/
t a
# cleanup...
s/Â°Â°.*//
s/Â°//g
# Check if the hold space flag is to be set:
# j = this line continued the previous one
# J = this line will be continued by the next one
# jJ = both things
/<[^>]*$/ {
    x
    s/$/J/
    x
}
# If the hold space `j' flag was set, remove it, and also delete
# the leading < from pattern space
x
/^j/ {
    x
    s/^.//
    x
    s/j//
}
# Change the `J' flag to `j' and go on with the next line
s/J/j/
x
