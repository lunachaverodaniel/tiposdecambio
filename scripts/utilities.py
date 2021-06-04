import datetime as dt
@staticmethod
def escribirlog(archivo,mensaje,excepcion,stacktrace,funcion):
    with open(archivo,mode='a', encoding='utf-8') as fw:
        msj = []
        
        msj.append("------------------------------------------------------------------")
        msj.append("Se registro excepción en el metodo: " + funcion)
        msj.append("Con la fecha: " + dt.datetime.now)
        msj.append("Excepción:")
        msj.append(excepcion)
        msj.append("StackTrace:")
        msj.append(stacktrace)
        msj.append("Detalle de excepción:")
        msj.append(excepcion)
        msj.append("------------------------------------------------------------------")
        fw.write("\n".join(msj))