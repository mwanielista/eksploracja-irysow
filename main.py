import PySimpleGUI as sg
import pandas as pd
import statistics
import matplotlib.pyplot as plt

class Main:
    def __init__(self):
        sg.theme('LightGray1')  # wybór motywu
        layout = [[sg.Text('Wczytaj plik CSV')],
                  [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse()],
                  [sg.Button('Wczytaj')],
                  [sg.Frame('Oblicz miary statystyczne',
                            [[sg.Checkbox('sepal length in cm', key='-SEPALLENGTH-'),
                              sg.Checkbox('sepal width in cm', key='-SEPALWIDTH-'),
                              sg.Checkbox('petal length in cm', key='-PETALLENGTH-'),
                              sg.Checkbox('petal width in cm', key='-PETALWIDTH-'),
                              sg.Checkbox('class', key='-CLASS-', default=True)]])],
                  [sg.Button('Oblicz')],
                  [sg.Multiline(size=(60, 10), key='-RESULT-', disabled=True)],
                  [sg.Text('Generuj wykres')],
                  [sg.Radio('sepal length vs. sepal width', 'RADIO1', key='-PLOT1-', enable_events=True),
                   sg.Radio('petal length vs. petal width', 'RADIO1', key='-PLOT2-', enable_events=True),
                   sg.Radio('sepal length vs. petal length', 'RADIO1', key='-PLOT3-', enable_events=True),
                   sg.Radio('sepal width vs. petal width', 'RADIO1', key='-PLOT4-', enable_events=True)],
                  [sg.Button('Generuj wykres')]]

        self.window = sg.Window('Aplikacja', layout)
        self.df = pd.DataFrame()

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == 'Wczytaj':
                try:
                    self.df = pd.read_csv(values['-FILE-'], delimiter=',', header=None, names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class'], dtype={'class': str})
                    sg.popup(f'Wczytano {len(self.df)} wierszy')
                except pd.errors.EmptyDataError:
                    sg.popup('Pusty plik!')
                except pd.errors.ParserError:
                    sg.popup('Niepoprawny format pliku!')
                except Exception as e:
                    sg.popup(f'Wystąpił błąd: {e}')
            if event == 'Oblicz':
                columns = []
                if values['-SEPALLENGTH-']:
                    columns.append('sepal_length')
                if values['-SEPALWIDTH-']:
                    columns.append('sepal_width')
                if values['-PETALLENGTH-']:
                    columns.append('petal_length')
                if values['-PETALWIDTH-']:
                    columns.append('petal_width')
                if values['-CLASS-']:
                    columns.append('class')
                if not columns:
                    sg.popup('Wybierz co najmniej jedną kolumnę!')
                else:
                    result = []
                    for col in columns:
                        try:
                            col_data = self.df[col].astype(float) if col != 'class' else self.df[col]
                            min_value = round(min(col_data), 2)
                            max_value = round(max(col_data), 2)
                            mean_value = round(statistics.mean(col_data), 2)
                            stdev_value = round(statistics.stdev(col_data), 2)
                            result.append(f"{col}:\nmin={min_value}\nmax={max_value}\nśrednia={mean_value}\nodchylenie standardowe={stdev_value}\nmediana={statistics.median(col_data)}\nmoda={statistics.mode(col_data)}")
                        except Exception as e:
                            result.append(f"{col}: wystąpił błąd: {e}")
                    self.window['-RESULT-'].update('\n\n'.join(result))
            if event == 'Generuj wykres':
                selected_plot = self.get_selected_plot(values)
                if selected_plot:
                    self.generate_plot(selected_plot)

        self.window.close()

    def get_selected_plot(self, values):
        plots = ['-PLOT1-', '-PLOT2-', '-PLOT3-', '-PLOT4-']
        selected_plot = None
        for plot in plots:
            if values[plot]:
                if selected_plot:
                    self.window[plot].update(False)
                else:
                    selected_plot = plot
        return selected_plot

    def generate_plot(self, selected_plot):
        x_label, y_label = self.get_plot_labels(selected_plot)
        plt.scatter(self.df[x_label], self.df[y_label])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f"{x_label} vs. {y_label}")
        plt.show()

    def get_plot_labels(self, selected_plot):
        if selected_plot == '-PLOT1-':
            return 'sepal_length', 'sepal_width'
        elif selected_plot == '-PLOT2-':
            return 'petal_length', 'petal_width'
        elif selected_plot == '-PLOT3-':
            return 'sepal_length', 'petal_length'
        elif selected_plot == '-PLOT4-':
            return 'sepal_width', 'petal_width'
        else:
            return None, None


if __name__ == '__main__':
    app = Main()
    app.run()
