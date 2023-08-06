from nimutool.canbus import *
from nimutool.data import *
from nimutool.message_processor import *
import threading
from pathlib import Path


class NimuReader:

    def __init__(self, bus, traffic_study_period=0.5):
        self.bus = bus
        processor = NimuMessageProcessor()
        self.synchronizer = BusSynchronizer(traffic_study_period, processor)

    def __iter__(self):
        return self

    def __next__(self) -> ProcessedCanDataBlock:
        for msg in self.bus:
            processed_block = self.synchronizer.synchronize(msg)
            if processed_block:
                return processed_block


def read_bus(bus, nimu_file, pi_file, extras=False, nimu_protocol=2, traffic_study_period=0.5):
    niwriter = CsvWriter(nimu_file)
    piwriter = CsvWriter(pi_file)
    niprocessor = NimuMessageProcessorOld() if nimu_protocol == 1 else NimuMessageProcessor()
    piprocessor = PIMessageProcessor()
    nisynchronizer = BusSynchronizer(traffic_study_period, niprocessor)
    pisynchronizer = BusSynchronizer(traffic_study_period, piprocessor, True)
    next_trace = 0
    for msg in bus:
        block = nisynchronizer.synchronize(msg)
        if block: niwriter.write(block)
        block = pisynchronizer.synchronize(msg)
        if block: piwriter.write(block)

        if next_trace < msg.timestamp:
            print(f'NI: {nisynchronizer} PI: {pisynchronizer}')
            next_trace = msg.timestamp + 1
            if extras:
                ConsoleWriter.write(block)
        yield msg
    if nisynchronizer.collection_monitor.count != 0:
        print(f'Written {nisynchronizer.collection_monitor.count} rows to {nimu_file}')
    if pisynchronizer.collection_monitor.count != 0:
        print(f'Written {pisynchronizer.collection_monitor.count} rows to {pi_file}')


class BusReader(threading.Thread):

    def __init__(self, path: Path, file_prefix: str):
        super().__init__()
        self.running = True
        self.nifile = path / Path(f'{file_prefix}_ni_data.csv')
        self.pifile = path / Path(f'{file_prefix}_pi_data.csv')
        self.bus = None

    def run(self):
        self.bus = CanBusReader(can.interface.Bus(bustype='pcan', bitrate=1000000))
        for _ in read_bus(self.bus, self.nifile, self.pifile):
            if not self.running:
                break

    def stop(self):
        self.running = False
        self.join()
        if self.bus:
            self.bus.stop()