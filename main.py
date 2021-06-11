import question as qst
import argparse
import question_test
from pathlib import Path
import time
from rich.console import Console
import submit
import configparser
import os


console = Console()

class GFG:

    def __init__(self):
        parser = argparse.ArgumentParser(description='GFG CLI')
        sub_parser = parser.add_subparsers()


        # Parser For get
        parser_get = sub_parser.add_parser('get',help='Get the problem')
        parser_get.add_argument('-c',type=str,help="Problem Code",required=True)
        parser_get.add_argument('-l',type=str,default='cpp',help="Language for the problem",choices=['cpp','java','python'])
        parser_get.set_defaults(func=self.get)

        # Parser for Testing Code
        parser_test = sub_parser.add_parser('test',help='Test the code')
        parser_test.add_argument('file',type=argparse.FileType('r'),help='Input file to test')
        parser_test.add_argument('-c',type=str,help='Problem Code Default filename')
        parser_test.add_argument('-i',type=argparse.FileType('r'),help='Code Input Default Sample Input')
        parser_test.add_argument('-l',type=str,default='cpp',help="Language for the problem",choices=['cpp','java','python'])
        parser_test.set_defaults(func=self.test)

        # Parser for Submit Code
        parser_submit = sub_parser.add_parser('submit',help='Submit the Code')
        parser_submit.add_argument('file',type=argparse.FileType('r'),help='Input file to submit')
        parser_submit.add_argument('-c',type=str,help='Problem Code Default filename')
        parser_submit.add_argument('-l',type=str,default='cpp',help="Language for the problem",choices=['cpp','java','python'])
        parser_submit.set_defaults(func=self.submit)

        # Parser for Setting Config
        parser_config = sub_parser.add_parser('config',help='Set Config.json path')
        parser_config.add_argument('path',type=self._file_path,help='Path to config.json',metavar='File')
        parser_config.set_defaults(func=self.config)


        # Parser for showing the problem
        parser_show = sub_parser.add_parser('show',help='View problem')
        parser_show.add_argument('-c',type=str,help='Problem code',required=True)
        parser_show.set_defaults(func=self.show_problem)

    

        


        args = parser.parse_args()
        args.func(args)

    def _file_path(self,path:str) -> str:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path
        else:
            raise argparse.ArgumentError(message='File not found')


    def _get_extension(self,language:str) -> str:
        language_extension = {
                'cpp':'cpp',
                'java':'java',
                'python':'py'
        }
        return language_extension[language]


    def get(self,args) -> None:
        question_id = args.c
        language = args.l
        question = qst.get_question(question_id)
        ext = '.' + self._get_extension(language)
        file_name = question.question_id + ext
        with open(file_name,'w') as fs:
            code = question.get_intial_code(language=language).replace('\r\n','\n')
            fs.write(code)
        print("Created file {}".format(file_name))

    def submit(self,args) -> None:
        question_id = args.c if args.c else Path(args.file.name).stem
        code = args.file.read()
        with console.status('Loading...',spinner='line') as status:
            submit.submit_code(question_id,code,args.l,status)


    def test(self,args) -> None:
        question_id = args.c if args.c else Path(args.file.name).stem
        # print(question_id)
        code = args.file.read()
        inp = args.i.read() if args.i else None
        with console.status('Loading...',spinner='line') as status:
            question_test.test_code(question_id,code,language=args.l,inp=inp,status=status)

    def config(self,args) -> None:
        file = args.path
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'config_path':file}
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname,'config.ini'),'w') as configfile:
            config.write(configfile)

    def show_problem(self,args) -> None:
        question_id = args.c
        with console.status('Loading...',spinner='line') as status:
            qst.show_question(question_id,status)




if __name__ == '__main__':
    GFG()





