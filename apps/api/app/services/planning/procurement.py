from __future__ import annotations
from datetime import date, datetime, timedelta

class ProcurementEngine:
    @staticmethod
    def _date(v):
        if isinstance(v, date): return v
        if not v: return None
        return datetime.strptime(str(v)[:10], '%Y-%m-%d').date()

    @classmethod
    def analyze(cls, required_on_site_date, lead_time_days, planned_procurement_start=None,
                source_verified=True, tight_buffer_days=None):
        req=cls._date(required_on_site_date)
        if req is None or lead_time_days is None:
            return {'status':'MISSING','missing':[k for k,v in {'required_on_site_date':req,'lead_time_days':lead_time_days}.items() if v is None]}
        lead=float(lead_time_days)
        if lead < 0: raise ValueError('lead_time_days cannot be negative')
        latest=req-timedelta(days=lead)
        out={'required_on_site_date':req.isoformat(),'lead_time_days':lead,
             'latest_safe_procurement_start':latest.isoformat(),'source_verified':bool(source_verified)}
        if not source_verified:
            out['status']='SOURCE_UNVERIFIED'; return out
        ps=cls._date(planned_procurement_start)
        if ps is None:
            out['status']='REVIEW_REQUIRED'; out['reason']='PLANNED_PROCUREMENT_START_UNAVAILABLE'; return out
        variance=(latest-ps).days
        out['planned_procurement_start']=ps.isoformat(); out['start_margin_days']=variance
        if ps > latest:
            out['status']='PROCUREMENT_LATE'
        elif tight_buffer_days is not None and variance <= int(tight_buffer_days):
            out['status']='PROCUREMENT_TIGHT'
        else:
            out['status']='PROCUREMENT_OK'
        return out
