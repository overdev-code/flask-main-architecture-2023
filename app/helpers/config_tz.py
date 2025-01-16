from datetime import datetime
import pytz

def get_current_country_date_time(nombre_pais):
    try:
        # Obtener la zona horaria del país
        zona_horaria = pytz.country_timezones(nombre_pais)[0]
        # Obtener la fecha y hora actual en la zona horaria del país
        fecha_hora_actual = datetime.now(pytz.timezone(zona_horaria))

        return (nombre_pais, fecha_hora_actual.strftime("%Y-%m-%d"), fecha_hora_actual.strftime("%H:%M:%S"))
    
    except IndexError:
        print(f'No se encontró información de zona horaria para {nombre_pais}')
        
