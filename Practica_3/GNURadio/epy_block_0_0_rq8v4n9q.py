import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
    """This block is a CE VCO or baseband VCO and works as following:
	Baseband Signal Formation Aid 
	Inputs:
	1)We have the first input named A (input_items[0]) which controls the amplitude of the output signal.
	2)The second input named Q (Q=input_items[1]) is responsible for varying the phase for the complex exponential.
	
	Parameters:
	In this case we will not have additional parameters like fc or samp_rate.

	Recommendations:
	1)Both the first and the second input should have the same length.
	2) Do not add high values for amplitude or radical variations so that Q does not generate unwanted spectral components.
	unwanted spectral components
	"""

    def __init__(self,):  
        gr.sync_block.__init__(
            self,
            name='e_CE_VCO_fc',   
            in_sig=[np.float32, np.float32],
            out_sig=[np.complex64]
        )
        
    def work(self, input_items, output_items):
        A=input_items[0]
        Q=input_items[1]
        y=output_items[0]
        N=len(A)
        y[:]=A*np.exp(1j*Q)			#Señal en banda base, componente compleja
        return len(output_items[0])
