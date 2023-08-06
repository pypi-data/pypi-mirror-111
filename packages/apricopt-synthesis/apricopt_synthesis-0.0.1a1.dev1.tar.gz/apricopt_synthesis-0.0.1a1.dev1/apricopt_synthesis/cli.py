import argparse


def get_command_line_arguments():
    parser = argparse.ArgumentParser(description="Process Apricopt input")

    parser.add_argument('-y', '--yaml', '--config', type=str,
                        help="The path to the YAML file that defines the problem",
                        required=True)

    parser.add_argument('-t', '--task', type=str,
                        help="The task to perform. One of 'synthesis', 'evaluation' and 'prioritisation'",
                        required=True)

    parser.add_argument('-d', '--dump-twin', type=str, dest='dump_twin',
                        help="Path to save the entire Digital Twin.",
                        required=False)

    parser.add_argument('-v', '--verbosity', '--log', type=int, dest='verb',
                        help="Verbosity level of log",
                        required=False)

    parser.add_argument('-o', '--dump', '--output', type=str, dest='output',
                        help="Output path of synthesized therapy",
                        required=False)

    parser.add_argument('-p', '--patient', type=int, dest='pat_idx',
                        help="Index of real patient in population tsv",
                        required=False)


    parser.add_argument('-c', '--class', type=str, dest='class_info',
                        help="Comma-separated list of strings <parameter_id>:<interval_id>",
                        required=False)

    return parser.parse_args()


if __name__ == "__main__":
    task, yaml = get_command_line_arguments()
    print(f"Task: {task}")
    print(f"YAML configuration file: {yaml}")
