import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib import style

class Graph():

    def __init__(self):
        self.__graph_data = None
        self.__fig = plt.figure()
        self.__is_first_display = True

    def display(self):

        if self.__is_first_display == True:
            ani = animation.FuncAnimation(self.__fig, self.__animate, interval=1000)
            self.__is_first_display = False
            
        plt.show()


    def __animate(self, i):

        style.use('fivethirtyeight')

        x = ['positive', 'negative', 'neutral']
        y = [self.__graph_data['positive'], self. __graph_data['negative'], self.__graph_data['neutral']]

        plt.bar(x, y, align='center')

        plt.title('Bitcoin Sentiment Analysis')
        plt.ylabel('Number of people')
        plt.xlabel('Sentiment')
        self.__fig.clear() 
        

    def set_graph_data(self,score):
       self. __graph_data = score





    