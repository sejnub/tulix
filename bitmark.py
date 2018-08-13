import pprint
import html
import re


###############
## constants ##
###############

CURRENT_DIR = '<to be implemented>'
INPUT_FN    = 'src/kopie_von_t59_####_hunte37_via_raspi-docker-02.tlp'
OUTPUT_FN   = 'out.html'

OK          = 'ok'
ERROR       = 'error'
MATCH       = 'did_match'
NOMATCH     = 'did_not_match'


#############
## helpers ##
#############


###############
## functions ##
###############

class Holder:
    tunnels_all                    = []
    
    matchlevel_1_outer             = 0
    matchlevel_2_inner             = 0
    matchlevel_3_inner_convertable = 0
    matchlevel_4_inner_field_sizes = 0

    # Returns all link_entries
    def get_links(self, local_or_remote):
        pass

    def str_tunnels_all(self):
        ret_value = ''
        for tunnel in self.tunnels_all:
            ret_value += str(tunnel) + '\n'
        return(ret_value)

    def html_test_tunnels_all(self, local:bool):
        ret_value = ''
        for tunnel in self.tunnels_all:
            ret_value += tunnel.get_html(local) + '\n'
        return(ret_value)


    def write_html(self, out_file):
        out_str = pprint.pformat(self)
        out_file.write(out_str)


class Tunnel():
    f_s_listen_if   = 0            
    f_s_listen_port = 0            
    f_s_dest_host   = 0          
    f_s_dest_port   = 0          
    f_s_comment     = 0        

    f_v_listen_if   = ''          
    f_v_listen_port = 0            
    f_v_dest_host   = ''          
    f_v_dest_port   = 0          
    f_v_comment     = ''        

    def __str__(self):
        return(str(self.f_v_listen_port) + ' | ' + self.f_v_comment)

    def get_html(self, local:bool):
        return(
            self.get_link(local).get_html()
        )

    def get_link(self, local:bool):

        def local_link(self):
            return(Link(
                i_host    = self.f_v_listen_if, 
                i_port    = self.f_v_listen_port, 
                i_comment = self.f_v_comment)
            )

        def remote_link(self):
            return(Link(
                i_host    = self.f_v_dest_host, 
                i_port    = self.f_v_dest_port, 
                i_comment = self.f_v_comment)
            )

        return local_link(self) if local else remote_link(self)


class Link:
    host    = ''      
    port    = 0
    comment = ''      
    # TODO: See if there is a shorter syntax to set these values
    def __init__(self, i_host='', i_port=0, i_comment=''):
        self.host    = i_host
        self.port    = i_port
        self.comment = i_comment

    def get_html(self):
        #       <a href="https://www.w3schools.com">Visit W3Schools</a>
        html = '<a href="http://{host}:{port}">{comment}</a>'.format(
            host    = self.host,
            port    = self.port,
            comment = self.comment
        )    


def pf_match(match_object):
    try:
        match_info = ((
            "\n"                      + 
            "match_object: {pretty}"  +
            "\n"                      +
            "tunnel:        '{group}'" +
            "\n"                      +
            "span_hex:     ({start_hex}, {end_hex}), length_of_match: {length}\n" 

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


def match_level_0(input_fn, output_fn):

    try:
        with open(input_fn, "rb") as in_file:
            in_bytes = in_file.read()
    except:
        reason = 'L0: File read failed'
        print( ERROR, reason)
        return(ERROR, reason)

    value = 'L0: File read worked'
    print( OK, value)

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
    pprint.pprint(holder.html_test_tunnels_all(local=True))

    try:
        with open(output_fn, "w") as out_file:
            holder.write_html(out_file)
    except:
        reason = 'L0: File write failed'
        print( ERROR, reason)
        return(ERROR, reason)

    value = 'L0: File write worked'
    print( OK, value)

    ret_value = None

    value = 'L0: Everything worked'
    print( OK, value)
    return(OK, value)


def match_level_1(in_bytes, holder):

    print()
    print('################ match_level_1')
    print("Number of bytes to parse: {n}".format(n=len(in_bytes)))

    #p2 = re.compile(b'\01\00\00\00(.*?)((\01\00\00\00)|(\00\00\00\00\00\00\00\00\00))')
    #p2 = re.compile(b'\01\00\00\00(.*?)\01\00\00\00')
    p2 = re.compile(b'\01\00\00\00(.*?)((\01\00\00\00)|(\00\00\00\00\00\00\00\00\00))')
    m = p2.search(in_bytes)
    match_info = pf_match(m)
    print(match_info)

    if match_info == NOMATCH:
        reason = 'L1: No more tunnel found'
        print( ERROR, reason)
        return(ERROR, reason)

    value = 'L1: A tunnel was found'
    print( OK, value)

    holder.matchlevel_1_outer += 1
    match_level_2(m.group(1), holder)

    match_level_1(in_bytes[m.span()[1]-5:], holder)

    return(OK, value)


def match_level_2(matched_group, holder):

    p2 = re.compile(b'(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)$')
    m = p2.search(matched_group)
    match_info = pf_match(m)

    if match_info == NOMATCH:
        reason = 'L2: Tunnel does not have 5 fields'
        print( ERROR, reason)
        return(ERROR, reason)

    value = 'L2: Five fields were found'
    print( OK, value)

    holder.matchlevel_2_inner += 1

    match_level_3(m = m, holder = holder)

    return(OK, value)


def match_level_3(m, holder):

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
    except:
        reason = 'Fields are not convertible'
        print( ERROR, reason)
        return(ERROR, reason)

    value = 'L3: All fields could be converted'
    print( OK, value)

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
    print(groups_str)

    holder.matchlevel_3_inner_convertable += 1

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

    return(OK, value)


def match_level_4(size_1, field_1, size_2, field_2, size_3, field_3, size_4, field_4, size_5, field_5, holder):

    # f_s : field size
    # f_v : field value

    try:
        tunnel = Tunnel()
        tunnel.f_s_listen_if   = size_1
        tunnel.f_v_listen_if   = field_1
        tunnel.f_s_listen_port = size_2
        tunnel.f_v_listen_port = int(field_2)
        tunnel.f_s_dest_host   = size_3
        tunnel.f_v_dest_host   = field_3
        tunnel.f_s_dest_port   = size_4
        tunnel.f_v_dest_port   = int(field_4)
        tunnel.f_s_comment     = size_5
        tunnel.f_v_comment     = field_5

        if (
            tunnel.f_s_listen_if   < 3 or
            tunnel.f_s_listen_port < 1 or
            tunnel.f_s_listen_port > 6 or
            tunnel.f_s_dest_host   < 3 or
            tunnel.f_s_dest_port   < 1 or
            tunnel.f_s_dest_port   > 6
        ):
            reason = 'L4: Field sizes are not plausible'
            print( ERROR, reason)
            return(ERROR, reason)
        else:
            holder.matchlevel_4_inner_field_sizes += 1
            value = 'L4: All fields sizes are plausible'
            print( OK, value)
    except:
        reason = 'L4: Exception was raised'
        print(ERROR, reason)
        return(ERROR, reason)

    match_level_5(tunnel, holder)

    return(OK, value)


def match_level_5(tunnel, holder):
    holder.tunnels_all.append(tunnel)
    value = 'L5: Tunnel was added to holder.tunnels_all'
    print( OK, value)

    # WIP:

    value = 'L5: Ended successfully'
    print( OK, value)
    return(OK, value)


##########
## main ##
##########

if __name__ == '__main__':
    print('p2')
    match_level_0(INPUT_FN, OUTPUT_FN)
