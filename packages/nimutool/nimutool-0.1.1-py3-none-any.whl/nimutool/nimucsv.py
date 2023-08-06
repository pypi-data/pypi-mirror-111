import argparse
from nimutool import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for reading nimu data from CAN bus')
    parser.add_argument('--trace-file', type=str, help='PCAN-View generated trace file')
    parser.add_argument('--hex2nimu', action='store_true', help='Convert PILogger can2hex output')
    parser.add_argument('--output', help='Output file name', default='ni_data.csv')
    parser.add_argument('--extras', action='store_true', help='Show some extra contents from CAN BUS')
    parser.add_argument('--can-adapter', default='pcan', help='Can adapter to use, see options from python-can documentation')
    parser.add_argument('--traffic-study-period', type=float, default=1.5, help='How long to study CAN bus traffic before starting logging')
    args = parser.parse_args()

    if args.hex2nimu:
        bus = PiLoggerCanBusReader()
    elif args.trace_file:
        bus = TraceFileCanBusReader(args.trace_file)
    else:
        bus = CanBusReader(can.interface.Bus(bustype=args.can_adapter, bitrate=1000000))
    writer = CsvWriter(args.output)
    for processed_block in NimuReader(bus, args.traffic_study_period):
        if processed_block is None:
            break
        writer.write(processed_block)
    print(f'{args.output} written')