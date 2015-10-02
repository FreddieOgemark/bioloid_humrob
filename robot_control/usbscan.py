import subprocess


def scan_for_usb():
    command = ['ls', '/dev/']
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = p.communicate()
    
    devfiles = out.split()

    for df in devfiles:
        if df.find("cu.usbserial") != -1:
            return "/dev/" + df

    
if __name__ == "__main__":
    print scan_for_usb()
