import tkinter as ttk
import numpy as np
import sounddevice as sd


class Menu_window:
    def __init__(self, title, icon):
        self.window = ttk.Tk()
        self.window.title(title)
        self.window.state('zoomed')
        self.window.iconphoto(True, ttk.PhotoImage(file=icon))
        self.window['bg'] = 'bisque2'
        self.window.config(cursor='heart')
        self.window.grab_set()

    pass


class Sound:
    def change_frequency(self, newVal):
        self.frequency_label['text'] = f'Frequency: {newVal}'

    def change_volume(self, newVal):
        self.volume_label['text'] = f'Volume: {newVal}'

    def delete_all(self):
        Creator.sounds.remove(self)
        self.frequency_label.destroy()
        self.new_scale_frequency.destroy()
        self.volume_label.destroy()
        self.new_scale_volume.destroy()
        self.delete_sound.destroy()
        Creator.counter -= 1

    def __init__(self, window):
        self.frequency_label = ttk.Label(
            window,
            text='Frequency: 0',
            font=('Cooper Black', 11),
            background='bisque2',
            foreground='SaddleBrown'
        )
        self.new_scale_frequency = ttk.Scale(
            window,
            background='bisque3',
            foreground='SaddleBrown',
            orient='horizontal',
            length=600,
            from_=0,
            to=4000,
            command=self.change_frequency
        )
        self.volume_label = ttk.Label(
            window,
            text='Volume: 0',
            font=('Cooper Black', 11),
            background='bisque2',
            foreground='SaddleBrown'
        )
        self.new_scale_volume = ttk.Scale(
            window,
            background='bisque3',
            foreground='SaddleBrown',
            orient='horizontal',
            length=600,
            from_=0,
            to=1000,
            command=self.change_volume
        )
        self.delete_sound = ttk.Button(
            window,
            text='Delete',
            font=('Cooper Black', 12),
            background='bisque3',
            foreground='SaddleBrown',
            command=self.delete_all
        )
        self.frequency_label.pack()
        self.new_scale_frequency.pack()
        self.volume_label.pack()
        self.new_scale_volume.pack()
        self.delete_sound.pack()
        Creator.counter += 1

    pass


class New_window:
    def __init__(self, title):
        self.window = ttk.Toplevel()
        self.window.title(title)
        self.window.state('zoomed')
        self.window['bg'] = 'bisque2'
        self.window.withdraw()
        self.window.config(cursor='heart')
        self.sounds = []
        self.counter = 0
        self.Play_Stop_button = ttk.Button(
            self.window,
            text='Play',
            font=('Cooper Black', 20),
            background='bisque3',
            foreground='SaddleBrown',
            relief=ttk.RIDGE,
            command=self.play_stop_sound
        )
        self.Play_Stop_button.pack(side=ttk.BOTTOM)

    def dismiss(self):
        self.window.grab_release()
        self.window.withdraw()
        Harmony.window.state('zoomed')
        Harmony.window.grab_set()

    def open(self):
        Harmony.window.grab_release()
        Harmony.window.withdraw()
        self.window.state('zoomed')
        self.window.grab_set()

    def add_sound(self):
        if self.counter < 4:
            new_sound = Sound(self.window)
            self.sounds.append(new_sound)

    def play_stop_sound(self):
        if self.Play_Stop_button['text'] == 'Play':
            if self.counter != 0:
                duration = 10
                samplerate = 44100
                num_samples = int(round(duration * samplerate))
                all_sounds = np.zeros(num_samples, dtype=np.int16)
                for sound in self.sounds:
                    sound_buffer = np.zeros(num_samples, dtype=np.int16)
                    frequency = sound.new_scale_frequency.get()
                    amp = 32767 / 1000 * sound.new_scale_volume.get()
                    for sample_num in range(num_samples):
                        t = float(sample_num) / samplerate
                        sine = amp * np.sin(2 * np.pi * frequency * t)
                        sound_buffer[sample_num] = sine
                    all_sounds += sound_buffer
                sd.play(all_sounds)
                self.Play_Stop_button['text'] = 'Stop'

        else:
            sd.stop()
            self.Play_Stop_button['text'] = 'Play'

    pass


Harmony = Menu_window(title='Harmony Creator', icon='Menu_Icon.png')
Creator = New_window(title='Harmony Creator')
name = ttk.Label(
    Harmony.window,
    text='Harmony Creator',
    font=('Cooper Black', 60),
    background='bisque2',
    foreground='SaddleBrown'
)
name.pack(padx=100, pady=100)
name_of_creator = ttk.Label(
    Harmony.window,
    text='created by GGalim',
    font=('Cooper Black', 14),
    background='bisque2',
    foreground='SaddleBrown'
)
name_of_creator.pack(side=ttk.BOTTOM, anchor='sw')

main_button = ttk.Button(
    Harmony.window,
    text='Create my own harmony',
    font=('Cooper Black', 30),
    background='bisque3',
    foreground='SaddleBrown',
    relief=ttk.RIDGE,
    command=Creator.open
)
main_button.pack()
close_Main = ttk.Button(
    Creator.window,
    text='Back',
    font=('Cooper Black', 15),
    background='bisque3',
    foreground='SaddleBrown',
    relief=ttk.RIDGE,
    command=Creator.dismiss
)
close_Main.pack(side=ttk.TOP, anchor='nw')
Add_button = ttk.Button(
    Creator.window,
    text='Add new sound',
    font=('Cooper Black', 30),
    background='bisque3',
    foreground='SaddleBrown',
    relief=ttk.RIDGE,
    command=Creator.add_sound)
Add_button.pack()
Harmony.window.mainloop()
