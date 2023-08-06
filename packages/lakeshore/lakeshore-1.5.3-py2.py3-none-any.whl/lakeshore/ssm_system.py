"""Implements functionality unique to the Lake Shore M81."""

import struct
from base64 import b64decode
from threading import Lock

from lakeshore.xip_instrument import XIPInstrument, XIPInstrumentException, RegisterBase
from lakeshore.ssm_measure_module import MeasureModule
from lakeshore.ssm_source_module import SourceModule
from lakeshore.ssm_settings_profiles import SettingsProfiles

try:
    from wakepy import keepawake
except NotImplementedError:
    pass  # Proceed without wakepy on linux without systemd


class SSMSystemOperationRegister(RegisterBase):
    """Class object representing the operation status register"""

    bit_names = [
        "s1_summary",
        "s2_summary",
        "s3_summary",
        "m1_summary",
        "m2_summary",
        "m3_summary",
        "data_stream_in_progress"
    ]

    def __init__(self,
                 s1_summary,
                 s2_summary,
                 s3_summary,
                 m1_summary,
                 m2_summary,
                 m3_summary,
                 data_stream_in_progress):
        self.s1_summary = s1_summary
        self.s2_summary = s2_summary
        self.s3_summary = s3_summary
        self.m1_summary = m1_summary
        self.m2_summary = m2_summary
        self.m3_summary = m3_summary
        self.data_stream_in_progress = data_stream_in_progress


class SSMSystemQuestionableRegister(RegisterBase):
    """Class object representing the questionable status register"""

    bit_names = [
        "s1_summary",
        "s2_summary",
        "s3_summary",
        "m1_summary",
        "m2_summary",
        "m3_summary",
        "critical_startup_error",
        "critical_runtime_error",
        "heartbeat",
        "calibration",
        "data_stream_overflow"
    ]

    # pylint: disable=too-many-arguments
    def __init__(self,
                 s1_summary,
                 s2_summary,
                 s3_summary,
                 m1_summary,
                 m2_summary,
                 m3_summary,
                 critical_startup_error,
                 critical_runtime_error,
                 heartbeat,
                 calibration,
                 data_stream_overflow):
        self.s1_summary = s1_summary
        self.s2_summary = s2_summary
        self.s3_summary = s3_summary
        self.m1_summary = m1_summary
        self.m2_summary = m2_summary
        self.m3_summary = m3_summary
        self.critical_startup_error = critical_startup_error
        self.critical_runtime_error = critical_runtime_error
        self.heartbeat = heartbeat
        self.calibration = calibration
        self.data_stream_overflow = data_stream_overflow


class SSMSystem(XIPInstrument):
    """Class for interaction with the M81 instrument"""

    vid_pid = [(0x1FB9, 0x0704), (0x10C4, 0xEA60)]

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=921600,
                 flow_control=True,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to SSM
        XIPInstrument.__init__(self,
                               serial_number,
                               com_port,
                               baud_rate,
                               flow_control,
                               timeout,
                               ip_address,
                               tcp_port,
                               **kwargs)

        self.operation_register = SSMSystemOperationRegister
        self.questionable_register = SSMSystemQuestionableRegister

        # Instantiate modules
        self.source_modules = [SourceModule(i + 1, self) for i in range(self.get_num_source_channels())]
        self.measure_modules = [MeasureModule(i + 1, self) for i in range(self.get_num_measure_channels())]

        self.settings_profiles = SettingsProfiles(self)

        self.stream_lock = Lock()

    def get_num_measure_channels(self):
        """Returns the number of measure channels supported by the instrument"""

        return int(self.query('SENSe:NCHannels?'))

    def get_num_source_channels(self):
        """Returns the number of source channels supported by the instrument"""

        return int(self.query('SOURce:NCHannels?'))

    def get_source_module(self, port_number):
        """Returns a SourceModule instance for the given port number"""

        try:
            return self.source_modules[port_number - 1]
        except IndexError:
            raise IndexError(
                'Invalid port number. Must be between 1 and {}'.format(self.get_num_source_channels())) from None

    def get_source_pod(self, port_number):
        """alias of get_source_module"""
        return self.get_source_module(port_number)

    def get_source_module_by_name(self, module_name):
        """Return the SourceModule instance that matches the specified name"""

        return self._locate_module_by_name(module_name, self.source_modules)

    def get_measure_module(self, port_number):
        """Returns a MeasureModule instance for the given port number"""

        try:
            return self.measure_modules[port_number - 1]
        except IndexError:
            raise IndexError(
                'Invalid port number. Must be between 1 and {}'.format(self.get_num_measure_channels())) from None

    def get_measure_pod(self, port_number):
        """alias of get_measure_module"""
        return self.get_measure_module(port_number)

    def get_measure_module_by_name(self, module_name):
        """Return the MeasureModule instance that matches the specified name"""

        return self._locate_module_by_name(module_name, self.measure_modules)

    @staticmethod
    def _locate_module_by_name(module_name, set_of_modules):
        module_names = []
        for module in set_of_modules:
            try:
                module_names.append(module.get_name())
            except XIPInstrumentException as exception:
                if '-241,"Hardware missing;' not in str(exception):
                    raise
                module_names.append(None)

        num_matches = len([name for name in module_names if name == module_name])

        if num_matches < 1:
            raise XIPInstrumentException('No module was found with the name {}.'.format(module_name))
        if num_matches > 1:
            raise XIPInstrumentException('Module name conflict: more than one module is named {}.'.format(module_name))

        return set_of_modules[module_names.index(module_name)]

    data_source_types = {
        'RTIMe': float,
        'SAMPlitude': float,
        'SOFFset': float,
        'SFRequency': float,
        'SRANge': float,
        'SVLimit': lambda s: bool(int(s)),
        'SILimit': lambda s: bool(int(s)),
        'MDC': float,
        'MRMs': float,
        'MPPeak': float,
        'MNPeak': float,
        'MPTPeak': float,
        'MX': float,
        'MY': float,
        'MR': float,
        'MTHeta': float,
        'MRANge': float,
        'MOVerload': lambda s: bool(int(s)),
        'MSETtling': lambda s: bool(int(s)),
        'MUNLock': lambda s: bool(int(s)),
        'MRFRequency': float,
        'GPIStates': int,
        'GPOStates': int,
    }

    data_source_lookup = {}
    for mnemonic, channel_index in data_source_types.items():
        short_form = ''.join(c for c in mnemonic if not c.islower())
        data_source_lookup[mnemonic.upper()] = channel_index
        data_source_lookup[short_form.upper()] = channel_index

    def get_multiple(self, *data_sources):
        """Gets a list of values corresponding to the input data sources.

            Args:
                data_sources (str, int): Variable length list of pairs of (DATASOURCE_MNEMONIC, CHANNEL_INDEX).

            Returns:
                Tuple of values corresponding to the given data sources
        """

        elements = ','.join('{},{}'.format(mnemonic, index) for (mnemonic, index) in data_sources)
        response_values_with_indices = enumerate(self.query('FETCh? {}'.format(elements)).split(','))

        return tuple(
            (self.data_source_lookup[data_sources[i][0].upper()])(value) for (i, value) in response_values_with_indices)

    def stream_data(self, rate, num_points, *data_sources):
        """Generator object to stream data from the instrument.

            Args:
                rate (int): Desired transfer rate in points/sec.
                num_points (int): Number of points to return. None to stream indefinitely.
                data_sources (str, int): Variable length list of pairs of (DATASOURCE_MNEMONIC, CHANNEL_INDEX).

            Yields:
                A single row of stream data as a tuple
        """

        with self.stream_lock:
            with keepawake(keep_screen_awake=True):
                self.command('TRACe:RESEt')
                self._configure_stream_elements(data_sources)
                self.command('TRACe:FORMat:ENCOding B64')
                self.command('TRACe:RATE {}'.format(rate))

                bytes_per_row = int(self.query('TRACe:FORMat:ENCOding:B64:BCOunt?'))
                binary_format = '<' + self.query('TRACe:FORMat:ENCOding:B64:BFORmat?').strip('\"')

                if num_points is not None:
                    self.command('TRACe:STARt {}'.format(num_points))
                else:
                    self.command('TRACe:STARt')

                num_collected = 0
                while num_points is None or num_collected < num_points:
                    b64_string = ''
                    while not b64_string:
                        b64_string = self.query('TRACe:DATA:ALL?', check_errors=False)

                    new_bytes = b64decode(b64_string)
                    rows = [new_bytes[i:i + bytes_per_row] for i in range(0, len(new_bytes), bytes_per_row)]

                    for row in rows:
                        data = struct.unpack(binary_format, row)
                        num_collected += 1

                        yield data

            overflow_occurred = bool(int(self.query('TRACe:DATA:OVERflow?', check_errors=True)))
            if overflow_occurred:
                raise XIPInstrumentException('Data loss occurred during this data stream.')

    def get_data(self, rate, num_points, *data_sources):
        """Like stream_data, but returns a list.

            Args:
                rate (int): Desired transfer rate in points/sec.
                num_points (int): Number of points to return.
                data_sources (str, int): Variable length list of pairs of (DATASOURCE_MNEMONIC, CHANNEL_INDEX).

            Returns:
                All available stream data as a list of tuples
        """

        return list(self.stream_data(rate, num_points, *data_sources))

    def log_data_to_csv_file(self, rate, num_points, file, *data_sources, **kwargs):
        """Like stream_data, but logs directly to a CSV file.

            Args:
                rate (int): Desired transfer rate in points/sec.
                file (IO): File to log to.
                num_points (int): Number of points to log.
                data_sources (str, int): Pairs of (DATASOURCE_MNEMONIC, CHANNEL_INDEX).
                write_header (bool): If true, a header row is written with column names.
        """
        write_header = kwargs.pop('write_header', True)

        if write_header:
            self._configure_stream_elements(data_sources)
            header = self.query('TRACe:FORMat:HEADer?').strip('\"')
            file.write(header + '\n')

        for row in self.stream_data(rate, num_points, *data_sources):
            file.write(','.join(str(x) for x in row) + '\n')

    def _configure_stream_elements(self, data_sources):
        elements = ','.join('{},{}'.format(mnemonic, index) for (mnemonic, index) in data_sources)
        self.command('TRACe:FORMat:ELEMents {}'.format(elements))

    def get_ref_in_edge(self):
        """Returns the active edge of the reference input. 'RISing' or 'FALLing'."""

        return self.query('INPut:REFerence:EDGe?')

    def set_ref_in_edge(self, edge):
        """Sets the active edge of the reference input

            Args:
                edge (str):
                    The new active edge ('RISing', or 'FALLing')
        """

        self.command('INPut:REFerence:EDGe {}'.format(edge))

    def get_ref_out_source(self):
        """Returns the channel used for the reference output. 'S1', 'S2', or 'S3'."""

        return self.query('OUTPut:REFerence:SOURce?')

    def set_ref_out_source(self, ref_out_source):
        """Sets the channel used for the reference output.

            Args:
                ref_out_source (str):
                    The new reference out source ('S1', 'S2', or 'S3')
        """

        self.command('OUTPut:REFerence:SOURce {}'.format(ref_out_source))

    def get_ref_out_state(self):
        """Returns the enable state of reference out"""

        return bool(int(self.query('OUTPut:REFerence:STATe?')))

    def set_ref_out_state(self, ref_out_state):
        """Sets the enable state of reference out

            Args:
                ref_out_state (bool):
                    The new reference out state (True to enable reference out, False to disable reference out)
        """

        self.command('OUTPut:REFerence:STATe {}'.format(str(int(ref_out_state))))

    def enable_ref_out(self):
        """Sets the enable state of reference out to True"""

        self.set_ref_out_state(True)

    def disable_ref_out(self):
        """Sets the enable state of reference out to False"""

        self.set_ref_out_state(False)

    def configure_ref_out(self, ref_out_source, ref_out_state=True):
        """Configure the reference output

            Args:
                ref_out_source (str):
                    The new reference out source ('S1', 'S2', or 'S3')

                ref_out_state (bool):
                    The new reference out state (True to enable reference out, False to disable reference out)
        """

        self.set_ref_out_source(ref_out_source)
        self.set_ref_out_state(ref_out_state)

    def get_mon_out_mode(self):
        """Returns the channel used for the monitor output. 'M1', 'M2', 'M3', or 'MANUAL'."""

        return self.query('OUTPut:MONitor:MODe?')

    def set_mon_out_mode(self, mon_out_source):
        """Sets the channel used for the monitor output.

            Args:
                mon_out_source (str):
                    The new monitor out source ('M1', 'M2', 'M3', or 'MANUAL')
        """

        self.command('OUTPut:MONitor:MODe {}'.format(mon_out_source))

    def get_mon_out_state(self):
        """Returns the enable state of monitor out"""

        return bool(int(self.query('OUTPut:MONitor:STATe?')))

    def set_mon_out_state(self, mon_out_state):
        """Sets the enable state of monitor out

            Args:
                mon_out_state (bool):
                    The new monitor out state (True to enable monitor out, False to disable monitor out)
        """

        self.command('OUTPut:MONitor:STATe {}'.format(str(int(mon_out_state))))

    def enable_mon_out(self):
        """Sets the enable state of monitor out to True"""

        self.set_mon_out_state(True)

    def disable_mon_out(self):
        """Sets the enable state of monitor out to False"""

        self.set_mon_out_state(False)

    def configure_mon_out(self, mon_out_source, mon_out_state=True):
        """Configure the monitor output

            Args:
                mon_out_source (str):
                    The new monitor out source ('M1', 'M2', or 'M3')

                mon_out_state (bool):
                    The new monitor out state (True to enable monitor out, False to disable monitor out)
        """

        self.set_mon_out_mode(mon_out_source)
        self.set_mon_out_state(mon_out_state)

    def get_head_self_cal_status(self):
        """Returns the status of the last head self calibration"""

        return self.query('CALibration:SCALibration:STATus?')

    def run_head_self_calibration(self):
        """"Runs a self calibration for the head"""

        self.command('CALibration:SCALibration:RUN')

    def reset_head_self_calibration(self):
        """"Restore the factory self calibration"""

        self.command('CALibration:SCALibration:RESet')

    def set_mon_out_manual_level(self, manual_level):
        """Set the manual level of monitor out when the mode is MANUAL

            Args:
                manual_level (float):
                    The new monitor out manual level
        """

        self.command('OUTPut:MONitor:MLEVel {}'.format(str(manual_level)))

    def get_mon_out_manual_level(self):
        """Returns the manual level of monitor out"""

        return float(self.query('OUTPut:MONitor:MLEVel?'))

    def configure_mon_out_manual_mode(self, manual_level, mon_out_state=True):
        """Configures the monitor output for manual mode

            Args:
                manual_level (float):
                    The new monitor out manual level

                mon_out_state (bool):
                    The new monitor out state (True to enable monitor out, False to disable monitor out)
        """

        self.set_mon_out_manual_level(manual_level)
        self.set_mon_out_mode('MANUAL')
        self.set_mon_out_state(mon_out_state)
