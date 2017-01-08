To build a new exe from the source file run_cmd_from_exe
run the following command:
python setup.py py2exe

IMPORTANT:
The whole idea of the source written inside of run_cmd_from_exe is to make it
so general that it does not need modifications. 
So as a rule of thumb no modifications should be needed, since all it does is to
run run_server.cmd over the parent directory. 
run_server.cmd on the other hand can be modified really easily and it is the idea to do so.