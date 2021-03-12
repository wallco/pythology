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

class MainFlow(Flow):
    def __init__(self, contactrate):
        self.parameter_label = 'beta'
        self.rate = contactrate
        self.origin = 'S'
        self.destiny = 'I'

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
            if type(flow) not in (Flow, MainFlow):
                raise AttributeError('The "flows" argument must be a list of flow objects')

        if type(flows) != list:
            raise AttributeError('The "flows" argument must be a list of flow objects')
        else:
            self.flows = flows

    def build(self, population, initial, time):
        for key, value in initial.items():
            if type(value) != int or type(key) != str or len(key) != 1:
                raise ValueError('The "initial" parameter must be a dictionary with 1-character strings as keys and integers as values!')
        if population != sum(initial.values()):
            raise ValueError('The sum of all initial values must be equal to the total population!')
        derivpos = {}
        derivneg = {}
        startarguments = ', '.join([str(flow.parameter_label) for flow in self.flows])
        start = 'import numpy as np\ndef deriv(y, timelist, N, {}):'.format(startarguments) + '\n\t'
        var = ', '.join(self.compartments) + ' = y\n'
        paramstring =''
        for flow in self.flows:
            if type(flow) != MainFlow:
                if flow.origin in derivneg.keys():
                    derivneg[flow.origin] += '-' + flow.parameter_label +'*{}'.format(flow.origin)
                else:
                    derivneg[flow.origin] = '-' + flow.parameter_label+'*{}'.format(flow.origin)

                if flow.destiny in derivpos.keys():
                  derivpos[flow.destiny] += '+' + flow.parameter_label+'*{}'.format(flow.origin)
                else:
                     derivpos[flow.destiny] = '+' + flow.parameter_label+'*{}'.format(flow.origin)
                paramstring = paramstring + '{} = {}\n'.format(flow.parameter_label, flow.rate)
            else:
                if flow.origin in derivneg.keys():
                    derivneg[flow.origin] += '-' + flow.parameter_label +'*{}'.format(flow.origin) + '*I/N'
                else:
                    derivneg[flow.origin] = '-' + flow.parameter_label + '*{}'.format(flow.origin) + '*I/N'

                if flow.destiny in derivpos.keys():
                    derivpos[flow.destiny] += '+' + flow.parameter_label + '*{}'.format(flow.origin) + '*I/N'
                else:
                    derivpos[flow.destiny] = '+' + flow.parameter_label + '*{}'.format(flow.origin) + '*I/N'
                paramstring = paramstring + '{} = {}\n'.format(flow.parameter_label, flow.rate)

        initialstring = ''
        equations = '\t'

        for compartment in self.compartments:
            try:
                pospart = derivpos[compartment]
            except KeyError:
                pospart = ''
            try:
                negpart = derivneg[compartment]
            except KeyError:
                negpart = ''
            equations += 'd{}dt = '.format(compartment) + pospart + negpart + '\n\t'
            initialstring = initialstring + ('{}0 = {}'.format(compartment, str(initial[compartment])+'\n'))


        derivlist = ['d{}dt'.format(c) for c in self.compartments]
        ret = 'return {}'.format(', '.join(derivlist))
        pop = '\nN = {}\n'.format(population)
        timeint = 'timelist = np.linspace(0, {}, {})'.format(time, time)
        initialist = '\ny0 = {}0\n'.format('0, '.join(self.compartments))
        integrate = 'retu = odeint(deriv, y0, timelist, args=(N, {}))'.format(', '.join(flow.parameter_label for flow in self.flows))
        final = '\n{} = retu.T'.format(', '.join(compartment for compartment in self.compartments))
        func = start + var + equations + ret + pop + initialstring + paramstring + timeint + initialist + integrate + final
        print (func)
        exec(func, globals())
        return retu.T



