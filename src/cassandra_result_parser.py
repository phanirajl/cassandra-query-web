# coding: utf-8

import struct
def parseCassandraOutput(output):
    values=[]
    message=""
    columnWidthsFound=False
    
    for l  in output.splitlines():
        if("--+--" in l):
            headerlengths= [len(s) for s in l.split("+")]
            fmtstring = ' 1x '.join('{}{}'.format(abs(fw), 'x' if fw < 0 else 's')
                        for fw in headerlengths)
            fieldstruct = struct.Struct(fmtstring)
            parse = fieldstruct.unpack_from
            columnWidthsFound = True
        elif not (l.strip() == "" or "rows)" in l  or columnWidthsFound ):
            headers = [s.strip() for s in l.split("|")]
            values.append(headers)
        if("rows)" in l or len(l.strip()) == 0 ):
            message = message + ("\n"+ l) if not l.strip() == "" else ""
            continue
        elif(columnWidthsFound and "--+--" not in l):        
            text = l + (" "*headerlengths[-1])
            fields = parse(text)
            values.append([ s.strip() for s in fields])
    return {"result": values, "message": message}

