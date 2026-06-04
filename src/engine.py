from psychopy import visual, event, core
from pathlib import Path
import random
import yaml

_dir = Path(__file__).parent
with open(_dir / 'config.yaml') as f:
    config = yaml.safe_load(f)

LETTERS      = config['letters']['pool']
letter_max   = config['timing']['letter_max']
equation_max = config['timing']['equation_max']
blank_min    = config['timing']['blank_min']
blank_max    = config['timing']['blank_max']
equations    = config['equations']
text_color   = config['display']['text_color']
btn_color    = config['display']['btn_color']
btn_hover    = config['display']['btn_hover']


def quit_program(win):
    win.close()
    core.quit()


def draw_letter(letter_stim, letter, win, max_time):
    win.mouseVisible = False
    letter_stim.text = letter
    event.clearEvents()
    clock = core.Clock()
    while clock.getTime() < max_time:
        letter_stim.draw()
        win.flip()
        keys = event.getKeys(keyList=['space', 'escape'])
        if 'escape' in keys:
            quit_program(win)
        if 'space' in keys:
            break


def draw_equation(eq_stim, btn_true_rect, btn_true_label,
                  btn_false_rect, btn_false_label,
                  equation, win, mouse, max_time):
    win.mouseVisible = True
    mouse.setPos([0, 0])
    eq_stim.text = equation
    event.clearEvents()
    clock = core.Clock()
    response = None
    mouse_was_down = False

    while clock.getTime() < max_time:
        btn_true_rect.fillColor  = btn_hover if btn_true_rect.contains(mouse)  else btn_color
        btn_false_rect.fillColor = btn_hover if btn_false_rect.contains(mouse) else btn_color

        eq_stim.draw()
        btn_true_rect.draw()
        btn_true_label.draw()
        btn_false_rect.draw()
        btn_false_label.draw()
        win.flip()

        # Kliknięcie wykrywane przy puszczeniu przycisku myszy
        pressing_true  = mouse.isPressedIn(btn_true_rect)
        pressing_false = mouse.isPressedIn(btn_false_rect)
        if pressing_true and not mouse_was_down:
            response = True
            break
        if pressing_false and not mouse_was_down:
            response = False
            break
        mouse_was_down = pressing_true or pressing_false

        if 'escape' in event.getKeys(keyList=['escape']):
            quit_program(win)

    return response


def logic(n, win, mouse):
    letter_stim    = visual.TextStim(win, text='', color=text_color, height=0.4)
    eq_stim        = visual.TextStim(win, text='', color=text_color, height=0.12, pos=(0, 0.2))
    btn_true_rect  = visual.Rect(win, width=0.35, height=0.15, pos=(-0.35, -0.5),
                                 fillColor=btn_color, lineColor=text_color)
    btn_true_label = visual.TextStim(win, text='PRAWDA', color=text_color, height=0.08, pos=(-0.35, -0.5))
    btn_false_rect = visual.Rect(win, width=0.35, height=0.15, pos=(0.35, -0.5),
                                 fillColor=btn_color, lineColor=text_color)
    btn_false_label = visual.TextStim(win, text='FAŁSZ', color=text_color, height=0.08, pos=(0.35, -0.5))

    correct = 0
    displayed_letters = random.sample(LETTERS, n)

    for letter in displayed_letters:
        eq_text, eq_correct = random.choice(list(equations.items()))

        draw_letter(letter_stim, letter, win, max_time=letter_max)

        win.flip()
        core.wait(random.uniform(blank_min, blank_max))

        response = draw_equation(
            eq_stim, btn_true_rect, btn_true_label,
            btn_false_rect, btn_false_label,
            eq_text, win, mouse, max_time=equation_max
        )

        win.flip()
        core.wait(random.uniform(blank_min, blank_max))

        if response == eq_correct:
            correct += 1

    correct_ratio = round(correct / n * 100, 1)
    return correct_ratio, displayed_letters
