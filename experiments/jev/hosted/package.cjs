#!/usr/bin/env node
'use strict';
// Uses Python's standard library ZIP writer and an explicit source-file allowlist.
const {spawnSync}=require('node:child_process');const path=require('node:path');
const root=path.resolve(__dirname,'../../..');
const result=spawnSync('python3',['-c',`
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root=Path.cwd()
files=['data ingestion/server.py','data ingestion/static/index.html','data ingestion/static/style.css','data ingestion/static/app.js','acquisition/run_skill.cjs','acquisition/skills/upright-paid-orders.skill.json','tools/verification/package.json','tools/verification/package-lock.json']
files += ['experiments/jev/'+name for name in ['lab.cjs','run.cjs','provider.cjs','dom.cjs','verify.cjs','recorder.cjs','recipe.cjs']]
files += [str(p.relative_to(root)) for p in (root/'experiments/jev/hosted').iterdir() if p.is_file()]
output=root/'.runtime/jev-replit-demo.zip'; output.parent.mkdir(exist_ok=True)
with ZipFile(output,'w',ZIP_DEFLATED) as archive:
 for name in sorted(files): archive.write(root/name,name)
 archive.write(root/'experiments/jev/hosted/replit.example.toml','.replit')
 archive.write(root/'experiments/jev/hosted/replit.example.nix','replit.nix')
 archive.writestr('.gitignore',chr(10).join(['.runtime/','node_modules/','.env','.env.*','__pycache__/','']))
print(str(output))
`],{cwd:root,encoding:'utf8'});
if(result.status!==0){console.error(result.stderr);process.exitCode=1;}else process.stdout.write(result.stdout);
