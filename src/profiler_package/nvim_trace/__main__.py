import sys
import argparse
import runpy
from tracer import Tracer

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Trace the execution of a Python script.")
    parser.add_argument('script', type=str, help='The Python script to execute and trace.')
    parser.add_argument('script_args', nargs=argparse.REMAINDER, help='Arguments to pass to the script.')
    
    args = parser.parse_args()
    script_path = args.script
    script_args = args.script_args
    sys.argv = [script_path] + script_args

    def run_script():
        runpy.run_path(script_path)

    Tracer().profile_code(run_script)

if __name__ == '__main__':
    main()
