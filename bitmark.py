import pprint
import html
import re



###############
## constants ##
###############

NOMATCH     = 'no match'

CURRENT_DIR = '<to be implemented>'
INPUT_FN    = 'src/kopie_von_t59_####_hunte37_via_raspi-docker-02.tlp'
OUTPUT_FN   = 'out.html'


#############
## helpers ##
#############


###############
## functions ##
###############

class Holder:
    locals  = []
    remotes = []
    state_x = 'x'
    state_y = 'y'

    def write_html(self, out_file):
        out_str = pprint.pformat(self)
        out_file.write(out_str)


def pf_match(match_object):
    
    pprint.pprint(type(match_object) )

    try:
        match_info = ((
            "########\n" + 
            "{pretty}\n" +
            "########\n" + 
            "span_hex: ({start_hex}, {end_hex}), length_of_match: {length}\n" +
            "match: '{group}'"
            
            '').format(
                pretty    = pprint.pformat(match_object),
                start_hex = hex(match_object.span()[0]),
                end_hex   = hex(match_object.span()[1]),
                length    = match_object.span()[1] - match_object.span()[0],
                group     = match_object.group(1)
            ) 
        )
    except:
        match_info = NOMATCH
    return(match_info)

 



def parse_entry_to_holder(matched_group, holder):
    
    # WIP:

    p2 = re.compile(b'(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)$')
    m = p2.search(matched_group)
    match_info = pf_match(m)

    print('################ Inner match')
    if match_info == NOMATCH:
        print('No inner match')
    else:
        try:
            groups_str = "## s1:{size_1} ## f1:{field_1} ## s2:{size_2} ## f2:{field_2} ## s3:{size_3} ## f3:{field_3} ## s4:{size_4} ## f4:{field_4} ## s5:{size_5} ## f5:{field_5} ".format(
                size_1  = int.from_bytes(m.group(1), 'little'), 
                field_1 = m.group(2).decode("utf-8"), 
                size_2  = int.from_bytes(m.group(3), 'little'), 
                field_2 = m.group(4).decode("utf-8"),
                size_3  = int.from_bytes(m.group(5), 'little'), 
                field_3 = m.group(6).decode("utf-8"),
                size_4  = int.from_bytes(m.group(7), 'little'), 
                field_4 = m.group(8).decode("utf-8"),
                size_5  = int.from_bytes(m.group(9), 'little'), 
                field_5 = m.group(10).decode("utf-8"),
            )
        except:
            groups_str = "Fields are not convertible"

        print(groups_str)

    return(1)





def parse_whole_string(in_bytes, holder):

    #print('\n############################## match1')
    #p1 = re.compile(b'\01\00\00\00[^\00]...')
    #m = p1.search(in_bytes)
    #print(pf_match(m))

    print('\n############################## match')

    print("Number of bytes to parse: {n}".format(n=len(in_bytes)))
    #p2 = re.compile(b'\01\00\00\00(.*?)((\01\00\00\00)|(\00\00\00\00\00\00\00\00\00))')
    p2 = re.compile(b'\01\00\00\00(.*?)\01\00\00\00')
    m = p2.search(in_bytes)
    match_info = pf_match(m)
    print(match_info)

    if match_info != NOMATCH:

        result = parse_entry_to_holder(m.group(1), holder)


        parse_whole_string(in_bytes[m.span()[1]-5:], holder)




def process_whole_file(input_fn, output_fn):
    with open(input_fn, "rb") as in_file:
        in_bytes = in_file.read()

    holder = Holder()
    parse_whole_string(in_bytes, holder)

    with open(output_fn, "w") as out_file:
        holder.write_html(out_file)






##########
## main ##
##########

if __name__ == '__main__':
    print('p2')
    process_whole_file(INPUT_FN, OUTPUT_FN)
