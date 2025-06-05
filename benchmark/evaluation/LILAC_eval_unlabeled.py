"""
This file is part of TA-Eval-Rep.
Copyright (C) 2022 University of Luxembourg
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import os

sys.path.append('../')

from logparser.LILAC import LogParser
from evaluation.settings import benchmark_settings
from evaluation.utils.common import common_args
from evaluation.utils.evaluator_main import evaluator, prepare_results
from evaluation.utils.postprocess import post_average


datasets_2k = [
    "Proxifier",
    "Linux",
    "Apache",
    "Zookeeper",
    "Hadoop",
    "HealthApp",
    "OpenStack",
    "HPC",
    "Mac",
    "OpenSSH",
    "Spark",
    "Thunderbird",
    "BGL",
    "HDFS",
]

datasets_full = [
    "Logs",
]


if __name__ == "__main__":
    args = common_args()
    data_type = "full" if args.full_data else "2k"
    input_dir = f"../../{data_type}_dataset/"
    output_dir = f"../../result/result_LILAC_{data_type}_{args.shot}_{args.example_size}_{args.model}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    result_file = prepare_results(
        output_dir=output_dir,
        otc=args.oracle_template_correction,
        complex=args.complex,
        frequent=args.frequent
    )

    if args.full_data:
        datasets = datasets_full
    else:
        datasets = datasets_2k
    for dataset in datasets:
        setting = benchmark_settings[dataset]
        log_file = setting['log_file'].replace("_2k", f"_{data_type}")
        indir = os.path.join(input_dir, os.path.dirname(log_file))
        if os.path.exists(os.path.join(output_dir, f"{dataset}_{data_type}.log_structured.csv")):
            parser = None
            print("parseing result exist.")
        else:
            parser = LogParser
        # run evaluator for a dataset
        evaluator(
            dataset=dataset,
            input_dir=input_dir,
            output_dir=output_dir,
            log_file=log_file,
            LogParser=parser,
            param_dict={
                # 'log_format': setting['log_format'], 'indir': indir, 'outdir': output_dir, 'rex': setting['regex'],
                'log_format': setting['log_format'], 'indir': indir, 'outdir': output_dir, 'rex': [],
                'data_type': data_type, 'shot': args.shot, 'example_size': args.example_size,
                'model': args.model, 'selection_method': args.selection_method,
            },
            otc=args.oracle_template_correction,
            complex=args.complex,
            frequent=args.frequent,
            result_file=result_file,
        )  # it internally saves the results into a summary file
    metric_file = os.path.join(output_dir, result_file)
    post_average(metric_file, f"LILAC_{data_type}_complex={args.complex}_frequent={args.frequent}_{args.shot}_{args.example_size}_{args.model}", args.complex, args.frequent)
