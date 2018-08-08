import pprint
import html
import re



###############
## constants ##
###############

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
    out_str = ((
        "########\n" + 
        "{pretty}\n" +
        "########\n" + 
        "span_hex: ({start_hex}, {end_hex})"        
        
        
        '').format(
            pretty    = pprint.pformat(match_object),
            start_hex = hex(match_object.span()[0]),
            end_hex   = hex(match_object.span()[1])
        ) 
    )
    return(out_str)

 
def parse_whole_string(in_bytes, holder):

    #print('\n############################## match1')
    #p1 = re.compile(b'\01\00\00\00[^\00]...')
    #m = p1.search(in_bytes)
    #print(pf_match(m))

    print('\n############################## match')

    print("Number of parsed bytes: {n}\n".format(n=in_bytes.length())
    p2 = re.compile(b'\01\00\00\00(.*?)\01\00\00\00')
    m = p2.search(in_bytes)
    print(pf_match(m))

    parse_whole_string(in_bytes[m.span()[1]:], holder)



    # WIP
    pass


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
