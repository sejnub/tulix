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
    matchlevel_1_outer             = 0
    matchlevel_2_inner             = 0
    matchlevel_3_inner_convertable = 0
    matchlevel_4_inner_field_sizes = 0

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



def match_level_4(size_1, field_1, size_2, field_2, size_3, field_3, size_4, field_4, size_5, field_5, holder):
    
    # f_s : field size
    # f_v : field value
    
    f_s_listen_if   = size_1
    f_v_listen_if   = field_1
    f_s_listen_port = size_2
    f_v_listen_port = field_2
    f_s_dest_host   = size_3
    f_v_dest_host   = field_3
    f_s_dest_port   = size_4
    f_v_dest_port   = field_4
    f_s_comment     = size_5
    f_v_comment     = field_5

    try:
        if (
            f_s_listen_if   < 3 or
            f_s_listen_port < 1 or
            f_s_dest_host   < 3 or
            f_s_dest_port   < 1
        ): 
            print('Unmatched level 4')
            return('error')
        else:
            print('Matched level 4')
            holder.matchlevel_4_inner_field_sizes += 1
            # WIP: 
            holder.locals.append(f_v_listen_port + '   ' + f_v_comment)
    except:
        return(NOMATCH)
    



def match_level_2_3(matched_group, holder):

    # WIP:

    p2 = re.compile(b'(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)$')
    m = p2.search(matched_group)
    match_info = pf_match(m)

    print('################ Inner match')
    if match_info == NOMATCH:
        print('No inner match')
    else:
        holder.matchlevel_2_inner += 1
        try:
            size_1  = int.from_bytes(m.group(1), 'little')
            field_1 = m.group(2).decode("utf-8")
            size_2  = int.from_bytes(m.group(3), 'little')
            field_2 = m.group(4).decode("utf-8")
            size_3  = int.from_bytes(m.group(5), 'little')
            field_3 = m.group(6).decode("utf-8")
            size_4  = int.from_bytes(m.group(7), 'little')
            field_4 = m.group(8).decode("utf-8")
            size_5  = int.from_bytes(m.group(9), 'little')
            field_5 = m.group(10).decode("utf-8")


            groups_str = "## s1:{size_1} ## f1:{field_1} ## s2:{size_2} ## f2:{field_2} ## s3:{size_3} ## f3:{field_3} ## s4:{size_4} ## f4:{field_4} ## s5:{size_5} ## f5:{field_5} ".format(
                size_1  = size_1,
                field_1 = field_1,
                size_2  = size_2,
                field_2 = field_2,
                size_3  = size_3,
                field_3 = field_3,
                size_4  = size_4,
                field_4 = field_4,
                size_5  = size_5,
                field_5 = field_5
            )

            holder.matchlevel_3_inner_convertable += 1

            print ('p11')

        except:
            groups_str = "Fields are not convertible"
            return(NOMATCH)

        print(groups_str)

        match_level_4(
            size_1  = size_1,
            field_1 = field_1,
            size_2  = size_2,
            field_2 = field_2,
            size_3  = size_3,
            field_3 = field_3,
            size_4  = size_4,
            field_4 = field_4,
            size_5  = size_5,
            field_5 = field_5,
            holder  = holder
        )


    return(1)





def match_level_1(in_bytes, holder):

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

        holder.matchlevel_1_outer += 1
        result = match_level_2_3(m.group(1), holder)


        match_level_1(in_bytes[m.span()[1]-5:], holder)




def process_whole_file(input_fn, output_fn):
    with open(input_fn, "rb") as in_file:
        in_bytes = in_file.read()

    holder = Holder()
    match_level_1(in_bytes, holder)

    print()
    print()
    print("matchlevel_1: " + str(holder.matchlevel_1_outer))
    print("matchlevel_2: " + str(holder.matchlevel_2_inner))
    print("matchlevel_3: " + str(holder.matchlevel_3_inner_convertable))
    print("matchlevel_4: " + str(holder.matchlevel_4_inner_field_sizes))
    
    print()
    print('Found the following entries:')
    pprint.pprint(holder.locals)

    with open(output_fn, "w") as out_file:
        holder.write_html(out_file)






##########
## main ##
##########

if __name__ == '__main__':
    print('p2')
    process_whole_file(INPUT_FN, OUTPUT_FN)
