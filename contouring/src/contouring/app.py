import logging
from contouring.datareader import Datareader
from contouring.parser import Parser

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
    logging.info('Started')
    parser = Parser()
    parser.list_contours_in_wfs("")
    logging.info('Finished')

if __name__ == '__main__':
    main()

# create a directory bin and put your executables there, if you have any.
# Don't give them a .py extension, even if they are Python source files.
# Don't put any code in them except an import of and call to a main function
# defined somewhere else in your projects. (Slight wrinkle: since on Windows,
# the interpreter is selected by the file extension, your Windows users
# actually do want the .py extension. So, when you package for Windows,
# you may want to add it. Unfortunately there's no easy distutils trick that
# I know of to automate this process. Considering that on POSIX the .py
# extension is a only a wart, whereas on Windows the lack is an actual bug,
# if your userbase includes Windows users, you may want to opt to just
# have the .py extension everywhere.)

# import asyncio
# import time

# async def count():
#     print("One")
#     await asyncio.sleep(1)
#     print("Two")

# async def main():
#     await asyncio.gather(count(), count(), count())

# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
#     import time
#     s = time.perf_counter()
#     asyncio.run(main())
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")


# 1.1.12.449.g4109e645
# 1.1.12.451.gdb77255f

