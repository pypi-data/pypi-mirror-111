import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run trainer script, Select an experiment name and provide mu;tinode configs and needed')

    parser.add_argument("--exp", type=str, help="Name of experiment", required=True)

    parser.add_argument('--node-rank', type=int, default=None, help='Rank of the node', required=False)
    parser.add_argument('--num-nodes', type=int, default=None, help='Number of nodes', required=False)
    parser.add_argument('--master-addr', type=str, default=None, help='Master address', required=False)
    parser.add_argument('--master-port', type=int, default=None, help='Master port', required=False)

    return parser


def prepare_configs(args: argparse.Namespace):
    import trainify.configs as configs
    configs.init(args.exp)

    from trainify.configs import SystemConfig
    for key, value in vars(args).items():
        assert hasattr(SystemConfig, key), f'Internal error: parameter {key} not present in SystemConfig'
        if value is not None:
            SystemConfig.key = value


def train():
    parser = create_parser()
    args = parser.parse_args()
    prepare_configs(args)

    from .system.builder import Builder

    trainer = Builder().create_trainer()
    trainer.train()
