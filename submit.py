import question as qst
import request
import config
import time
from rich.console import Console
from rich.status import Status
from rich import print as rprint


console = Console()


def submit_code(question_id:str,code:str,language:str,status:Status=None):
    # start_time = time.time()
    question = qst.get_question(question_id)
    data = {'request_type':'solutionCheck','code':code,'language':language,'source':'https://practice.geeksforgeeks.org','track':""}
    cookies = config.get_cookies()
    submission_info = request.post('/problems/' + question_id + '/compile/',data=data,cookies=cookies).json()
    # print(submission_info)
    sub_id = submission_info['results']['submission_id']
    data = {'sub_id':sub_id,'sub_type':'solutionCheck'}
    time.sleep(1)
    for i in range(10):
            sub_req = request.post('/problems/submission/result/',data=data,cookies=cookies)
            sub_json = sub_req.json()
            if sub_json['status'] == 'SUCCESS':
                break
    # print(sub_json)
    msg = sub_json['message']
    if status:status.stop()
    sanitize = lambda x:x.replace('\r\n','\n')
    if sub_json['view_mode'] == 'correct':
        output_str = []
        output_str.append('Correct Answer :white_check_mark:')
        output_str.append('Execution Time: [bold]{}'.format(msg['execution_time']))
        rprint('\n'.join(output_str))
    elif sub_json['view_mode'] == 'wrong_p':
        output_str = []
        output_str.append('Wrong answer :x:\n')
        output_str.append('Input\n{}\n'.format(sanitize(msg['file_input'])))
        output_str.append('Your Output\n{}'.format(sanitize(msg['code_output'])))
        output_str.append('Expected Output\n{}'.format(sanitize(msg['file_output'])))
        rprint('\n'.join(output_str))
    elif sub_json['view_mode'] == 'runtime':
        output_str = []
        output_str.append('[bold red]Runtime Error :heavy_exclamation_mark:\n')
        output_str.append('{}'.format(sanitize(msg['error'])))
        rprint('\n'.join(output_str))


