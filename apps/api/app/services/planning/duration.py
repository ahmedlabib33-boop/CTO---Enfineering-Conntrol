from __future__ import annotations
from math import ceil

class DurationEngine:
    BASES = {
        'QUANTITY_PER_MANHOUR','MANHOURS_PER_QUANTITY','QUANTITY_PER_CREW_HOUR',
        'QUANTITY_PER_EQUIPMENT_HOUR','QUANTITY_PER_SHIFT','QUANTITY_PER_DAY',
        'CREW_DAILY_PRODUCTION','EQUIPMENT_DAILY_PRODUCTION','TIME_BASED','ALLOWANCE','UNKNOWN'
    }

    @staticmethod
    def _missing(**kwargs):
        return [k for k,v in kwargs.items() if v is None or v == '']

    @classmethod
    def calculate(cls, *, quantity=None, rate=None, rate_basis='UNKNOWN', crews=None,
                  shift_hours=None, productive_hours=None, labor_per_crew=None,
                  equipment_units_per_crew=None, operating_hours=None,
                  time_based_duration=None, round_up=True, source_ids=None):
        basis=str(rate_basis or 'UNKNOWN').upper()
        if basis not in cls.BASES:
            return {'status':'REVIEW_REQUIRED','reason':'UNSUPPORTED_RATE_BASIS','rate_basis':basis}
        if basis == 'UNKNOWN':
            return {'status':'REVIEW_REQUIRED','reason':'RATE_BASIS_UNKNOWN','rate_basis':basis}
        if basis in {'TIME_BASED','ALLOWANCE'}:
            missing=cls._missing(time_based_duration=time_based_duration)
            if missing: return {'status':'MISSING','missing':missing,'rate_basis':basis}
            d=float(time_based_duration)
            if d < 0: raise ValueError('duration cannot be negative')
            return {'status':'CALCULATED','rate_basis':basis,'raw_duration_days':d,
                    'planned_duration_days':ceil(d) if round_up else d,
                    'formula':'DURATION = EXPLICIT TIME-BASED DURATION','source_ids':source_ids or []}

        missing=cls._missing(quantity=quantity, rate=rate)
        if missing: return {'status':'MISSING','missing':missing,'rate_basis':basis}
        q=float(quantity); r=float(rate)
        if q < 0 or r <= 0: raise ValueError('quantity must be >=0 and rate must be >0')

        total_mh=None; daily=None; formula=''
        if basis == 'QUANTITY_PER_MANHOUR':
            missing=cls._missing(crews=crews, labor_per_crew=labor_per_crew, productive_hours=productive_hours)
            if missing: return {'status':'MISSING','missing':missing,'rate_basis':basis,'total_mh':q/r}
            total_mh=q/r
            daily_capacity=float(crews)*float(labor_per_crew)*float(productive_hours)
            if daily_capacity <= 0: raise ValueError('daily labor capacity must be >0')
            raw=total_mh/daily_capacity
            formula='TOTAL_MH = QUANTITY / PRODUCTIVITY; DURATION = TOTAL_MH / (CREWS × LABOR_PER_CREW × PRODUCTIVE_HOURS)'
        elif basis == 'MANHOURS_PER_QUANTITY':
            missing=cls._missing(crews=crews, labor_per_crew=labor_per_crew, productive_hours=productive_hours)
            if missing: return {'status':'MISSING','missing':missing,'rate_basis':basis,'total_mh':q*r}
            total_mh=q*r
            daily_capacity=float(crews)*float(labor_per_crew)*float(productive_hours)
            if daily_capacity <= 0: raise ValueError('daily labor capacity must be >0')
            raw=total_mh/daily_capacity
            formula='TOTAL_MH = QUANTITY × MH_PER_UNIT; DURATION = TOTAL_MH / (CREWS × LABOR_PER_CREW × PRODUCTIVE_HOURS)'
        elif basis == 'QUANTITY_PER_CREW_HOUR':
            missing=cls._missing(crews=crews, productive_hours=productive_hours)
            if missing: return {'status':'MISSING','missing':missing,'rate_basis':basis}
            daily=r*float(crews)*float(productive_hours)
            raw=q/daily
            formula='DAILY_PRODUCTION = RATE × CREWS × PRODUCTIVE_HOURS; DURATION = QUANTITY / DAILY_PRODUCTION'
        elif basis == 'QUANTITY_PER_EQUIPMENT_HOUR':
            missing=cls._missing(crews=crews, equipment_units_per_crew=equipment_units_per_crew, operating_hours=operating_hours)
            if missing: return {'status':'MISSING','missing':missing,'rate_basis':basis}
            daily=r*float(equipment_units_per_crew)*float(crews)*float(operating_hours)
            raw=q/daily
            formula='DAILY_PRODUCTION = RATE × EQUIPMENT_UNITS_PER_CREW × CREWS × OPERATING_HOURS; DURATION = QUANTITY / DAILY_PRODUCTION'
        elif basis in {'QUANTITY_PER_SHIFT','QUANTITY_PER_DAY','CREW_DAILY_PRODUCTION'}:
            missing=cls._missing(crews=crews)
            if missing: return {'status':'MISSING','missing':missing,'rate_basis':basis}
            daily=r*float(crews)
            raw=q/daily
            formula='TOTAL_DAILY_PRODUCTION = CREW_DAILY_PRODUCTION × NUMBER_OF_CREWS; DURATION = QUANTITY / TOTAL_DAILY_PRODUCTION'
        elif basis == 'EQUIPMENT_DAILY_PRODUCTION':
            missing=cls._missing(crews=crews, equipment_units_per_crew=equipment_units_per_crew)
            if missing: return {'status':'MISSING','missing':missing,'rate_basis':basis}
            daily=r*float(equipment_units_per_crew)*float(crews)
            raw=q/daily
            formula='TOTAL_DAILY_PRODUCTION = EQUIPMENT_DAILY_PRODUCTION × EQUIPMENT_UNITS_PER_CREW × CREWS; DURATION = QUANTITY / TOTAL_DAILY_PRODUCTION'
        else:
            return {'status':'REVIEW_REQUIRED','reason':'RATE_BASIS_UNKNOWN','rate_basis':basis}
        if daily is not None and daily <= 0: raise ValueError('daily production must be >0')
        result={'status':'CALCULATED','rate_basis':basis,'quantity':q,'rate':r,
                'raw_duration_days':raw,'planned_duration_days':ceil(raw) if round_up else raw,
                'formula':formula,'source_ids':source_ids or []}
        if total_mh is not None: result['total_man_hours']=total_mh
        if daily is not None: result['total_daily_production']=daily
        if labor_per_crew is not None and crews is not None and shift_hours is not None:
            result['labor_mh_planned']=float(labor_per_crew)*float(crews)*float(shift_hours)*raw
        if equipment_units_per_crew is not None and crews is not None and operating_hours is not None:
            result['equipment_hours_planned']=float(equipment_units_per_crew)*float(crews)*float(operating_hours)*raw
        return result
