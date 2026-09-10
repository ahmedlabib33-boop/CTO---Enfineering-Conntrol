from __future__ import annotations
from pathlib import Path
from datetime import datetime
import re

class XerCreator:
    REL_MAP={'FS':'PR_FS','SS':'PR_SS','FF':'PR_FF','SF':'PR_SF','PR_FS':'PR_FS','PR_SS':'PR_SS','PR_FF':'PR_FF','PR_SF':'PR_SF'}
    TYPE_MAP={'TASK':'TT_Task','TASK_DEPENDENT':'TT_Task','MILESTONE':'TT_Mile','START_MILESTONE':'TT_Mile','FINISH_MILESTONE':'TT_FinMile','LEVEL_OF_EFFORT':'TT_LOE','LOE':'TT_LOE','RESOURCE_DEPENDENT':'TT_Rsrc'}

    @staticmethod
    def esc(v):
        return str('' if v is None else v).replace('\t',' ').replace('\r',' ').replace('\n',' ').strip()
    @staticmethod
    def xdate(v): return f'{v} 08:00' if v else ''
    @classmethod
    def validate(cls,p):
        errors=[]; warnings=[]
        for k,label in [('project_name','Project Name'),('project_code','Project Code'),('planned_start','Planned Start')]:
            if not p.get(k): errors.append(f'{label} is required.')
        hp=p.get('hours_per_day'); dpw=p.get('workdays_per_week')
        try:
            if float(hp)<=0: errors.append('Hours/Day must be explicitly entered and > 0.')
        except Exception: errors.append('Hours/Day must be explicitly entered and > 0.')
        try:
            if not (1<=float(dpw)<=7): errors.append('Workdays/Week must be between 1 and 7.')
        except Exception: errors.append('Workdays/Week must be between 1 and 7.')
        acts=p.get('activities') or []
        if not acts: errors.append('At least one activity is required.')
        ids=set()
        for i,a in enumerate(acts):
            aid=cls.esc(a.get('activity_id') or a.get('task_code')); name=cls.esc(a.get('activity_name') or a.get('task_name'))
            typ=cls.esc(a.get('activity_type') or 'TASK').upper(); mile=typ in {'MILESTONE','START_MILESTONE','FINISH_MILESTONE'}
            dur=a.get('duration_days',a.get('original_duration'))
            if not aid: errors.append(f'Activity #{i+1}: activity_id is required.')
            if aid in ids: errors.append(f'Duplicate Activity ID: {aid}')
            ids.add(aid)
            if not name: errors.append(f'{aid or "Activity #"+str(i+1)}: activity_name is required.')
            if not mile:
                try:
                    if dur in (None,'') or float(dur)<0: raise ValueError
                except Exception: errors.append(f'{aid}: duration_days is required for non-milestone activities.')
            elif float(dur or 0)!=0: warnings.append(f'{aid}: milestone duration will be written as 0.')
        for i,r in enumerate(p.get('relationships') or []):
            pred=cls.esc(r.get('predecessor') or r.get('pred_activity_id')); succ=cls.esc(r.get('successor') or r.get('succ_activity_id'))
            typ=cls.esc(r.get('type') or r.get('relationship_type') or 'FS').upper()
            if pred not in ids: errors.append(f'Relationship #{i+1}: predecessor {pred} not found.')
            if succ not in ids: errors.append(f'Relationship #{i+1}: successor {succ} not found.')
            if typ not in cls.REL_MAP: errors.append(f'Relationship #{i+1}: unsupported type {typ}.')
        return {'valid':not errors,'errors':errors,'warnings':warnings,'status':'XER_STRUCTURE_VALID' if not errors else 'BLOCKED',
                'schedule_quality_approved':False,'p6_native_verification_required':True}

    @classmethod
    def table(cls,name,fields,rows):
        lines=[f'%T\t{name}', '%F\t'+'\t'.join(fields)]
        lines += ['%R\t'+'\t'.join(cls.esc(x) for x in row) for row in rows]
        return lines

    @classmethod
    def build(cls,p):
        v=cls.validate(p)
        if not v['valid']: raise ValueError('\n'.join(v['errors']))
        hp=float(p['hours_per_day']); dpw=float(p['workdays_per_week']); week=hp*dpw; month=week*4.3333333333; year=week*52
        project_id=1000; calendar_id=3000; root_wbs_id=2000
        pcode=re.sub(r'[^A-Za-z0-9_.-]+','-',cls.esc(p['project_code']))[:40] or 'PROJECT'
        start=cls.xdate(p['planned_start']); dd=cls.xdate(p.get('data_date') or p['planned_start']); now=datetime.now().strftime('%Y-%m-%d %H:%M')
        lines=[f'ERMHDR\t24.0\t{datetime.now().date().isoformat()}\tProject\tXER Creator\t\tUSD']
        lines += cls.table('CALENDAR',['clndr_id','default_flag','clndr_name','proj_id','base_clndr_id','last_chng_date','clndr_type','day_hr_cnt','week_hr_cnt','month_hr_cnt','year_hr_cnt','rsrc_private','clndr_data'],
                           [[calendar_id,'Y',p.get('calendar_name') or f'{hp:g}h x {dpw:g}d Calendar',project_id,'',now,'CA_Project',hp,week,f'{month:.2f}',f'{year:.2f}','N','']])
        lines += cls.table('PROJECT',['proj_id','proj_short_name','plan_start_date','last_recalc_date','scd_end_date','add_date','def_duration_type','task_code_prefix','task_code_base','task_code_step','def_task_type','critical_drtn_hr_cnt','clndr_id'],
                           [[project_id,pcode,start,dd,'',now,'DT_FixedDrtn','',1000,10,'TT_Task',0,calendar_id]])
        wbs_names={}
        for a in p['activities']:
            code=cls.esc(a.get('wbs_code') or a.get('wbs'))
            if code: wbs_names[code]=cls.esc(a.get('wbs_name')) or code
        wbs_map={pcode:root_wbs_id}; wrows=[[root_wbs_id,project_id,1,'Y','Y','WS_Open',pcode,p['project_name'],'']]
        for i,(code,name) in enumerate(sorted(wbs_names.items()),1):
            wid=2000+i; wbs_map[code]=wid; wrows.append([wid,project_id,i+1,'N','Y','WS_Open',code,name,root_wbs_id])
        lines += cls.table('PROJWBS',['wbs_id','proj_id','seq_num','proj_node_flag','sum_data_flag','status_code','wbs_short_name','wbs_name','parent_wbs_id'],wrows)
        task_id={}; tf=['task_id','proj_id','wbs_id','clndr_id','phys_complete_pct','rev_fdbk_flag','est_wt','lock_plan_flag','auto_compute_act_flag','complete_pct_type','task_type','duration_type','status_code','task_code','task_name','rsrc_id','total_float_hr_cnt','free_float_hr_cnt','remain_drtn_hr_cnt','act_work_qty','target_work_qty','target_drtn_hr_cnt','target_equip_qty','act_equip_qty','remain_equip_qty','cstr_type','cstr_date','act_start_date','act_end_date','late_start_date','late_end_date','expect_end_date','early_start_date','early_end_date','restart_date','reend_date','target_start_date','target_end_date','rem_late_start_date','rem_late_end_date','cstr_type2','cstr_date2','priority_type','suspend_date','resume_date','float_path','float_path_order','guid','tmpl_guid','is_starred']
        tr=[]
        for i,a in enumerate(p['activities']):
            iid=10001+i; code=cls.esc(a.get('activity_id') or a.get('task_code')); task_id[code]=iid
            typ=cls.esc(a.get('activity_type') or 'TASK').upper(); tt=cls.TYPE_MAP.get(typ,'TT_Task'); mile=tt in {'TT_Mile','TT_FinMile'}
            days=0 if mile else float(a.get('duration_days',a.get('original_duration'))); hrs=days*hp
            wbs=wbs_map.get(cls.esc(a.get('wbs_code') or a.get('wbs')),root_wbs_id)
            row=[iid,project_id,wbs,calendar_id,0,'N',1,'N','Y','CP_Drtn',tt,'DT_FixedDrtn','TK_NotStart',code,cls.esc(a.get('activity_name') or a.get('task_name')),'',0,0,hrs,'','',hrs,'','','','','','','','','','','','','','',start,'','','','','','','','','','','','','']
            if len(row)<len(tf): row += ['']*(len(tf)-len(row))
            tr.append(row[:len(tf)])
        lines += cls.table('TASK',tf,tr)
        rr=[]
        for i,r in enumerate(p.get('relationships') or []):
            pred=cls.esc(r.get('predecessor') or r.get('pred_activity_id')); succ=cls.esc(r.get('successor') or r.get('succ_activity_id'))
            typ=cls.REL_MAP[cls.esc(r.get('type') or r.get('relationship_type') or 'FS').upper()]
            rr.append([50001+i,task_id[succ],task_id[pred],project_id,project_id,typ,float(r.get('lag_days') or 0)*hp])
        lines += cls.table('TASKPRED',['task_pred_id','task_id','pred_task_id','proj_id','pred_proj_id','pred_type','lag_hr_cnt'],rr)
        lines.append('%E')
        return '\r\n'.join(lines)+'\r\n'

    @classmethod
    def save(cls,p,directory):
        text=cls.build(p); code=re.sub(r'[^A-Za-z0-9_.-]+','-',cls.esc(p['project_code'])) or 'PROJECT'
        path=Path(directory)/f'{code}_CREATED.xer'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding='utf-8',newline='')
        return {'path':str(path),'filename':path.name,'validation':cls.validate(p),'bytes':path.stat().st_size}
