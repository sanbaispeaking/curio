# curio/activation.py
#
# Scheduler activations can be used to monitor and effect
# what happens during task execution in the kernel. They
# can be used to implement features such as task-local storage,
# tracers, debuggers, and other things.   This file merely
# defines the base class. 

from functools import wraps

class ActivationBase:
    
    def activate(self, kernel):
        '''
        Called each time the kernel sets up its environment and is ready to run.
        kernel is an instance of the kernel that's executing.
        '''
        pass

    def scheduled(self, task):
        '''
        Called before the execution of a task.
        '''
        pass

    def suspended(self, task, exc):
        '''
        Called after the task has suspended. exc is set to an exception if
        the task has terminated.
        '''
        pass

def trap_patch(kernel, trapno):
    '''
    Patch the in-kernel trap table.  This decorator is intended for
    use in scheduler activations.  Main use is in debuggers, tracers, etc.
    Usage looks like this:

    from .traps import Traps

    class Activation(ActivationBase):

        def activate(self, kernel):

            @trap_patch(kernel, Traps._some_trap)
            def new_some_trap(*args, trapfunc):
                 result = trapfunc(*args)     # Call original trap
                 return result

    You can die using this feature.  Tread lightly.
    '''
    orig_trap = kernel._traps[trapno]

    def decorate(func):
        @wraps(func)
        def wrapper(*args):
            return func(*args, trap=orig_trap)
        kernel._traps[trapno] = wrapper
        return wrapper
    return decorate

    
    
