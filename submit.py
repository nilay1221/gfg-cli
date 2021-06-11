import question as qst
import request
import config
import time
from rich.console import Console
from rich.status import Status


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
    if sub_json['view_mode'] == 'correct':
        console.print('Correct Answer :white_check_mark:')
        console.print('Execution Time: [bold]{}'.format(msg['execution_time']))
    elif sub_json['view_mode'] == 'wrong_p':
        console.print('Wrong answer :x:')
        console.print('Input\n{}'.format(msg['file_input']))
        console.print('Your Output\n{}'.format(msg['code_output']))
        console.print('Expected Output\n{}'.format(msg['file_output']))
    elif sub_json['view_mode'] == 'runtime':
        console.print('[bold red]Runtime Error :heavy_exclamation_mark:\n')
        console.print('{}'.format(msg['error']))


