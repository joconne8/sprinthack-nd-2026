"""Render a inspectable HTML preview from actual XLSX cells, never invented data."""
import argparse
import html
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p': 'http://schemas.openxmlformats.org/package/2006/relationships'}


def read_workbook(filename):
    with zipfile.ZipFile(filename) as archive:
        assert archive.testzip() is None
        shared = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            for item in ET.fromstring(archive.read('xl/sharedStrings.xml')).findall('m:si', NS):
                shared.append(''.join(t.text or '' for t in item.iterfind('.//m:t', NS)))
        targets = {r.attrib['Id']: r.attrib['Target'] for r in ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))}
        sheets = {}
        for sheet in ET.fromstring(archive.read('xl/workbook.xml')).findall('m:sheets/m:sheet', NS):
            target = targets[sheet.attrib['{'+NS['r']+'}id']]
            path = target.lstrip('/') if target.startswith('/') else 'xl/'+target
            rows = []
            for row in ET.fromstring(archive.read(path)).findall('m:sheetData/m:row', NS):
                values = {}
                for cell in row.findall('m:c', NS):
                    value = cell.find('m:v', NS)
                    if cell.attrib.get('t') == 's':
                        text = shared[int(value.text)] if value is not None else ''
                    elif cell.attrib.get('t') == 'inlineStr':
                        text = ''.join(t.text or '' for t in cell.findall('m:is/m:t', NS))
                    else:
                        text = value.text if value is not None else ''
                    column = re.sub(r'\d', '', cell.attrib['r'])
                    values[column] = text
                rows.append(values)
            sheets[sheet.attrib['name']] = rows
        return sheets


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workbook',required=True);parser.add_argument('--output',required=True);args=parser.parse_args()
    sheets=read_workbook(args.workbook)
    expected=['2026-09-%02d'%n for n in range(1,31)]
    assert all(name in sheets for name in expected), 'Workbook does not contain all 30 daily tabs'
    assert 'Monthly Summary' in sheets and 'Source Evidence' in sheets
    rows=sheets['Monthly Summary'];heads=rows[0];columns=sorted(heads,key=lambda s:(len(s),s))
    table='<thead><tr>'+''.join('<th>'+html.escape(heads.get(c,''))+'</th>' for c in columns)+'</tr></thead><tbody>'
    table+=''.join('<tr>'+''.join('<td>'+html.escape(row.get(c,''))+'</td>' for c in columns)+'</tr>' for row in rows[1:])+'</tbody>'
    provenance=sheets.get('Definitions',[])
    snapshot=next((r.get('B','') for r in provenance if r.get('A')=='Snapshot'),'Unknown snapshot')
    document='''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Actual Aimsigh workbook preview</title><style>*{box-sizing:border-box}body{background:#f6f5ef;color:#1c2521;font:19px Arial;margin:0;padding:42px}h1{font:42px Georgia;margin:12px 0}p{color:#5d655f;line-height:1.5}.eyebrow{color:#2e7d5b;font-size:15px;letter-spacing:2px}.sheet{background:white;border:1px solid #cbd6c8;padding:24px;border-radius:10px}table{width:100%;border-collapse:collapse;font-size:18px}th,td{padding:16px 12px;text-align:left;border:1px solid #dbe2d8}th{background:#e5eee2;color:#2e7d5b}tbody tr:nth-child(even){background:#fafbf8}.tabs{display:flex;gap:8px;overflow:hidden;margin-top:15px}.tabs span{white-space:nowrap;border:1px solid #cbd6c8;padding:9px 12px;background:white;font-size:14px}.tabs span:first-child{background:#2e7d5b;color:white}.mono{font:13px monospace;overflow-wrap:anywhere}</style></head><body><div class="eyebrow">ACTUAL EXPORTED XLSX · CELL-VALUE PREVIEW</div><h1>Amanda’s September workbook</h1><p>30 daily tabs · monthly aggregation · normalized records · modeled inputs · original-file evidence</p><div class="sheet"><h2>Monthly Summary</h2><table>'''+table+'''</table></div><div class="tabs"><span>Monthly Summary</span><span>Definitions</span>'''+''.join('<span>'+n+'</span>' for n in expected[:8])+'''<span>… 30 daily tabs</span><span>Source Evidence</span></div><p>Fictional sales; invented labor/shipping assumptions. This preview reads cached values from the downloaded workbook, not an Excel application screenshot.</p><p class="mono">Snapshot: '''+html.escape(snapshot)+'''</p></body></html>'''
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(document)
    target.with_suffix('.json').write_text(json.dumps({'workbook':Path(args.workbook).name,'snapshot_id':snapshot,'sheets':list(sheets),'daily_tabs':30,'monthly_rows':rows,'source':'actual XLSX cached cell values'},indent=2)+'\n')
    print('Previewed actual XLSX:',len(sheets),'sheets; 30 daily tabs; snapshot',snapshot)


if __name__=='__main__':main()
