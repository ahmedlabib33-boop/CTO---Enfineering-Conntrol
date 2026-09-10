from __future__ import annotations

class _GuidanceReview:
    NAME='GUIDANCE'; FIELDS=[]; CRITICAL=[]
    @classmethod
    def review(cls, context):
        context=context or {}; findings=[]; available=0
        for field,label in cls.FIELDS:
            v=context.get(field)
            ok=v not in (None,'',[],{})
            if ok: available+=1
            else:
                findings.append({'field':field,'label':label,'severity':'CRITICAL' if field in cls.CRITICAL else 'REVIEW', 'status':'MISSING'})
        pct=round(100*available/max(1,len(cls.FIELDS)),1)
        crit=[f for f in findings if f['severity']=='CRITICAL']
        return {'engine':cls.NAME,'basis':'GUIDANCE_NOT_CONTRACT_STANDARD','coverage_percent':pct,
                'status':'REVIEW_REQUIRED' if crit or findings else 'PASS','critical_gaps':crit,'findings':findings,
                'note':'Review output supports planning judgment; it does not create contractual obligations or silently modify source schedule data.'}

class ScheduleBasisEngine(_GuidanceReview):
    NAME='AACE 38R-06 Schedule Basis Review'
    FIELDS=[('project_description','Project description'),('scope','Scope'),('wbs','WBS'),('execution_strategy','Execution strategy'),
            ('key_dates','Key dates'),('milestones','Milestones'),('calendar_basis','Calendar basis'),('duration_methodology','Duration methodology'),
            ('crew_resource_basis','Crew/resource basis'),('production_rate_source','Production-rate source'),('logic_methodology','Logic methodology'),
            ('long_lead_basis','Long-lead basis'),('commissioning_basis','Commissioning basis'),('critical_path_basis','Critical path/path of execution'),
            ('risks_assumptions','Risks/assumptions'),('p6_configuration','P6 configuration')]
    CRITICAL={'scope','wbs','key_dates','calendar_basis','duration_methodology','logic_methodology'}

class ConstructabilityEngine(_GuidanceReview):
    NAME='AACE 48R-06 Constructability Review'
    FIELDS=[('scope_completeness','Scope completeness'),('sequence','Sequence buildability'),('engineering_readiness','Engineering readiness'),
            ('procurement_readiness','Procurement readiness'),('site_access','Site access'),('laydown_storage','Laydown/storage'),
            ('work_restrictions','Work restrictions'),('weather_calendar','Weather/calendar'),('manpower_availability','Manpower availability'),
            ('equipment_limitations','Equipment limitations'),('material_availability','Material availability'),('trade_coordination','Trade coordination'),
            ('qa_testing','QA/QC integration'),('commissioning_integration','Commissioning integration'),('handover_demobilization','Handover/demobilization')]
    CRITICAL={'scope_completeness','sequence','engineering_readiness','procurement_readiness','site_access','commissioning_integration'}
