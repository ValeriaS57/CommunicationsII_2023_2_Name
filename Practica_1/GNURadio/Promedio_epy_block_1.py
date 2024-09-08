"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__ will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, ventana_tamano=4096, num_ventanas=20):
        gr.sync_block.__init__(
            self,
            name='Promedios_de_tiempos',
            in_sig=[np.float32],
            out_sig=[np.float32, np.float32, np.float32, np.float32, np.float32]
        )
        self.ventana_tamano = ventana_tamano
        self.num_ventanas = num_ventanas
        self.ventanas = []
        self.salida_promedio = []
        self.resultados_acumulados = []

      
    def work(self, input_items, output_items):
        x = input_items[0]

        y0 = output_items[0]
        y1 = output_items[1]
        y2 = output_items[2]
        y3 = output_items[3]
        y4 = output_items[4]

        while len(x) >= self.ventana_tamano:
            ventana = x[:self.ventana_tamano]
            self.ventanas.append(ventana)
            x = x[self.ventana_tamano:]

            resultados = self.procesar_ventana(ventana)
            self.resultados_acumulados.append(resultados)

            if len(self.resultados_acumulados) == self.num_ventanas:
                resultados_array = np.array(self.resultados_acumulados)

                promedio_por_operacion = np.mean(resultados_array, axis=0)

                # Asignar los promedios a las salidas correspondientes
                y0[:] = promedio_por_operacion[0]
                y1[:] = promedio_por_operacion[1]
                y2[:] = promedio_por_operacion[2]
                y3[:] = promedio_por_operacion[3]
                y4[:] = promedio_por_operacion[4]

                # Limpiar para la próxima tanda de ventanas
                self.resultados_acumulados = []
                self.ventanas = []

        return len(y0)

    def procesar_ventana(self, ventana):
        promedio= np.mean(ventana)
        cua= np.mean(np.multiply(ventana, ventana))
        rms = np.sqrt(cua)
        potencia = np.multiply(rms, rms)
        desviacion_estandar = np.sqrt(np.var(ventana))

        # Retornar los resultados como una lista (promediados para ser consistentes)
        return [np.mean(promedio), np.mean(cua), np.mean(rms), np.mean(potencia),np.mean(desviacion_estandar)]
