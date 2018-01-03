import time
import os
import subprocess
import argparse


def wait_and_act(cmd, trigger_on_path, trigger_off_path, wait_time):
    proc = None
    try:
        while True:
            if (time.time()-os.path.getmtime(trigger_on_path)) < wait_time:
                if proc:
                    proc.poll()
                    if proc.returncode is None:
                        print('{} is already on!'.format(cmd))
                        time.sleep(wait_time)
                        continue
                proc = subprocess.Popen(cmd.split())
                print('{} turned on!'.format(cmd))
                time.sleep(wait_time)
            if (time.time()-os.path.getmtime(trigger_off_path)) < wait_time:
                if proc:
                    proc.poll()
                    if proc.returncode is None:
                        proc.terminate()
                        print('{} turned off!'.format(cmd))
                    else:
                        print('{} has already been turned off!'.format(cmd))
                else:
                    print('{} is not running!'.format(cmd))
                proc = None
                time.sleep(wait_time)
            time.sleep(1)
    except KeyboardInterrupt:
        print("W: interrupt received, stopping ...")
    finally:
        if proc:
            proc.kill()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')
    parser.add_argument('trigger_on')
    parser.add_argument('trigger_off')
    parser.add_argument('--wait', type=float, default=5.0)
    args = parser.parse_args()

    wait_and_act(args.cmd, args.trigger_on, args.trigger_off, args.wait)
