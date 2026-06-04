import csv
import uuid
from datetime import datetime
from pathlib import Path
from psychopy import gui


def generate_id():
    """Generuje unikalny 8-znakowy ID uczestnika."""
    return str(uuid.uuid4())[:8].upper()


def get_info():
    subject_id = generate_id()
    myDlg = gui.Dlg(title="Informacje o uczestniku")
    myDlg.addText(f'ID uczestnika: {subject_id}')
    myDlg.addField('Wiek:')
    myDlg.addField('Płeć:', choices=["Mężczyzna", "Kobieta", "Inna"])
    ok_data = myDlg.show()
    if myDlg.OK:
        return {'id': subject_id, 'age': ok_data[0], 'gender': ok_data[1]}
    else:
        return None


class DataManager:
    def __init__(self, participant):
        self.subject_id = participant['id']
        self.age        = participant['age']
        self.gender     = participant['gender']
        self.start_time = datetime.now()
        self._trials    = []
        self._events    = []

    def log_trial(self, trial_num, is_practice, n, eq_type,
                  math_pct, memory_pct, counted,
                  displayed_letters, recalled_letters):
        self._trials.append({
            'subject_id':        self.subject_id,
            'age':               self.age,
            'gender':            self.gender,
            'trial':             trial_num,
            'practice':          is_practice,
            'n':                 n,
            'eq_type':           eq_type,
            'math_pct':          round(math_pct, 1),
            'memory_pct':        round(memory_pct, 1),
            'counted':           counted,
            'displayed_letters': ' '.join(displayed_letters),
            'recalled_letters':  ' '.join(recalled_letters),
        })

    def log_event(self, trial_num, event_type, content='',
                  response=None, correct=None, rt=None):
        self._events.append({
            'subject_id': self.subject_id,
            'trial':      trial_num,
            'timestamp':  datetime.now().isoformat(timespec='milliseconds'),
            'type':       event_type,
            'content':    content,
            'response':   '' if response is None else response,
            'correct':    '' if correct  is None else correct,
            'rt':         '' if rt       is None else round(rt, 3),
        })

    def save(self, data_dir='data'):
        Path(data_dir).mkdir(exist_ok=True)
        date_str = self.start_time.strftime('%Y%m%d_%H%M%S')
        base = Path(data_dir) / f'{self.subject_id}_{date_str}'
        self._write_csv(f'{base}_trials.csv', self._trials)
        self._write_csv(f'{base}_events.csv', self._events)

    @staticmethod
    def _write_csv(path, rows):
        if not rows:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
