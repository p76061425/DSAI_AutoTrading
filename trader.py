import pandas as pd

def load_data(str):
    df = pd.read_csv(str, names=["open", "high", "low", "close"])
    return df

class Cross:
    def __init__(self):

        self.day = 0
        self.stock_num = 0
        self.stock_num_test = 0
        self.action = 0
        self.five_avg_list=[]
        self.twenty_avg_list=[]
        self.my_money = 0
        self.five_avg = 0
        self.twenty_avg = 0
        
    def predict(self,row):
        
        self.day += 1
        
        if(self.action==1):
            self.stock_num+=1
            self.my_money = self.my_money - row[0]
        elif(self.action==-1):
            self.stock_num -=1
            self.my_money = self.my_money + row[0]

        if(self.day<=20):
            self.stock_num = 0
            
            self.five_avg = sum(self.five_avg_list)/5
            self.twenty_avg = sum(self.twenty_avg_list)/20

            if(self.day<=5):
                self.five_avg_list.append(row[3])
            else:
                del self.five_avg_list[0]
                self.five_avg_list.append(row[3])

            self.twenty_avg_list.append(row[3])
            
            self.action = 0
            output_file.write(str(self.action)+'\n')

        else:

            del self.five_avg_list[0]
            self.five_avg_list.append(row[3])
            del self.twenty_avg_list[0]
            self.twenty_avg_list.append(row[3])

            self.five_avg = sum(self.five_avg_list)/5
            self.twenty_avg = sum(self.twenty_avg_list)/20

            if(self.five_avg > self.twenty_avg):
                self.stock_num_test+=1
                self.action = 1
            else:
                self.stock_num_test-=1
                self.action = -1

            if(self.stock_num_test>1):
                self.stock_num_test = 1
                self.action = 0

            elif(self.stock_num_test<-1):
                self.stock_num_test = -1
                self.action = 0

            output_file.write(str(self.action)+'\n')
        # Show result
        print(self.day, "act:",self.action,"stock:", self.stock_num, "money:",self.my_money,"五日:",self.five_avg,"二十日:",self.twenty_avg,"開盤價:",row[0])
        

if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    parser.add_argument('-f',
                        default=None,
                        help='')
    args = parser.parse_args()
    
    # The following part is an example.
    # You can modify it at will.
    training_data = load_data(args.training)
    
#    trader = Trader()
#    trader.train(training_data)
    cross = Cross ()
    testing_data = load_data(args.testing)
    with open(args.output, 'w') as output_file:
        for row in testing_data.values:
            cross.predict(row)
            
            # this is your option, you can leave it empty.
            #trader.re_training()
            
    if(cross.stock_num==1):
        cross.my_money = cross.my_money+372.8301
        
    elif(cross.stock_num==-1):
        cross.my_money = cross.my_money-372.8301

    print("end_money:",cross.my_money)