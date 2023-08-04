import subprocess
import os
import signal
import tempfile
import time
to_fill = {
        "WIDTH": None,
        "HEIGHT": None,
        "K1": None,
        "K2": None,
        "K3": None,
        "K4": None,
        "D1": None,
        "D2": None,
        "D3": None,
        "D4": None
        }
names = ["calibration_for_svo.yaml", "calibration_for_kalibr.yaml"]
def main():
    for name in names:
        try:
            os.remove(name)
        except:
            pass
    proc = subprocess.Popen(['/bin/bash','utils.sh']) #,stdout=subprocess.PIPE)
    pid = proc.pid
    print("PID:", pid)
    prompt = input("Hit enter once you finish calibrating")
    os.kill(pid + 1, signal.SIGINT) # not neccesarily deterministic
    time.sleep(1)
    os.kill(pid, signal.SIGINT)
    with open("output.txt", "r") as f:
        wflag = False
        hflag = False
        for line in f:
            print(line)
            if  "D = [" in line:
                dists = line[5:-1].split(", ")
                for i in range(1,5):
                    to_fill[f"D{i}"] = dists[i - 1]
            if "K = [" in line:
                calibs = line[5:-1].split(", ")
                i = 1
                while i < 5:
                    if calibs[i - 1] == "0.0" or calibs[i - 1] == "1.0":
                        i -= 1
                        calibs.pop(i)
                    else:
                        to_fill[f"K{i}"] = calibs[i - 1]
                    i += 1
            if wflag:
                to_fill["WIDTH"] = line
                wflag = False
            if hflag:
                to_fill["HEIGHT"] = line
                hflag = False
                break
            if "width" in line:
                wflag = True
            if "height" in line:
                hflag = True
        text = []
    for index in range(len(names)):
        with open(f"template{index}.yaml", 'r') as f:
            text = f.readlines()
        i = 0
        while i < len(text):
            line = text[i]
            if "TAG_" in line:
                bindex = line.index("TAG_") + 4
                eindex = line.index("_END")
                key = line[bindex : eindex]
                line = line.replace(f"TAG_{key}_END", to_fill[key])
                text[i] = line
                i -= 1
            i += 1
        with open(names[index], 'w') as f:
            f.writelines(text)
if __name__ == "__main__":
    main()
