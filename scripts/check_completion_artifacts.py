"""Check promised documents/evidence exist; never infer task acceptance."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ['GOV-01', 'GOV-02', 'GOV-03', 'GOV-04', 'ENG-01', 'ENG-02', 'ENG-05'] + [f'DAT-{n:02d}' for n in range(1, 10)]


def main():
    checked = []
    errors = []
    for task in TASKS:
        packet = (ROOT / f'ProjectManagement/agent-assignments/tasks/{task}.md').read_text()
        block = packet.split('## Required output artifacts\n', 1)[1].split('\n## ', 1)[0]
        # Enforce exact review artifacts, not suggested implementation directories.
        # Actual Python test/implementation lane mappings are in development.md.
        for line in block.splitlines():
            if line.startswith('- '):
                match = re.match(r'- ((?:planning|reports)/[^\s]+)', line)
                if match:
                    relative = match.group(1)
                    if not (ROOT / relative).exists():
                        errors.append(f'{task}: missing {relative}')
                    else:
                        checked.append(relative)
        record_path = ROOT / f'reports/{task}/verification.json'
        record = json.loads(record_path.read_text())
        if record.get('accepted') is not False:
            errors.append(f'{task}: implementation report must not self-accept')
        for artifact in record.get('artifacts', []):
            if not (ROOT / artifact).exists():
                errors.append(f'{task}: evidence artifact missing {artifact}')
        evidence = record_path.parent / record['evidence']
        if not evidence.is_file():
            errors.append(f'{task}: missing verification reference {evidence}')
    print(json.dumps({'passed': not errors, 'tasks_checked': TASKS,
                      'required_artifacts_checked': len(checked), 'errors': errors,
                      'limit': 'Presence/reference check only; not human or independent acceptance'}, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
