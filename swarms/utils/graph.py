"""Plot and Save the results."""

from matplotlib import pyplot as plt
import pandas as pd

plt.style.use('fivethirtyeight')


class Graph:

    def __init__(self, directory, fname, fields):
        self.directory = directory
        self.fname = fname
        self.fields = fields
        self.data = self.load_file()
        self.mean = self.data[self.data['header'] == 'MEAN']
        self.std = self.data[self.data['header'] == 'STD']
        self.overall = self.data[self.data['header'] == 'OVERALL']['fitness'].values
        self.diverse = self.data[self.data['header'] == 'DIVERSE']['fitness'].values
        self.explore = self.data[self.data['header'] == 'EXPLORE']['fitness'].values
        self.forge = self.data[self.data['header'] == 'FORGE']['fitness'].values

    def gen_best_plots(self):
        fig = plt.figure()
        i = 1
        for field in self.fields:
            mean = self.mean[field].values
            std = self.std[field].values
            field_max = mean + std
            field_min = mean - std
            xvalues = range(1, len(mean) + 1)
            ax1 = fig.add_subplot(2, 1, i)
            i += 1
            # Plotting mean and standard deviation
            ax1.plot(xvalues, mean, color='blue', label='Mean ' + field)
            ax1.fill_between(
                xvalues, field_max, field_min, color='DodgerBlue', alpha=0.3)

            ax1.plot(xvalues, self.overall, color='red', label='Overall')
            ax1.plot(xvalues, self.diverse, color='green', label='Diversity')
            ax1.plot(xvalues, self.explore, color='orange', label='Explore')
            ax1.plot(xvalues, self.forge, color='indigo', label='Forge')
            plt.xlim(0, len(mean))
            ax1.set_xlabel('Steps')
            ax1.set_xlabel('Fitness')
            ax1.set_title('Fitness function')

        fig.savefig(self.directory + '/best.pdf')

    def load_file(self):
        data = pd.read_csv(self.directory + '/' + self.fname, sep='|')
        return data

    def save_step_graph(self, filename, fields):
        pass


class GraphACC:

    def __init__(self, directory, fname):
        self.directory = directory
        self.fname = fname
        self.data = self.load_file()
        self.step = self.data['step'].values
        self.performance = self.data['fitness'].values

    def gen_plot(self):
        fig = plt.figure()
        xvalues = self.step
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(xvalues, self.performance, color='red', label='Values')
        ax1.set_xlabel('Steps')
        ax1.set_xlabel('Performance')

        ax1.set_title('ACC Graph')

        fig.savefig(self.directory + '/acc.pdf')

    def load_file(self):
        data = pd.read_csv(self.directory + '/' + self.fname, sep='|')
        return data

    def save_step_graph(self, filename, fields):
        pass
