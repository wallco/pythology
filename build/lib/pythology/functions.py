import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from pprint import pprint

class Flow:
    def __init__(self, parameter_label, rate, origin=None, destiny=None):
        if type(rate) not in (int, float):
            raise AttributeError('The flow element rate must be a number!')
        else:
            self.rate = rate

        if type(origin) not in (None, str) or (type(origin) == str and len(origin) != 1):
            raise AttributeError("""The flow origin must be either None (for individuals coming from outside the model 
                                 in increasing populations) or an 1-character string""")
        else:
            self.origin = origin

        if type(destiny) not in (None, str) or (type(destiny) == str and len(destiny) != 1):
            raise AttributeError("""The flow origin must be either None (for individuals coming from outside the model 
                                 in increasing populations) or an 1-character string""")
        else:
            self.destiny = destiny

        if parameter_label is None or len(parameter_label) > 4 or type(parameter_label) != str:
            raise AttributeError('The parameter label must be a 4-digit or less string!')
        else:
            self.parameter_label = parameter_label

class CompartmentalModel:
    def __init__(self, compartments, flows):
        for compartment in compartments:
            if type(compartment) != str or len(compartment) != 1:
                raise AttributeError('The "compartments" argument must be a list of 1-character strings')

        if type(compartments) != list:
            raise AttributeError('The "compartments" argument must be a list of 1-character strings')
        else:
            self.compartments = compartments

        for flow in flows:
            if type(flow) != Flow:
                raise AttributeError('The "flows" argument must be a list of flow objects')

        if type(flows) != list:
            raise AttributeError('The "flows" argument must be a list of flow objects')
        else:
            self.flows = flows

    def build(self, population, initial, params, time):
        derivpos = {}
        derivneg = {}
        startarguments = ', '.join([str(flow.parameter_label) for flow in self.flows])
        start = 'def deriv(y, t, {}):'.format(startarguments) + '\n\t'
        var = ', '.join(self.compartments) + ' = y\n'
        for flow in self.flows:
              if flow.origin in derivneg.keys():
                  derivneg[flow.origin] += '-' + flow.parameter_label
              else:
                  derivneg[flow.origin] = '-' + flow.parameter_label

              if flow.destiny in derivpos.keys():
                  derivpos[flow.destiny] += '+' + flow.parameter_label
              else:
                  derivpos[flow.destiny] = '+' + flow.parameter_label

        equations = '\t'
        for compartment in self.compartments:
            try:
                pospart = derivpos[compartment] + '*{}'.format(compartment)
            except KeyError:
                pospart = ''
            try:
                negpart = derivneg[compartment] + '*{}'.format(compartment)
            except KeyError:
                negpart = ''
            equations += 'd{}dt = '.format(compartment) + pospart + negpart + '\n\t'

        derivlist = ['d{}dt'.format(c) for c in self.compartments]
        ret = 'return {}'.format(', '.join(derivlist))
        func = start + var + equations + ret
        print (func)
        #exec(func)



compartmentlist = ['S', 'I', 'R']

si = Flow(parameter_label='beta', rate=1, origin='S',destiny='I')
ir = Flow(parameter_label='mi', rate=0.5, origin='I', destiny='R')

flowlist = [si, ir]

a = CompartmentalModel(compartments=compartmentlist, flows=flowlist)


a.build(1,1, 1, 1)




