from cotea.runner import runner
from cotea.arguments_maker import argument_maker
#from cotea.debug_utils import pretty_print_task
import pathlib
import yaml

def sort_dict_by_depth(d):
    def _sort_dict_by_depth(d):
        if isinstance(d, dict):
            children_depths = [(k, _sort_dict_by_depth(v)) for k, v in d.items()]
            return (
                max(depth for _, (depth, _) in children_depths) + 1,
                {k: v for k, (_, v) in sorted(children_depths, key=lambda t: t[1][0])}
            )
        return 0, d
    return _sort_dict_by_depth(d)[1]


inv_path = str(pathlib.Path(pathlib.Path.cwd(),'helloworld','inventory'))
playbook_path = str(pathlib.Path(pathlib.Path.cwd(),'helloworld','playbook.yml'))

am = argument_maker()
am.add_arg("-i", inv_path)

r = runner(playbook_path, am)

specific_play = "all"
specific_task = "s_task"
s_var_name = "s_var"

while r.has_next_play():
    current_play = r.get_cur_play_name()

    while r.has_next_task():
        next_task = r.get_next_task_name()
        if current_play == specific_play and next_task == specific_task:
            # getting variable at specific execution point
            s_var_value = r.get_variable(s_var_name)
        if current_play == specific_play and next_task == 'Example fail':
            r.add_var_as_extra_var('hellome', 'get nicked')
            print(yaml.dump(r.get_all_vars(), sort_keys=False))
            tasksy = r.get_all_facts()

        r.run_next_task()

r.finish_ansible()

if r.was_error():
    print("Ansible error was:", r.get_error_msg())