from psychopy import visual, event, core, logging
from pathlib import Path
from participiant_info import get_info, DataManager
from UI import instructions, training, main_program
import yaml

logging.console.setLevel(logging.WARNING)

_dir = Path(__file__).parent
with open(_dir / 'config.yaml') as f:
    config = yaml.safe_load(f)

win = visual.Window(
    fullscr=config['display']['fullscreen'],
    color=config['display']['background'],
    units='norm',
    allowGUI=False,
    waitBlanking=True,
)
participant = get_info()
dm = DataManager(participant)

win.mouseVisible = False
mouse = event.Mouse(win=win)
instructions(win)
training(win, mouse, dm)
main_program(win, mouse, dm)

dm.save(config['data']['dir'])

win.close()
core.quit()
