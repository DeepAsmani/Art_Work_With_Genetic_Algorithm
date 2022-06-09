"""

Draw image with Polygons(like Triangle) using genetic algorithm

"""
from PIL import Image, ImageDraw
import numpy as np
import random
import cv2
import threading as t

nup = 10000000


def mainclass(path, st, filename, totalP, imgshape="Polygon"):
    cnterr = 0
    num_polygons = 50
    num_generations = nup
    num_chromosomes = 100

    imgOrigin = path
    width, height, temp = imgOrigin.shape
    aImage = np.array(imgOrigin)
    aImage = aImage.astype('int32')

    def to_img(chromosome):

        img = Image.new('RGB', (height, width), (255, 255, 255))
        draw = ImageDraw.Draw(img, 'RGBA')

        for polygon in chromosome:
            colour = (polygon[6], polygon[7], polygon[8], polygon[9])
            if imgshape == "Polygon":
                points = (polygon[0], polygon[1], polygon[2],
                          polygon[3], polygon[4], polygon[5])
                draw.polygon(points, fill=colour, outline=None)
            if imgshape == "Ellipse":
                points = (polygon[0], polygon[1], polygon[2],
                          polygon[3])
                draw.ellipse(points, fill=colour, outline=None)
        tempimg = np.array(img)
        out = cv2.cvtColor(tempimg, cv2.COLOR_RGB2BGR)
        return out

    def evaluate(img_1, img_2):
        # find fitness of two images like(original image array - new possible image array)
        #eval = 0
        #aimg = np.array(img_2)
        #aimg = aimg.astype('int32')
        #errorMatrix = abs(aImage-aimg)
        #eval = np.sum(errorMatrix)

        err = np.sum((img_1.astype("float") -
                      img_2.astype("float")) ** 2)
        err /= float(img_1.shape[0] * img_2.shape[1])

        return err  # eval

    def select(evals, candidates):
        parent_1 = candidates[evals.index(sorted(evals)[0])]
        parent_2 = candidates[evals.index(sorted(evals)[1])]
        return parent_1, parent_2

    def crossover(parent_1, parent_2):
        # select_matrix = np.ones(shape = parent_1.shape, dtype = int) * [1,1,1,1,1,1,0,0,0,0]
        # The above matrix does not lead to convergence.
        select_matrix = np.random.randint(2, size=parent_1.shape)

        child_1 = parent_1 * select_matrix + parent_2 * (select_matrix ^ 1)
        child_2 = parent_2 * select_matrix + parent_1 * (select_matrix ^ 1)

        return child_1, child_2

    def mutate(row):
        colomn = random.randrange(10)
        if colomn in (0, 2, 4):
            row[colomn] = random.randrange(width)
        elif colomn in (1, 3, 5):
            row[colomn] = random.randrange(height)
        else:
            row[colomn] = random.randrange(255)
        return row

    def themain(st):

        # Step 1: Generate chromosomes as candidates
        candidates = [Chromosome(num_polygons, width, height)
                      for i in range(num_chromosomes)]

        for generation in range(num_generations):

            # Step 2: Evaluate
            evals = [evaluate(imgOrigin, to_img(candidate))
                     for candidate in candidates]
            # print(evals)

            # Step 3: Select
            parent_1, parent_2 = select(evals, candidates)

            # Step 4: Crossover
            child_1, child_2 = crossover(parent_1, parent_2)

            # Step 5: Mutate
            index = random.randrange(num_polygons)
            child_1[index] = mutate(child_1[index])
            index = random.randrange(num_polygons)
            child_2[index] = mutate(child_2[index])

            # Step 6: Evaluate two parents and two children
            candidates = (parent_1, parent_2, child_1, child_2)
            # evals = [evaluate(imgOrigin, to_img(candidate))
            #         for candidate in candidates]
            base_out = to_img(child_1)
            err = np.sum((imgOrigin.astype("float") -
                         base_out.astype("float")) ** 2)
            err /= float(imgOrigin.shape[0] * base_out.shape[1])
            err1 = "{:.2f}".format(err)
            if generation % 50 == 0:
                for i in range(0, totalP):
                    if st == "Process : "+str(i+1):
                        cv2.imwrite(filename+"_OutPut//Part_"+str(i) +
                                    '//{}.png'.format(generation), base_out)
                print(st+" At Generation : "+str(generation) +
                      " & Fitness : "+str(err1))
            if err < 700:
                cnterr = cnterr+1
                if err < 600 and cnterr < 1000:
                    for i in range(0, totalP):
                        if st == "Process : "+str(i+1):
                            cv2.imwrite(filename+"_OutPut//Part_"+str(i) +
                                        '//{}.png'.format(generation), base_out)
                    print(st+" At Generation : "+str(generation) +
                          " & Fitness : "+str(err1))
                    return
            elif err < 1100 and generation > 200000:
                cnterr = cnterr+1
                if err < 600 and cnterr < 1000:
                    for i in range(0, totalP):
                        if st == "Process : "+str(i+1):
                            cv2.imwrite(filename+"_OutPut//Part_"+str(i) +
                                        '//{}.png'.format(generation), base_out)
                    print(st+" At Generation : "+str(generation) +
                          " & Fitness : "+str(err1))
                    return
    themain(st)


class Chromosome(object):
    def __init__(self, pol):
        self.num_polygons = pol

    def __new__(self, num_polygons, width, height):
        """
        structure is [x0,y0,x1,y1,x2,y2,r,g,b,alpha] 
        x0, x1, x2 in range(0, width]
        y0, y1, y2 in range(0, height]
        r,g,b,alpha in range (0,255]
        in total there exits 10 items
        """
        chromosome = np.random.rand(num_polygons, 10) \
            * [width, height, width, height, width, height, 255, 255, 255, 255]
        chromosome = chromosome.astype(int)
        return chromosome

    def __str__(self):
        return np.fromstring(self)
