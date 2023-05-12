import matplotlib.pyplot as plt
import cv2
import numpy as np
import os

def ConnectedComponent(imgin):
    ret, temp = cv2.threshold(imgin, 20, 255, cv2.THRESH_BINARY)
    temp = cv2.medianBlur(temp, 7)
    num_labels, label = cv2.connectedComponents(temp)
    print('Co %d thanh phan lien thong' % (num_labels-1))

    a = np.zeros(num_labels, np.int32)
    M, N = label.shape
    color = 150
    for x in range(0, M):
        for y in range(0, N):
            r = label[x, y]
            a[r] = a[r] + 1
            if r > 0:
                label[x,y] = label[x,y] + color

    for r in range(1, num_labels):
        print('%4d %10d' % (r, a[r]))
    return label.astype(np.uint8)

#for binary image only
#union-find algorithm
def connected_components(image):
    labels = image.copy()
    ret, labels = cv2.threshold(labels, 20, 255, cv2.THRESH_BINARY)
    current_label = 1
    parent = [0]

    #find the label 
    #make sure label pass in is same as parent 
    def find_root(label):
        while label < len(parent) and parent[label] != label:
            label = parent[label]
        return label

    for row in range(labels.shape[0]):
        for col in range(labels.shape[1]):
            if labels[row, col] == 0:
                continue

            neighbors = []

            # Check the 4 neighbors above, left, right, and below is 1 or not
            if row > 0 and labels[row - 1, col]:
                neighbors.append(labels[row - 1, col])
            if col > 0 and labels[row, col - 1]:
                neighbors.append(labels[row, col - 1])
            if row + 1 < labels.shape[0] and labels[row + 1, col]: 
                neighbors.append(labels[row + 1, col])
            if col + 1 < labels.shape[1] and labels[row, col + 1]:
                neighbors.append(labels[row, col + 1])

            # If no neighbors are 1, assign a new label
            if not neighbors:
                labels[row, col] = current_label
                parent.append(current_label)
                current_label += 1
            else:
            # If there are neighbors, assign the neighbor label
                neighbor_labels = [find_root(n) for n in neighbors]
                selected_neighbor_label = min(neighbor_labels)
                labels[row, col] = selected_neighbor_label
                for n in neighbor_labels:
                    if n != selected_neighbor_label:
                        parent[n] = selected_neighbor_label

    return labels

img = cv2.imread("./Bear.jpg", cv2.IMREAD_GRAYSCALE)
res = ConnectedComponent(img)
cv2.imshow("Result", res)
cv2.waitKey(0)
cv2.destroyAllWindows()