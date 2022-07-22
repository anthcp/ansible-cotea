from cotea.runner import runner
from cotea.arguments_maker import argument_maker
import pathlib


inv_path = str(pathlib.Path(pathlib.Path.cwd(),'helloworld','inventory'))
playbook_path = str(pathlib.Path(pathlib.Path.cwd(),'helloworld','playbook.yml'))

am = argument_maker()
am.add_arg("-i", inv_path)

r = runner(playbook_path, am)

while r.has_next_play():
    current_play = r.get_cur_play_name()
    print("PLAY:", current_play)

    while r.has_next_task():
        next_task = r.get_next_task_name()
        print("\tTASK:", next_task)
            
        r.run_next_task()

r.finish_ansible()