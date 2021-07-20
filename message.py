class Message():

    def __init__(self, mes):
        self.mes = mes
        if mes.find("New Master") > 0:
            self.state = 1
            self.type = "NM"
            a = mes.split()
            self.Master = int(a[0][-1])
            self.Anchor = int(a[0][-3])
            self.Master_x = float(a[5][1:])
            self.Master_y = float(a[6])
            self.Master_z = float(a[7][:-1])
            self.Anchor_x = float(a[8][1:])
            self.Anchor_y = float(a[9])
            self.Anchor_z = float(a[10][:-1])
            self.R = float(a[14])
        elif mes.find("CS_TX") > 0:
            self.state = 1
            self.type = "CS_TX"
            a = mes.split()
            self.Anchor = int(a[2][0:-1])
            self.Seq = int(a[4])
            self.TimeStamp = float(a[6])
        elif mes.find("CS_RX") > 0:
            self.state = 1
            self.type = "CS_RX"
            a = mes.split()
            self.Anchor = int(a[3][0:-4])
            self.Seq = int(a[4])
            self.TimeStamp = float(a[6])
        elif mes.find("BLINK ") > 0:
            self.state = 1
            self.type = "BLINK"
            a = mes.split()
            self.ID = a[1]
            self.SN = int(a[3])
            self.Anchor = int(a[6])
            self.TimeStamp = float(a[8])
        else:
            self.state = 0