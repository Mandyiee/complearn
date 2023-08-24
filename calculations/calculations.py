from typing import Any
import csv
import pandas as pd
import io
import csv
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import threading
import matplotlib.pyplot as plt
from django.core.files.uploadedfile import InMemoryUploadedFile
from composite.models import Composite

class Calculation(object):
    fibre = 90
    matrix = 10

    def __init__(self, tensileStrengthFibre, tensileStrengthMatrix, youngModulusFibre, youngModulusMatrix, desired_tensile_strength, desired_young_modulus, opt,comp_id):
        self.tsf = int(tensileStrengthFibre)
        self.tsm = int(tensileStrengthMatrix)
        self.ymf = int(youngModulusFibre)
        self.ymm = int(youngModulusMatrix)
        self.dts = int(desired_tensile_strength)
        self.dym = int(desired_young_modulus)
        self.opt = opt
        self.id = comp_id

    def __call__(self, *args, **kwds):
        print('starting')

        # Create a DataFrame to store data points for training the model
        data = self.generate_training_data()

        # Separate the input features (X) and the target variables (y)
        X = data.iloc[:, :2]  # Columns 1 and 2
        y = data.iloc[:, 2:]  # Columns 3 and 4

        # Train a Decision Tree regressor model
        model = DecisionTreeRegressor(random_state=42)
        model.fit(X, y)

        # Predict using the trained model
        predicted_values = model.predict(X)

        # Find the closest match to the desired values
        min_distance = float('inf')
        best_row_idx = None
        for i, row in enumerate(predicted_values):
            distance = np.sqrt((row[0] - self.dts)**2 + (row[1] - self.dym)**2)
            if distance < min_distance:
                min_distance = distance
                best_row_idx = i

        best_row = data.iloc[best_row_idx]
        best_row_dict = {'percentage of fibre': best_row['percentage of fibre'],
                         'percentage of matrix': best_row['percentage of matrix'],
                         'tensile strength': best_row['tensile strength'],
                         'young modulus': best_row['young modulus']}

        print(best_row_dict)
        try:
            composite = Composite.objects.get(id=self.id)
            composite.best_fibre_percentage =best_row['percentage of fibre'] 
            composite.best_matrix_percentage = best_row['percentage of matrix']
            composite.best_young_modulus = best_row['young modulus']
            composite.best_tensile_strength = best_row['tensile strength']
            composite.save()
        except Exception as e:
            print(e)
        # thread1 = threading.Thread(target=self.fiber_percentage_against_tensile_strength,args=[data])
        # thread2 = threading.Thread(target=self.fiber_percentage_against_young_modulus,args=[data])
        # thread3 = threading.Thread(target=self.matrix_percentage_against_tensile_strength,args=[data])
        # thread4 = threading.Thread(target=self.matrix_percentage_against_young_modulus,args=[data])

        # thread1.start()
        # thread2.start()
        # thread3.start()
        # thread4.start()
        self.fiber_percentage_against_tensile_strength(data)
        self.fiber_percentage_against_young_modulus(data)
        self.matrix_percentage_against_tensile_strength(data)
        self.matrix_percentage_against_young_modulus(data)
        
        return best_row_dict

    def generate_training_data(self):
        # Create an in-memory file-like object for writing CSV data
        output_data = io.StringIO()

        # Write CSV data to the in-memory file-like object
        outputWriter = csv.writer(output_data)

        outputWriter.writerow(['percentage of fibre', 'percentage of matrix', 'tensile strength', 'young modulus'])
        for x in range(9):
            ts = self.tensile_strength((self.fibre / 100), (self.matrix / 100))
            ym = self.young_modulus((self.fibre / 100), (self.matrix / 100))
            outputWriter.writerow([self.fibre, self.matrix, ts, ym])
            self.fibre -= 10
            self.matrix += 10

        # Reset the file-like object position to the beginning
        output_data.seek(0)

        # Load the data from the CSV file
        data = pd.read_csv(output_data)
        print(data)

        return data

    def tensile_strength(self, fp, mp):
        if self.opt == 'long':
            ts = (self.tsf * fp) + (self.tsm * mp)
            return ts
        else:
            ts = (self.tsf * self.tsm) / ((self.tsf * mp) + (self.tsm * fp))
            return ts

    def young_modulus(self, fp, mp):
        if self.opt == 'long':
            ym = (self.ymf * fp) + (self.ymm * mp)
            return ym
        else:
            ym = (self.ymf * self.ymm) / ((self.ymf * mp) + (self.ymm * fp))
            return ym
 
    def fiber_percentage_against_tensile_strength(self,data):
        
        composite = Composite.objects.get(id=self.id)
        print(self.id)
        plt.plot(data.iloc[0], data.iloc[2], marker='o', linestyle='-', color='b')
        plt.title('Fiber Percentage vs Tensile Strength')
        plt.xlabel('Percentage of Fiber')
        plt.ylabel('Tensile Strength')
        plt.grid(True)

        # Save plot as image
       
        
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png')
        plt.close() 
        
        # Create an InMemoryUploadedFile from the BytesIO buffer
        image_file = InMemoryUploadedFile(image_buffer, None, 'fiberts.png', 'image/png', image_buffer.tell(), None)
        composite.fibre_percentage_against_tensile_strength.save('fiberts.png', image_file, save=True)

        
    def fiber_percentage_against_young_modulus(self,data):
        
        composite = Composite.objects.get(id=self.id)
        print(self.id)
        plt.plot(data.iloc[0], data.iloc[3], marker='o', linestyle='-', color='b')
        plt.title('Fiber Percentage vs Young Modulus')
        plt.xlabel('Percentage of Fiber')
        plt.ylabel('Young Modulus')
        plt.grid(True)

        # Save plot as image
       
        
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png')
        plt.close() 
        
        image_file = InMemoryUploadedFile(image_buffer, None, 'fiberym.png', 'image/png', image_buffer.tell(), None)
        composite.fibre_percentage_against_young_modulus.save('fiberym.png', image_file, save=True)

        
    def matrix_percentage_against_tensile_strength(self,data):
        
        composite = Composite.objects.get(id=self.id)
        print(self.id)
        plt.plot(data.iloc[1], data.iloc[2], marker='o', linestyle='-', color='b')
        plt.title('Matrix Percentage vs Tensile Strength')
        plt.xlabel('Percentage of Matrix')
        plt.ylabel('Tensile Strength')
        plt.grid(True)

        # Save plot as image
       
        
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png')
        plt.close() 
        
        image_file = InMemoryUploadedFile(image_buffer, None, 'matrixts.png', 'image/png', image_buffer.tell(), None)
        composite.matrix_percentage_against_tensile_strength.save('matrixts.png', image_file, save=True)

        
    def matrix_percentage_against_young_modulus(self,data):
        
        composite = Composite.objects.get(id=self.id)
        print(self.id)
        plt.plot(data.iloc[0], data.iloc[2], marker='o', linestyle='-', color='b')
        plt.title('Matrix Percentage vs Young Modulus')
        plt.xlabel('Percentage of Matrix')
        plt.ylabel('Young Modulus')
        plt.grid(True)

        # Save plot as image
       
        
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png')
        plt.close() 
        
        image_file = InMemoryUploadedFile(image_buffer, None, 'matrixym.png', 'image/png', image_buffer.tell(), None)
        composite.matrix_percentage_against_young_modulus.save('matrixym.png', image_file, save=True)

        
    def fiber_percentage_against_tensile_strength_against_young_modulus(self,data):
        
        composite = Composite.objects.get(id=self.id)
        print(self.id)
        plt.plot(data.iloc[0], data.iloc[2], marker='o', linestyle='-', color='b')
        plt.title('Fiber Percentage vs Tensile Strength')
        plt.xlabel('Percentage of Fiber')
        plt.ylabel('Tensile Strength')
        plt.grid(True)

        # Save plot as image
       
        
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png')
        plt.close() 
        
        # Create an InMemoryUploadedFile from the BytesIO buffer
        image_file = InMemoryUploadedFile(image_buffer, None, 'graph.png', 'image/png', image_buffer.tell(), None)
        composite.fibre_percentage_against_tensile_strength = image_file
        composite.save()

  

    # ... rest of your code

# class Calculation(object):
#     fibre = 90
#     matrix = 10

#     def __init__(self, tensileStrengthFibre, tensileStrengthMatrix, youngModulusFibre, youngModulusMatrix,desired_tensile_strength,desired_young_modulus,opt):
#         self.tsf = int(tensileStrengthFibre)
#         self.tsm = int(tensileStrengthMatrix)
#         self.ymf = int(youngModulusFibre)
#         self.ymm = int(youngModulusMatrix)
#         self.dts= int(desired_tensile_strength)
#         self.dym = int(desired_young_modulus)
#         self.opt = opt

#     def __call__(self, *args, **kwds):
#         print('starting')
#         # Create an in-memory file-like object for writing CSV data
#         self.output_data = io.StringIO()
    

#         # Write CSV data to the in-memory file-like object
#         outputWriter = csv.writer(self.output_data)
        
#         outputWriter.writerow(['percentage of fibre', 'percentage of matrix', 'tensile strength', 'young modulus'])
#         for x in range(10):
#             ts = self.tensile_strength((self.fibre / 100), (self.matrix / 100))
#             ym = self.young_modulus((self.fibre / 100), (self.matrix / 100))
#             outputWriter.writerow([self.fibre, self.matrix, ts, ym])
#             self.fibre -= 10
#             self.matrix += 10
            
#         # Reset the file-like object position to the beginning
#         self.output_data.seek(0)
        
        
        
#         # Load the data from the CSV file
#         data = pd.read_csv(self.output_data)
#         print(data)
#         # Separate the input features (X) and the target variables (y)
#         X = data.iloc[:, :2]  # Columns 1 and 2
#         y = data.iloc[:, 2:]  # Columns 3 and 4

#         # Create and train the decision tree regressor
#         model = DecisionTreeRegressor()
#         model.fit(X, y)

#         # Set the desired tensile strength and young modulus values
#         desired_tensile_strength = self.dts
#         desired_young_modulus = self.dym

#         # Create a new data point with the desired values
#         desired_data = pd.DataFrame([[desired_tensile_strength, desired_young_modulus]])

#         # Use the trained model to predict the best row
#         predicted_row_index = model.predict(desired_data).argmin()
#         best_row = data.iloc[predicted_row_index]

#         print("Best row:", best_row)
        
#         # Convert the best_row DataFrame to a dictionary
#         best_row_dict = best_row.to_dict()

#         print(best_row_dict)
#         return best_row_dict

        

#     def tensile_strength(self, fp, mp):
#         if self.opt == 'long':
#             ts = (self.tsf * fp) + (self.tsm * mp)
#             return ts
#         else:
#             ts = (self.tsf* self.tsm )/((self.tsf * mp) + (self.tsm * fp))
#             return ts
        
#     def young_modulus(self, fp, mp):
#         if self.opt == 'long':
#             ym = (self.ymf * fp) + (self.ymm * mp)
#             return ym
#         else:
#             ym = (self.ymf* self.ymm )/((self.ymf * mp) + (self.ymm * fp))
#             return ym
    
    
        
  