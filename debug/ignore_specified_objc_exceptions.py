import lldb
import re
import shlex

# This script allows Xcode to selectively ignore Obj-C exceptions
# based on any selector on the NSException instance

def filterException(debugger, user_input, result, unused):
    thread = debugger.GetSelectedTarget().GetProcess().GetSelectedThread();
    frame = thread.GetFrameAtIndex(0)

    if frame.symbol.name != 'objc_exception_throw':
        # We can't handle anything except objc_exception_throw
        return None

    filters = shlex.split(user_input)
    name = thread.GetFrameAtIndex(1).symbol.name

    for filter in filters:
        className, method = filter.split(":", 1)

        match = re.search("{0} {1}".format(className, method), name)

        if match:
            exceptionFile = thread.GetFrameAtIndex(2).symbol.name
            output = "Skipping exception because exception is {0} in {1}".format(name, exceptionFile)
            result.PutCString(output)
            result.flush()
            # If we tell the debugger to continue before this script finishes,
            # Xcode gets into a weird state where it won't refuse to quit LLDB,
            # so we set async so the script terminates and hands control back to Xcode
            debugger.SetAsync(True)
            debugger.HandleCommand("continue")
            return None

    return None

def __lldb_init_module(debugger, unused):
    debugger.HandleCommand('command script add --function ignore_specified_objc_exceptions.filterException ignore_specified_objc_exceptions')