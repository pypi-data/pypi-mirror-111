import cProfile
import os
import sys

from snakeviz.cli import main as snakeviz


def run_snakeviz_server(func, kwargs):
    output_file = os.path.join(os.path.dirname(__file__), "temp_files", "snakeviz.prof")
    cProfile.runctx("func(**kwargs)", globals(), locals(), filename=output_file)
    sys.argv.append(output_file)
    snakeviz()
    os.remove(output_file)
