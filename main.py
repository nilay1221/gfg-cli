import question as qst
import argparse



class GFG:

    def __init__(self):
        parser = argparse.ArgumentParser(description='GFG CLI')
        sub_parser = parser.add_subparsers()


        # Parser For get
        parser_get = sub_parser.add_parser('get',help='Get the problem')
        parser_get.add_argument('-c',type=str,help="Problem Code",required=True)
        parser_get.add_argument('-l',type=str,default='cpp',help="Language for the problem",choices=['cpp','java','python'])
        parser_get.set_defaults(func=self.get)

        parser_test = sub_parser.add_parser('test',help='Test the code')
        parser_test.add_argument('-i',type=str,help='Input file to test',required=True)

        args = parser.parse_args()
        args.func(args)


    def _get_extension(self,language:str) -> str:
        language_extension = {
                'cpp':'cpp',
                'java':'java',
                'python':'py'
        }
        return language_extension[language]


    def get(self,args):
        question_id = args.c
        language = args.l
        question = qst.get_question(question_id)
        ext = '.' + self._get_extension(language)
        file_name = question.question_id + ext
        with open(file_name,'w') as fs:
            fs.write(question.get_intial_code(language=language))
        print("Created file {}".format(file_name))


if __name__ == '__main__':
    GFG()





