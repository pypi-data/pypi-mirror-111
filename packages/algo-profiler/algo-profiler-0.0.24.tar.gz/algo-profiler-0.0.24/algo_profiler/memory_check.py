import inspect
import tracemalloc
from textwrap import dedent

import matplotlib.pyplot as plt
import numpy as np
from memory_profiler import LineProfiler, memory_usage, show_results
from objsize import get_deep_size as get_size

from .big_o_analyzer import extend_analyse
from .helpers import LabelBase
from .linear_space import linear_space
from .printers import TablePrinterMixin


class TimerLabels(LabelBase):
    RUN_NUMBER = "Run number"
    RUN_ARGUMENT = "Function argument"
    RUN_ITERATIONS = "Function iterations"
    RUN_TIME = "Avg time (sec)"


class MemoryCheckResultFormatter(TablePrinterMixin):
    column_width = 23

    def __init__(self, runs_num):
        self.runs_num = runs_num
        self.results = []
        self.print_headers()

    def print_headers(self):
        column_names = [
            TimerLabels.RUN_NUMBER,
            TimerLabels.RUN_ARGUMENT,
            "Kwargs",
            "Function",
            "Total",
        ]
        self.print_row(columns=column_names, column_width=self.column_width)

    def append(self, run_idnex, run_arg, kwargs_size, func_usage, total_usage):

        self.results.append(
            {
                "run_arg": run_arg,
                "kwargs_size": kwargs_size,
                "func_usage": func_usage,
                "total_usage": total_usage,
            }
        )

        counter = f"{run_idnex}/{self.runs_num}"
        columns_value = [counter, run_arg, kwargs_size, func_usage, total_usage]
        self.print_row(columns=columns_value, column_width=self.column_width)

        if run_idnex == self.runs_num:
            print("")

    def render_base_chart(self):
        plt.title("Memory usage")
        plt.xlabel("Data generator's argument")
        plt.ylabel("Memory [MB]")

        args = [result["run_arg"] for result in self.results]
        kwarg_sizes = [result["kwargs_size"] for result in self.results]
        func_mem_usage = [result["func_usage"] for result in self.results]
        total_mem_usage = [result["total_usage"] for result in self.results]

        plt.plot(args, kwarg_sizes, label="kwargs size")
        plt.plot(args, func_mem_usage, label="function mem usage")
        plt.plot(args, total_mem_usage, label="total mem usage")

    def render_extended_chart(self):
        args = [result["run_arg"] for result in self.results]
        total_mem_usage = [result["total_usage"] for result in self.results]
        extend_analyse(args=args, vals=total_mem_usage, plt=plt)

    def display_chart(self):
        plt.legend()
        plt.show()


class MemoryCheck:
    def __init__(self):
        self.helper_funcs = {}

    def clean_result(self, profiler):
        code_map = profiler.code_map
        usage_by_lines = list(code_map.values())[0]
        initial_usage = list(usage_by_lines.values())[0][1]

        for code_obj_key, code_lines in dict(code_map).items():
            if len(code_map[code_obj_key]) == 0:
                continue

            first_line_usage_key = list(code_map[code_obj_key].keys())[0]
            _, usage, occurences = code_map[code_obj_key][first_line_usage_key]
            code_map[code_obj_key][first_line_usage_key] = (0.0, usage, occurences)

            for line_key, line_usage in code_lines.items():
                increment, usage, occurences = line_usage
                usage -= initial_usage
                code_map[code_obj_key][line_key] = (increment, usage, occurences)

    def get_kwargs_size(self, kwargs):
        return round(get_size(kwargs) / 1048576, 4)

    def extract_result_from_profiler(self, profiler):
        usage_by_lines = list(profiler.code_map.values())[0]
        usage_on_start = list(usage_by_lines.values())[0][1]
        usage_on_start = round(usage_on_start, 4)
        usage_on_end = list(usage_by_lines.values())[-1][1]
        usage_on_end = round(usage_on_end, 4)

        return usage_on_end - usage_on_start, usage_on_end

    def get_mem_usage(self, func, kwargs):
        tracemalloc.clear_traces()
        tracemalloc.start()
        func(**kwargs)
        _, peak_usage_B = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        kwargs_size = self.get_kwargs_size(kwargs)
        peak_usage_MB = round(peak_usage_B / 1048576, 4)
        total_usage = round(kwargs_size + peak_usage_MB, 4)

        return kwargs_size, peak_usage_MB, total_usage

    def print_summary(self, kwargs_size, func_usage, total_usage):
        summary = dedent(
            f"""\
        Kwargs size: {kwargs_size} MiB
        Function usage: {func_usage} MiB

        Total usage: {total_usage} MiB
        """
        )

        print(summary)

    def run_memory_check(self, func, kwargs):
        kwargs_size, func_usage, total_usage = self.get_mem_usage(
            func=func, kwargs=kwargs
        )
        self.print_summary(
            kwargs_size=kwargs_size, func_usage=func_usage, total_usage=total_usage
        )

    def run_memory_profiler(self, func, kwargs, clean_result=False):
        self.helper_funcs = {}
        func_module = inspect.getmodule(func)
        funcs = inspect.getmembers(func_module, inspect.isfunction)
        profiler = LineProfiler()
        wrapper = profiler(func)

        for func_name, func_instance in funcs:
            if func_name == func.__name__:
                continue

            profiler.code_map.add(func_instance.__code__)

        wrapper(**kwargs)

        kwargs_size = self.get_kwargs_size(kwargs)
        func_usage, total_usage = self.extract_result_from_profiler(profiler)

        if clean_result:
            self.clean_result(profiler)

        show_results(profiler, precision=4)

        self.print_summary(
            kwargs_size=kwargs_size, func_usage=func_usage, total_usage=total_usage
        )

    def run_time_based_memory_usage(self, func, kwargs, interval=0.1):
        import time

        start_time = time.time()
        mem_usage = memory_usage((func, (), kwargs), interval=interval)
        end_time = time.time()

        total_time = end_time - start_time
        real_interval = total_time / len(mem_usage)
        time = np.linspace(0, len(mem_usage) * real_interval, len(mem_usage))
        title = dedent(
            f"""\
        TIME BASED MEMORY USAGE
        Interval: given - {interval} sec, measured - {round(real_interval, 4)} sec"""
        )

        plt.title(title)
        plt.xlabel("Time [s]")
        plt.ylabel("Memory usage [MB]")

        plt.plot(time, mem_usage)
        plt.show()

    def run_memory_analysis(
        self,
        func,
        data_gen,
        gen_min_arg,
        gen_max_arg,
        gen_steps,
        draw_chart=False,
        find_big_o=False,
    ):
        args = linear_space(
            min_val=gen_min_arg, max_val=gen_max_arg, steps_num=gen_steps
        )
        result_formatter = MemoryCheckResultFormatter(runs_num=len(args))

        for index, arg in enumerate(args):
            kwargs = data_gen(arg)
            kwargs_size, func_usage, total_usage = self.get_mem_usage(
                func=func, kwargs=kwargs
            )

            result_formatter.append(
                run_idnex=index + 1,
                run_arg=arg,
                kwargs_size=kwargs_size,
                func_usage=func_usage,
                total_usage=total_usage,
            )

        if find_big_o:
            result_formatter.render_base_chart()
            result_formatter.render_extended_chart()
            result_formatter.display_chart()
        elif draw_chart:
            result_formatter.render_base_chart()
            result_formatter.display_chart()
