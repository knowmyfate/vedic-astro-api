from jhora.horoscope.chart import charts, dosha, raja_yoga, yoga
from jhora.horoscope.dhasa.graha import vimsottari
from jhora.horoscope.match import compatibility
from jhora.horoscope.prediction import general
from jhora.panchanga import drik
from jhora.utils import julian_day_number

def get_julian_day(data):
    return julian_day_number(data[0], data[1])

def get_place(data):
    return drik.Place(data[2])

def get_afflictions(data):
    jd = get_julian_day(data)
    place = get_place(data)
    return dosha.get_dosha_details(jd, place)

def get_compatibility(data):
    return compatibility.Ashtakoota(data[3])

def get_daily_calendar(data):
    jd = get_julian_day(data)
    place = get_place(data)
    tamil_date = drik.tamil_solar_month_and_date_from_jd(jd, place)
    moon_rise = drik.moonrise(jd, place)
    moon_set = drik.moonset(jd, place)
    sun_rise = drik.sunrise(jd, place)
    sun_set = drik.sunset(jd, place)
    rahu_kala = drik.trikalam(jd, place, data[3])
    gulika_kala = drik.trikalam(jd, place, data[3])
    yamaganda_kala = drik.trikalam(jd, place, data[3])
    tithi = drik.tithi(jd, place)
    rasi = drik.raasi(jd, place)
    nakshatra = drik.nakshatra(jd, place)
    karana= drik.karana(jd, place)
    masa = drik.lunar_month(jd, place)
    ritu = drik.ritu(masa[0])
    abhijit_muhurta = drik.abhijit_muhurta(jd, place)    
    day_length = drik.day_length(jd, place)
    night_length = drik.night_length(jd, place)
    nitya_yoga = drik.yogam(jd, place)
    elapsed_year = drik.elapsed_year(jd, masa[0])

    result = {
        "year": elapsed_year,
        "date": tamil_date,
        "sun": [sun_rise, sun_set],
        "moon": [moon_rise, moon_set],
        "day": day_length,
        "night": night_length,
        "ritu": ritu,
        "rasi": rasi,
        "nakshatra": nakshatra,
        "tithi": tithi,
        "karana": karana,
        "yoga": nitya_yoga,
        "rahu": rahu_kala,
        "gulika": gulika_kala,
        "yamaganda": yamaganda_kala,
        "abhijit": abhijit_muhurta,
    }
    return result

def get_divisional_chart(data):
    jd = get_julian_day(data)
    place = get_place(data)
    gulika = drik.upagraha_longitude(data[3], data[4], place, planet_index=data[5], ayanamsa_mode=data[6], divisional_chart_factor=data[7])
    chart = charts.divisional_chart(jd, place, ayanamsa_mode=data[6], divisional_chart_factor=data[7])
    retrograde_planets = drik.planets_in_retrograde(jd, place)
    return { chart, retrograde_planets, gulika }

def get_general_predictions(data):
    jd = get_julian_day(data)
    place = get_place(data)
    return general.get_prediction_details(jd, place)

def get_nakshatra(data):
    jd = get_julian_day(data)
    place = get_place(data)
    return drik.nakshatra(jd, place)

def get_planet_combinations(data):
    jd = get_julian_day(data)
    place = get_place(data)
    y = yoga.get_yoga_details(jd, place)
    r = raja_yoga.get_raja_yoga_details(jd, place)
    return { raja_yoga: r, yoga: y }

def get_planet_periods(data):
    jd = get_julian_day(data)
    place = get_place(data)
    dasha = {}
    if data[3] == "vimshottari":
        dasha = get_vimsottari_dasha(jd, place)
    return dasha

def get_planet_positions(data):
    return get_divisional_chart(data)

def get_vimsottari_dasha(jd, place):    
    dasha = vimsottari.vimsottari_mahadasa(jd, place)
    bhukthi = vimsottari.get_vimsottari_dhasa_bhukthi(jd, place)
    return { dasha, bhukthi }
  
