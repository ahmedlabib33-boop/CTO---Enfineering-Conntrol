from __future__ import annotations

class ScheduleQAEngine:
    VALID_REL={'FS','SS','FF','SF','PR_FS','PR_SS','PR_FF','PR_SF'}

    @classmethod
    def review(cls, activities, relationships, excessive_lag_days=None):
        issues=[]; ids=[]; amap={}
        for i,a in enumerate(activities or []):
            aid=str(a.get('activity_id') or a.get('task_code') or '').strip()
            name=str(a.get('activity_name') or a.get('task_name') or '').strip()
            typ=str(a.get('activity_type') or 'TASK').upper()
            milestone=typ in {'MILESTONE','START_MILESTONE','FINISH_MILESTONE'}
            if not aid: issues.append(cls._issue('MISSING_ACTIVITY_ID','CRITICAL',f'Activity row {i+1} has no ID'))
            elif aid in amap: issues.append(cls._issue('DUPLICATE_ACTIVITY_ID','CRITICAL',f'Duplicate Activity ID {aid}',aid))
            else: ids.append(aid); amap[aid]=a
            if not name: issues.append(cls._issue('MISSING_ACTIVITY_NAME','MAJOR',f'{aid or i+1}: activity name missing',aid))
            dur=a.get('duration_days',a.get('original_duration'))
            if not milestone and (dur is None or dur==''):
                issues.append(cls._issue('MISSING_DURATION','CRITICAL',f'{aid}: duration missing',aid))
            if not a.get('calendar_id') and not a.get('calendar'):
                issues.append(cls._issue('MISSING_CALENDAR','MAJOR',f'{aid}: calendar basis missing',aid))
        pred={x:0 for x in ids}; succ={x:0 for x in ids}
        for i,r in enumerate(relationships or []):
            p=str(r.get('predecessor') or r.get('pred_activity_id') or '').strip()
            s=str(r.get('successor') or r.get('succ_activity_id') or '').strip()
            t=str(r.get('type') or r.get('relationship_type') or 'FS').upper()
            if p not in amap: issues.append(cls._issue('MISSING_PREDECESSOR_REFERENCE','CRITICAL',f'Relationship {i+1}: predecessor {p} not found'))
            if s not in amap: issues.append(cls._issue('MISSING_SUCCESSOR_REFERENCE','CRITICAL',f'Relationship {i+1}: successor {s} not found'))
            if t not in cls.VALID_REL: issues.append(cls._issue('INVALID_RELATIONSHIP','CRITICAL',f'Relationship {i+1}: invalid type {t}'))
            if p in succ: succ[p]+=1
            if s in pred: pred[s]+=1
            lag=r.get('lag_days',0)
            if lag not in (None,'') and excessive_lag_days is not None and abs(float(lag)) > float(excessive_lag_days):
                issues.append(cls._issue('EXCESSIVE_LAG','MAJOR',f'{p}->{s}: lag {lag}d exceeds configured threshold'))
        for aid,a in amap.items():
            typ=str(a.get('activity_type') or 'TASK').upper()
            if pred.get(aid,0)==0 and typ not in {'START_MILESTONE'}:
                issues.append(cls._issue('OPEN_START','WARNING',f'{aid}: no predecessor',aid))
            if succ.get(aid,0)==0 and typ not in {'FINISH_MILESTONE'}:
                issues.append(cls._issue('OPEN_FINISH','WARNING',f'{aid}: no successor',aid))
        critical=sum(1 for x in issues if x['severity']=='CRITICAL')
        major=sum(1 for x in issues if x['severity']=='MAJOR')
        status='FAIL' if critical else ('REVIEW_REQUIRED' if major else ('PASS_WITH_COMMENTS' if issues else 'PASS'))
        return {'status':status,'issues':issues,'counts':{'critical':critical,'major':major,'total':len(issues)},
                'note':'Schedule QA is independent from XER structural validity and does not replace native Primavera P6 CPM.'}

    @staticmethod
    def _issue(code,severity,message,activity_id=None):
        return {'code':code,'severity':severity,'message':message,'activity_id':activity_id,'status':'OPEN'}
