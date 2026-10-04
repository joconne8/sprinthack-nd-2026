'use strict';
const fs = require('node:fs');
const crypto = require('node:crypto');
const {spawnSync} = require('node:child_process');
function verifyFile(result, start, end) {
  if (crypto.createHash('sha256').update(fs.readFileSync(result.file)).digest('hex') !== result.manifest.file_checksum)
    throw new Error('Checksum mismatch');
  const check = spawnSync('python3', ['-c', `import csv,json,sys
with open(sys.argv[1], newline='', encoding='utf-8-sig') as f:
 r=csv.DictReader(f)
 assert {'reporting_date','synthetic'}.issubset(r.fieldnames or []), 'Missing CSV headers'
 rows=list(r)
 assert len(rows)==int(sys.argv[4]), 'Row count mismatch'
 assert rows, 'No rows in requested report'
 for row in rows:
  assert row['synthetic']=='true', 'Non-synthetic row'
  assert sys.argv[2]<=row['reporting_date']<=sys.argv[3], 'Row outside requested dates'
 print(json.dumps({'rows_checked':len(rows),'dates_checked':True,'synthetic_checked':True}))`, result.file, start, end, String(result.manifest.row_count)], {encoding: 'utf8', timeout: 5000});
  if (check.status !== 0) throw new Error('CSV content validation failed');
  return {...JSON.parse(check.stdout), checksum_matches: true};
}
module.exports = {verifyFile};
