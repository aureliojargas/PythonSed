# GNU sed accepts end-of-line comments with no ; before.
/bla/ {
    # at this address
    h
    g
    #
}
#loop end
s///
