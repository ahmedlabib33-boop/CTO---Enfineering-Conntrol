"use client";
import {useState} from "react";
const API=process.env.NEXT_PUBLIC_API_URL||"http://127.0.0.1:8000";
const stages=["Source Upload","Data Analyzer","Raw Evidence Vault","Normalization","Master Activity","WBS / Coding","Engineering Readiness","Procurement","Productivity","Crews","Equipment","Materials","Quantity + Base Time","Duration / Man-Hour","Construction Sequence","MEP Stage","AACE 38R-06","AACE 48R-06","Schedule QA","Engineer Decision","Primavera Schedule Builder","XER Validation","XER Creator","P6 Native Import","P6 Native CPM","Post-P6 QA","Final Outputs"];
export default function PlanningPage(){
 const [qty,setQty]=useState(2400); const [rate,setRate]=useState(300); const [crews,setCrews]=useState(2); const [result,setResult]=useState<any>(null);
 const [token,setToken]=useState("");
 async function login(){const r=await fetch(`${API}/auth/login`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:"admin",password:"admin"})});const j=await r.json();setToken(j.access_token||"");}
 async function calc(){const r=await fetch(`${API}/planning/duration/calculate`,{method:"POST",headers:{"Content-Type":"application/json","Authorization":`Bearer ${token}`},body:JSON.stringify({quantity:qty,rate,rate_basis:"CREW_DAILY_PRODUCTION",crews})});setResult(await r.json());}
 return <main style={{padding:20,maxWidth:1500,margin:"auto",fontFamily:"Arial"}}>
  <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}><div><h1>Construction Planning + Primavera Intelligence Layer</h1><p>Evidence-first planning layer connected above the CAD/ML/Math platform.</p></div><a href="/">CAD Workspace</a></div>
  <section style={{background:"white",padding:16,border:"1px solid #ddd",borderRadius:8,marginBottom:16}}><b>Golden flow:</b> Preserve → Normalize → Analyze → Engineer → Calculate → Review → Approve → Export. Native Primavera P6 remains the final CPM authority after XER import.</section>
  <section style={{background:"white",padding:16,border:"1px solid #ddd",borderRadius:8,marginBottom:16}}><h3>27-Stage Planning Pipeline</h3><div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(210px,1fr))",gap:8}}>{stages.map((s,i)=><div key={s} style={{padding:10,border:"1px solid #e5e7eb",borderRadius:6}}><b>{String(i+1).padStart(2,"0")}</b> {s}</div>)}</div></section>
  <section style={{background:"white",padding:16,border:"1px solid #ddd",borderRadius:8}}><h3>Deterministic Duration Engine</h3><button onClick={login}>Login Demo</button><div style={{display:"flex",gap:8,marginTop:10,flexWrap:"wrap"}}><label>Quantity <input type="number" value={qty} onChange={e=>setQty(Number(e.target.value))}/></label><label>Production / crew / day <input type="number" value={rate} onChange={e=>setRate(Number(e.target.value))}/></label><label>Crews <input type="number" value={crews} onChange={e=>setCrews(Number(e.target.value))}/></label><button disabled={!token} onClick={calc}>Calculate</button></div>{result&&<pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(result,null,2)}</pre>}</section>
 </main>
}
