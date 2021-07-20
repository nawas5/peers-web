from tkinter import Tk
from tkinter.filedialog import askopenfilename
import clelib as cl
import datetime
import numpy as np
from config import Config
from message import Message


# browsing log file in explorer and opening it
Tk().withdraw()
filename = askopenfilename()
f = open(filename, 'r')

# load settings
config = Config()


#processing
for line in f:
    mes = Message(line)
    if mes.state > 0:
        if mes.type == "NM":
            cl.process_NM(mes, config)
        if mes.type == "CS_TX" or mes.type == "CS_RX":
            cl.process_CS(mes, config)
        if mes.type == "BLINK":
            cl.process_BLINK(mes, config)

# closing files
f.close()
config.f.close()
for tag in config.tags:
    tag.file.close()