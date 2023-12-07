class BurmeseEmbeds:

    TITLE = 'Burmese SSH Brute Successful'

    DESCRIPTION = 'Target IP : ``{}``\nTarget Port : ``{}``\nName : ``{}``\nPassword : ``{}``\nAttempts : ``{}``\nElapsed Time : ``{}``'

    COLOR = 0x6e34eb

    @staticmethod

    def get_embed(ip , port , username , password , attempts , elapsed):

        burmese_embed = {

            'title' : BurmeseEmbeds.TITLE,

            'description' : BurmeseEmbeds.DESCRIPTION.format(ip , port , username , password , attempts , elapsed),

            'color' : BurmeseEmbeds.COLOR
        }



        return {
            'embeds' : [burmese_embed]
        }



