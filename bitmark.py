import pprint
import html
import re
import os
import fnmatch
import textwrap

# TODO: Check which tlp files are opened and only process those tlp files!
# TODO: Open a browser with the produced link file!


###############
## constants ##
###############

START_FOLDER  = 'D:/hb-privat/reps/bitvise_to_bookmark'
START_FOLDER  = 'C:/hb-regime/3_configuration/remote-access'
START_FOLDER  = '.'


OUTPUT_FN     = 'bitmark.html'

RE_HTTPS = re.compile(r"(HTTPS)|(https)")
RE_HTTP  = re.compile(r"(HTTP)|(http)")
    
OK            = 'ok'
ERROR         = 'error'
MATCH         = 'did_match'
NOMATCH       = 'did_not_match'

HTML_TITLE    = 'Tunnel Links'
# See http://htmlshell.com/
HTML_SKELETON = textwrap.dedent("""\
    <!doctype html>
    <html lang="en">

    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>{title}</title>
    </head>

    <body>
        {body}
    </body>

    </html>
""")

#############
## helpers ##
#############

def indicates_https(comment):
    m = RE_HTTPS.search(comment)
    return(False if m == None else True)

def indicates_http(comment):
    if indicates_https(comment):
        return(False)
    else:
        m = RE_HTTP.search(comment)
        if m == None:
            return(False)
        else:
            return(True)

def indicates_http_or_https(comment):
    m = RE_HTTP.search(comment)
    if m == None:
        return(False)
    else:
        return(True)
    

###############
## functions ##
###############

class Tlp:

    def __init__(self) -> None:
        self.tunnels_all = []

        self.matchlevel_1_outer = 0
        self.matchlevel_2_inner = 0
        self.matchlevel_3_inner_convertable = 0
        self.matchlevel_4_inner_field_sizes = 0

        self.fn_full_path = ''
        self.fn_stripped = ''

    def html_test_tunnels_all(self, local: bool):
        ret_value = ''
        for tunnel in self.tunnels_all:
            ret_value += tunnel.get_html(local) + '<br/>\n'
        return (ret_value)


class Tunnel:

    def __init__(self) -> None:
        self.f_s_listen_if = 0
        self.f_s_listen_port = 0
        self.f_s_dest_host = 0
        self.f_s_dest_port = 0
        self.f_s_comment = 0

        self.f_v_listen_if = ''
        self.f_v_listen_port = 0
        self.f_v_dest_host = ''
        self.f_v_dest_port = 0
        self.f_v_comment = ''

    def __str__(self):
        return(str(self.f_v_listen_port) + ' | ' + self.f_v_comment)

    def get_html(self, local:bool):
        return(
            self.get_link(local).get_html()
        )

    def get_link(self, local:bool):

        def remote_link(self):
            # TODO: This is probably only necessary because of a routing error concerning 127.0.0.1
            host = "localhost" if self.f_v_listen_if == "127.0.0.1" else self.f_v_listen_if
            return(Link(
                i_host    = host,
                i_port    = self.f_v_listen_port,
                i_comment = self.f_v_comment)
            )

        def local_link(self):
            return(Link(
                i_host    = self.f_v_dest_host,
                i_port    = self.f_v_dest_port,
                i_comment = self.f_v_comment)
            )

        return local_link(self) if local else remote_link(self)


class Link:
    # TODO: Set URL path to the <value> of 'path=<value>' in the comment. 
    #       Comment example: "Livetracer path=livetracer-ui HTTP" 
    # TODO: See if there is a shorter syntax to set these values
    def __init__(self, i_host='', i_port=0, i_comment=''):
        if indicates_https(i_comment):
            # TODO: Are these self. correct or do they point to the class
            self.protocol = 'https'
        elif indicates_http(i_comment):
            self.protocol = 'http'
        else:
            self.protocol = 'other_protocol'
        self.host    = i_host
        self.port    = i_port
        self.comment = i_comment

    def get_html(self):
        html = '<a href="{protocol}://{host}:{port}">{comment}</a>'.format(
            protocol = self.protocol,
            host     = self.host,
            port     = self.port,
            comment  = self.comment
        )
        return(html)


def pf_match(match_object):
    try:
        match_info = ((
            "\n"                      +
            "match_object: {pretty}"  +
            "\n"                      +
            "tunnel:       '{group}'" +
            "\n"                      +
            "span_hex:     ({start_hex}, {end_hex}), length_of_match: {length}\n" +
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


def find_files(pattern, path):
    result = []
    for root, _, files in os.walk(path):
        print('# ' + root)
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def match_level_5_contains_http(tunnel, tlp):

    if indicates_http_or_https(tunnel.f_v_comment):
        tlp.tunnels_all.append(tunnel)
        value = 'L5: Tunnel was added to tlp.tunnels_all'
        print( OK, value)
    else: 
        value = 'L5: Tunnel was not added because of missing hint for HTTP(S) in the comment.'
        print( OK, value)

    value = 'L5: Ended successfully'
    print( OK, value)
    return(OK, value)


def match_level_4(size_1, field_1, size_2, field_2, size_3, field_3, size_4, field_4, size_5, field_5, tlp):

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
        print('\np1 Comment:', tunnel.f_v_comment, '\n')

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
            tlp.matchlevel_4_inner_field_sizes += 1
            value = 'L4: All fields sizes are plausible'
            print( OK, value)
    except:
        reason = 'L4: Exception was raised'
        print(ERROR, reason)
        return(ERROR, reason)

    match_level_5_contains_http(tunnel, tlp)

    return(OK, value)


def match_level_3(m, tlp):

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

    tlp.matchlevel_3_inner_convertable += 1

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
        tlp  = tlp
    )

    return(OK, value)


def match_level_2(matched_group, tlp):

    p2 = re.compile(b'(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)\00\00\00(.)([^\00]*)$')
    m = p2.search(matched_group)
    match_info = pf_match(m)

    if match_info == NOMATCH:
        reason = 'L2: Tunnel does not have 5 fields'
        print( ERROR, reason)
        return(ERROR, reason)

    value = 'L2: Five fields were found'
    print( OK, value)

    tlp.matchlevel_2_inner += 1

    match_level_3(m = m, tlp = tlp)

    return(OK, value)


def match_level_1(in_bytes, tlp):

    print()
    print('################ match_level_1')
    print("Number of bytes to parse: {n}".format(n=len(in_bytes)))

    #p2 = re.compile(b'\01\00\00\00(.*?)((\01\00\00\00)|(\00\00\00\00\00\00\00\00\00))')
    #p2 = re.compile(b'\01\00\00\00(.*?)\01\00\00\00')
    p2 = re.compile(b'\01\00\00\00(.*?)((\01\00\00\00)|(\00\00\00\00\00\00\00\00\00))')
    m = p2.search(in_bytes)
    match_info = pf_match(m)
    #print(match_info)

    if match_info == NOMATCH:
        reason = 'L1: No more tunnel found'
        print( ERROR, reason)
        return(ERROR, reason)

    value = 'L1: A tunnel was found'
    print( OK, value)

    tlp.matchlevel_1_outer += 1
    match_level_2(m.group(1), tlp)

    match_level_1(in_bytes[m.span()[1]-5:], tlp)

    return(OK, value)


def fn_to_tlp(input_fn):

    try:
        with open(input_fn, "rb") as in_file:
            in_bytes = in_file.read()
    except:
        reason = 'L0: File read failed'
        print( ERROR, reason)
        return(ERROR, reason)

    print()
    print()
    print('################################')
    print('################################')
    value = 'L0: File read worked'
    print( OK, value)

    tlp = Tlp()

    #p2 = re.compile(b'\01\00\00\00(.*?)((\01\00\00\00)|(\00\00\00\00\00\00\00\00\00))')
    #m = p2.search(in_bytes)
    try:
        m = re.search(r"([^/]*)\.tlp$", input_fn)
        tlp.fn_stripped  = m.group(1)
        tlp.fn_full_path = input_fn
    except:
        reason = 'L0: Filename extraction failed'
        print( ERROR, reason)
        return(ERROR, reason)

    match_level_1(in_bytes, tlp)

    print()
    print()
    print("matchlevel_1: " + str(tlp.matchlevel_1_outer))
    print("matchlevel_2: " + str(tlp.matchlevel_2_inner))
    print("matchlevel_3: " + str(tlp.matchlevel_3_inner_convertable))
    print("matchlevel_4: " + str(tlp.matchlevel_4_inner_field_sizes))
    print()
    print('Found the following entries:')
    print("Stripped fn: '{}'\nFull fn:     '{}'".format(tlp.fn_stripped, tlp.fn_full_path))
    pprint.pprint(tlp.html_test_tunnels_all(local=True))

    # TODO: Add logger module
    value = 'L0: File write worked'
    print( OK, value)

    value = 'L0: Everything worked'
    print( OK, value)
    return(OK, tlp)


def get_all_tlp(start_folder):

    tlp_fns = find_files('*.tlp', start_folder)
    pprint.pprint(tlp_fns)

    list_of_tlps = []
    for fn in tlp_fns:
        _, tlp = fn_to_tlp(fn)
        list_of_tlps.append(tlp)
        pass

    return(OK, list_of_tlps)


def get_html(start_folder):
    
    _, tlps = get_all_tlp(start_folder)
    
    body = ''
    for tlp in tlps:
        # TODO: make concatenations more efficient
        local_tunnels_html  = tlp.html_test_tunnels_all(local=True)
        remote_tunnels_html = tlp.html_test_tunnels_all(local=False)

        if local_tunnels_html != '' or remote_tunnels_html != '':
            body += "<h2>{tlp_name}</h2>\n".format(tlp_name=tlp.fn_stripped)
        if local_tunnels_html != '':
            body += "<h3>Local</h3>\n"
            body += local_tunnels_html
        if local_tunnels_html != '':
            body += "<h3>Remote</h3>\n"
            body += remote_tunnels_html

    title = HTML_TITLE
    html = HTML_SKELETON.format(title=title, body=body)
    return(OK, html)


def html_to_file(start_folder, output_fn):
    _, html = get_html(start_folder)

    try:
       with open(output_fn, "w") as out_file:
           out_file.write(html)
    except: # TODO: In all except clauses: Only catch the relevant exceptions!
       reason = 'get_html: File write failed'
       print( ERROR, reason)
       return(ERROR, reason)

    value = 'html is written to file'
    print(OK, value)

    return(OK, value)

def all():
    html_to_file(START_FOLDER, OUTPUT_FN)



##########
## main ##
##########

if __name__ == '__main__':
    print('p2')
    all()


# eof