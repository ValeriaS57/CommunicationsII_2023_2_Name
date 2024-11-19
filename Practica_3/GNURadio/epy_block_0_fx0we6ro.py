import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
     """This block is a RF VCO and works as following: .....
	Inputs:
	1)We have the first input named A (input_items[0]) which controls the amplitude of the output signal.
	2)The second input named Q (Q=input_items[1]) is responsible for varying the phase of the signal.
	
	Parameters:
	For frequency and samp rate the default values are 128kHz and 320kHz respectively (this applies only if no external values are given).
	only if no different external values are given).

	Recommendations:
	1)Special care should be taken with fc and samp_rate to avoid aliasing (samp_rate at least twice the carrier frequency).
	twice the carrier frequency).
	2) Both input one and input two should have the same length,
	additionally very large numbers should be avoided to avoid distortion.
	"""

    def __init__(self, fc=128000, samp_rate=320000): 
	#Se llaman funciones inicializadores de Python para crear el bloque en GNU  
        gr.sync_block.__init__(
            self,
            name='e_RF_VCO_ff',   				#Le agregamos nombre
            in_sig=[np.float32, np.float32],			#Definimos como flotante las dos señales de entrada
            out_sig=[np.float32]				#Defninmos como flotante la señal de salida
        )
        self.fc = fc						#Se agrega el valor de la frecuencia portadora
        self.samp_rate = samp_rate				#Se agrega el valor de frecuencia de muestreo
        self.n_m=0						#Se inicializa el acumulador

    def work(self, input_items, output_items):
        A=input_items[0]
        Q=input_items[1]
        y=output_items[0]
        N=len(A)						#Numero de muestras a procesar
        n=np.linspace(self.n_m,self.n_m+N-1,N)			# Índice de tiempo para el bloque actual
        self.n_m += N						# Actualizar el índice de muestras para el siguiente bloque
        y[:]=A*np.cos(2*math.pi*self.fc*n/self.samp_rate+Q)     # Generar la señal de salida
        return len(output_items[0])


