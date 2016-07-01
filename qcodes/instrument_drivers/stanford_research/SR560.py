from qcodes import Instrument
from qcodes.instrument.parameter import ManualParameter
from qcodes.utils.validators import Bool, Numbers

from qcodes.instrument.parameter import Parameter


class VoltageParameter(Parameter):
    def __init__(self, measured_param, vamp_ins, name='volt'):
        p_name = measured_param.name
        self.name = name
        super().__init__(names=('vamp_raw_'+p_name, name))

        _p_label = None
        _p_unit = None

        self.measured_param = measured_param
        self._instrument = vamp_ins

        if hasattr(measured_param, 'label'):
            _p_label = measured_param.label
        if hasattr(measured_param, 'units'):
            _p_unit = measured_param.units

        self.labels = (_p_label, 'Voltage')
        self.units = (_p_unit, 'V')

    def get(self):
        volt = self.measured_param.get()
        volt_amp = (volt / self._instrument.gain.get())

        if self._instrument.invert.get():
            volt_amp *= -1
        return (volt, volt_amp)


class SR560(Instrument):
    """
    This is the qcodes driver for the SR 560 Voltage-preamplifier.

    This is a virtual driver only and will not talk to your instrument.
    """
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        # TODO: are these Numbers() OK?
        # Can we be more specific with the ranges?
        self.add_parameter('cutoff_lo',
                           parameter_class=ManualParameter,
                           initial_value='DC',
                           label='High pass',
                           units='Hz',
                           vals=Numbers(min_value=0))

        self.add_parameter('cutoff_hi',
                           parameter_class=ManualParameter,
                           initial_value='1e6',
                           label='Low pass',
                           units='Hz',
                           vals=Numbers(min_value=0))

        self.add_parameter('invert',
                           parameter_class=ManualParameter,
                           initial_value=True,
                           label='Inverted output',
                           vals=Bool())

        self.add_parameter('gain',
                           parameter_class=ManualParameter,
                           initial_value=10,
                           label='Gain',
                           units=None,
                           vals=Numbers(min_value=0))

    def get_idn(self):
        vendor = 'Stanford Research Systems'
        model = 'SR560'
        serial = None
        firmware = None

        return {'vendor': vendor, 'model': model,
                'serial': serial, 'firmware': firmware}
