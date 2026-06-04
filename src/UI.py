from psychopy import visual, core, event
from pathlib import Path
import random
import yaml
from engine import logic
from participiant_info import DataManager

_dir = Path(__file__).parent

with open(_dir / 'config.yaml') as f:
    config = yaml.safe_load(f)
with open(_dir / 'instructions.txt') as f:
    instructions_text = f.read()


def quit_program(win):
    win.close()
    core.quit()


def wait_for_space(win):
    keys = event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in keys:
        quit_program(win)


def instructions(win):
    pages = instructions_text.split('---')

    stim = visual.TextStim(
        win, text='',
        color=config['display']['text_color'],
        height=config['display']['text_height'],
        wrapWidth=1.6, alignText='center', pos=(0, 0.1)
    )
    counter = visual.TextStim(
        win, text='', color='gray',
        height=config['display']['text_height'] * 0.7,
        pos=(0, -0.82)
    )

    win.mouseVisible = False
    for i, page in enumerate(pages):
        stim.text = page.strip()
        counter.text = f'{i + 1} / {len(pages)}'
        event.clearEvents()
        stim.draw()
        counter.draw()
        win.flip()
        wait_for_space(win)


def break_screen(win):
    stim = visual.TextStim(
        win,
        text='Przerwa! Naciśnij spację, aby kontynuować.',
        color=config['display']['text_color'],
        height=config['display']['text_height'],
        wrapWidth=1.5,
    )
    win.mouseVisible = False
    clock = core.Clock()
    event.clearEvents()
    while clock.getTime() < config['timing']['break_max']:
        stim.draw()
        win.flip()
        keys = event.getKeys(keyList=['space', 'escape'])
        if 'escape' in keys:
            quit_program(win)
        if 'space' in keys:
            break


def recall_screen(win, mouse, displayed_letters, correct_ratio):
    pool   = config['letters']['pool']
    btn_c  = config['display']['btn_color']
    btn_h  = config['display']['btn_hover']
    btn_s  = config['display']['btn_selected']
    cell_w, cell_h = 0.22, 0.17
    step_x, step_y = 0.26, 0.21

    positions = [
        (-(3/2)*step_x + c*step_x, 0.31 - r*step_y)
        for r in range(3) for c in range(4)
    ]

    btn_rects  = []
    btn_labels = []
    for letter, pos in zip(pool, positions):
        btn_rects.append(visual.Rect(win, width=cell_w, height=cell_h, pos=pos,
                                     fillColor=btn_c, lineColor='white'))
        btn_labels.append(visual.TextStim(win, text=letter, color='white',
                                          height=0.1, pos=pos, bold=True))

    title         = visual.TextStim(win, text='Wskaż zapamiętane litery w kolejności',
                                    color='white', height=0.07, pos=(0, 0.78))
    math_text     = visual.TextStim(win, text=f'Matematyka: {correct_ratio:.1f}%',
                                    color='lime', height=0.06, pos=(0.72, 0.92))
    selected_text = visual.TextStim(win, text='—', color='yellow', height=0.09,
                                    pos=(0, -0.38), bold=True)
    status        = visual.TextStim(win, text='', color='gray', height=0.06, pos=(0, -0.55))

    undo_rect     = visual.Rect(win, width=0.3,  height=0.12, pos=(-0.55, -0.78),
                                fillColor='brown', lineColor='white')
    undo_label    = visual.TextStim(win, text='Cofnij',    color='white', height=0.07, pos=(-0.55, -0.78))
    confirm_rect  = visual.Rect(win, width=0.35, height=0.12, pos=(0.55, -0.78),
                                fillColor='darkgreen', lineColor='white')
    confirm_label = visual.TextStim(win, text='Zatwierdź', color='white', height=0.07, pos=(0.55, -0.78))

    n = len(displayed_letters)
    selected = []
    win.mouseVisible = True
    mouse.setPos([0, 0])
    event.clearEvents()
    mouse_was_down = mouse.getPressed()[0]

    while True:
        pressing = mouse.getPressed()[0]
        just_clicked = pressing and not mouse_was_down

        if just_clicked:
            if undo_rect.contains(mouse) and selected:
                selected.pop()
            elif confirm_rect.contains(mouse) and selected:
                break
            else:
                selected_indices = {idx for idx, _ in selected}
                for i, rect in enumerate(btn_rects):
                    if i not in selected_indices and len(selected) < n and rect.contains(mouse):
                        selected.append((i, pool[i]))
                        break

        mouse_was_down = pressing

        selected_indices = {idx for idx, _ in selected}
        for i, rect in enumerate(btn_rects):
            if i in selected_indices:
                rect.fillColor = btn_s
            elif rect.contains(mouse):
                rect.fillColor = btn_h
            else:
                rect.fillColor = btn_c

        selected_text.text = '  →  '.join(l for _, l in selected) if selected else '—'
        undo_rect.fillColor    = 'orange' if undo_rect.contains(mouse)    else 'brown'
        confirm_rect.fillColor = 'green'  if confirm_rect.contains(mouse) else 'darkgreen'
        status.text = f'Wybrano: {len(selected)}/{n}'

        title.draw()
        math_text.draw()
        for rect, label in zip(btn_rects, btn_labels):
            rect.draw()
            label.draw()
        selected_text.draw()
        undo_rect.draw()
        undo_label.draw()
        if selected:
            confirm_rect.draw()
            confirm_label.draw()
        status.draw()
        win.flip()

        if 'escape' in event.getKeys(keyList=['escape']):
            quit_program(win)

    recalled = [letter for _, letter in selected]
    memory_accuracy = round(
        sum(r == d for r, d in zip(recalled, displayed_letters)) / len(displayed_letters) * 100, 1
    )
    return recalled, memory_accuracy


def training_complete_screen(win):
    stim = visual.TextStim(
        win,
        text='Trening zakończony!\n\nWyniki treningu nie są wliczane do Twojego wyniku.\n\nNaciśnij SPACJĘ, aby rozpocząć właściwe badanie.',
        color=config['display']['text_color'],
        height=config['display']['text_height'],
        wrapWidth=1.6, alignText='center',
    )
    win.mouseVisible = False
    event.clearEvents()
    stim.draw()
    win.flip()
    wait_for_space(win)


def training(win, mouse, dm):
    for trial_num in range(1, 4):
        n = random.randint(3, 7)
        math_pct, displayed_letters = logic(n, win, mouse)
        recalled, memory_pct = recall_screen(win, mouse, displayed_letters, math_pct)
        dm.log_trial(trial_num, True, n, 'mixed', math_pct, memory_pct,
                     math_pct >= config['scoring']['math_threshold'],
                     displayed_letters, recalled)
        break_screen(win)
    training_complete_screen(win)


def main_program(win, mouse, dm):
    sizes = [3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7]
    random.shuffle(sizes)
    for trial_num, n in enumerate(sizes, start=1):
        math_pct, displayed_letters = logic(n, win, mouse)
        recalled, memory_pct = recall_screen(win, mouse, displayed_letters, math_pct)
        dm.log_trial(trial_num, False, n, 'mixed', math_pct, memory_pct,
                     math_pct >= config['scoring']['math_threshold'],
                     displayed_letters, recalled)
        break_screen(win)
