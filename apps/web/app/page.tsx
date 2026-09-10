\
"use client";
import {useState} from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function Home(){
  const [token,setToken]=useState("");
  const [projectId,setProjectId]=useState<number|undefined>();
  const [currentId,setCurrentId]=useState<number|undefined>();
  const [referenceId,setReferenceId]=useState<number|undefined>();
  const [comparison,setComparison]=useState<any>(null);
  const [revised,setRevised]=useState("");
  const [exports,setExports]=useState<any>(null);
  const [log,setLog]=useState<string[]>([]);

  const note=(x:string)=>setLog(v=>[x,...v].slice(0,20));
  const headers=()=>({"Authorization":`Bearer ${token}`});

  async function login(){
    const r=await fetch(`${API}/auth/login`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:"admin",password:"admin"})});
    const j=await r.json(); setToken(j.access_token||""); note(r.ok?"Logged in":"Login failed");
  }
  async function createProject(){
    const r=await fetch(`${API}/projects`,{method:"POST",headers:{...headers(),"Content-Type":"application/json"},body:JSON.stringify({name:`Demo Project ${Date.now()}`})});
    const j=await r.json(); setProjectId(j.id); note(`Project ${j.id} created`);
  }
  async function upload(file:File|null, role:"current"|"reference"){
    if(!file||!projectId)return;
    const f=new FormData();f.append("file",file);f.append("kind",role);f.append("revision",role==="current"?"R01":"R02");
    const r=await fetch(`${API}/projects/${projectId}/documents`,{method:"POST",headers:headers(),body:f});
    const j=await r.json(); role==="current"?setCurrentId(j.id):setReferenceId(j.id); note(`${role} uploaded as document ${j.id}`);
  }
  async function compare(){
    const r=await fetch(`${API}/comparison-runs`,{method:"POST",headers:{...headers(),"Content-Type":"application/json"},body:JSON.stringify({project_id:projectId,current_document_id:currentId,reference_document_id:referenceId})});
    const j=await r.json();setComparison(j);note(`${j.change_count||0} changes detected`);
  }
  async function approve(id:number){
    const r=await fetch(`${API}/changes/${id}/approve`,{method:"POST",headers:headers()});
    note(r.ok?`Change ${id} approved`:`Change ${id} blocked/requires engineering review`);
    await refreshChanges();
  }
  async function reject(id:number){
    await fetch(`${API}/changes/${id}/reject`,{method:"POST",headers:headers()});note(`Change ${id} rejected`);await refreshChanges();
  }
  async function refreshChanges(){
    if(!comparison?.id)return;
    const r=await fetch(`${API}/comparison-runs/${comparison.id}/changes`,{headers:headers()});
    const j=await r.json();setComparison((v:any)=>({...v,changes:j}));
  }
  async function modify(){
    const r=await fetch(`${API}/modification-runs`,{method:"POST",headers:{...headers(),"Content-Type":"application/json"},body:JSON.stringify({comparison_id:comparison.id})});
    const j=await r.json();setRevised(j.revised_dxf_path);note(`Modified DXF QA: ${j.qa?.status}`);
  }
  async function exportAll(){
    const r=await fetch(`${API}/exports`,{method:"POST",headers:{...headers(),"Content-Type":"application/json"},body:JSON.stringify({project_id:projectId,comparison_id:comparison.id,revised_dxf_path:revised})});
    const j=await r.json();setExports(j);note("DXF/PDF/redline/XLSX exports generated");
  }

  const card={background:"#fff",border:"1px solid #d9dee5",borderRadius:8,padding:16};
  const btn={padding:"9px 14px",border:"1px solid #64748b",borderRadius:6,background:"#fff",cursor:"pointer",marginRight:8,marginBottom:8};
  return <main style={{padding:20,maxWidth:1400,margin:"0 auto"}}>
    <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}><h1 style={{marginTop:0}}>Engineering CAD Platform — Controlled DXF MVP</h1><a href="/planning">Planning Intelligence →</a></div>
    <p>Real DXF parse/compare/approval/modification/QA/export workflow. Class C is blocked server-side.</p>

    <div style={{display:"grid",gridTemplateColumns:"1fr 2fr 1fr",gap:14}}>
      <section style={card}>
        <h3>Documents</h3>
        <button style={btn} onClick={login}>1. Login</button>
        <button style={btn} disabled={!token} onClick={createProject}>2. Create Project</button>
        <p>Project: {projectId||"—"}</p>
        <label>Current DXF<br/><input type="file" accept=".dxf" onChange={e=>upload(e.target.files?.[0]||null,"current")}/></label>
        <p>Current document: {currentId||"—"}</p>
        <label>Reference DXF<br/><input type="file" accept=".dxf" onChange={e=>upload(e.target.files?.[0]||null,"reference")}/></label>
        <p>Reference document: {referenceId||"—"}</p>
        <button style={btn} disabled={!currentId||!referenceId} onClick={compare}>3. Compare</button>
      </section>

      <section style={card}>
        <h3>Change Review</h3>
        <div style={{maxHeight:520,overflow:"auto"}}>
          {(comparison?.changes||[]).map((c:any)=><div key={c.id||c.change_key} style={{borderBottom:"1px solid #e5e7eb",padding:"10px 0"}}>
            <b>{c.change_key}</b> {c.change_type} — Class {c.change_class} — <b>{c.status}</b><br/>
            <small>{c.source_handle||"∅"} → {c.target_handle||"∅"} | {c.authority} | {c.confidence}</small><br/>
            {c.id&&<><button style={btn} onClick={()=>approve(c.id)}>Approve</button><button style={btn} onClick={()=>reject(c.id)}>Reject</button></>}
          </div>)}
        </div>
        <button style={btn} disabled={!comparison?.id} onClick={refreshChanges}>Refresh</button>
        <button style={btn} disabled={!comparison?.id} onClick={modify}>4. Apply Approved Changes</button>
        <button style={btn} disabled={!revised} onClick={exportAll}>5. Generate Outputs</button>
      </section>

      <section style={card}>
        <h3>Control / Evidence</h3>
        <p><b>Revised DXF</b><br/><small>{revised||"—"}</small></p>
        <p><b>Exports</b></p>
        {exports&&Object.entries(exports.exports||{}).map(([k,v])=><div key={k}><small>{k}: {String(v)}</small></div>)}
        <h4>Activity</h4>
        {log.map((x,i)=><div key={i} style={{fontSize:12,padding:"4px 0"}}>{x}</div>)}
      </section>
    </div>
  </main>
}
