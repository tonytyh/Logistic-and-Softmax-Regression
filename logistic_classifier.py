import numpy as np
import load_train_data
import load_test_data
# from logistic_regression import *
import matplotlib.pyplot as plt



def check(W,X,Target):
    '''
    get the error rate
    :param W: Weights , m * 1 vector
    :param X: Input data (matrix) m * N matrix, X[i,j] represents  ith feature of jth data
    :param Target: target, for example, training target, test target, hold out target
    :return: error rate within 0-1
    '''
    return np.sum(np.abs(np.round(sigmoid(W,X)) - Target))/Target.shape[0]

def sigmoid(W,X):
    '''

    :param W: weights, m * 1 vector
    :param X: input data (matrix) m * N matrix, X[i,j] represents  ith feature of jth data
    :return: N * 1 vector
    '''
    z = np.dot(W.T,X)
    Y = 1.0 / (1.0 + np.exp(-z))

    return Y.T

def loss(Target,Y):
    '''

    :param Target: target, N * 1 vector for example, training target, test target, hold out target
    :param Y: sigmoid result N * 1 vector
    :return: loss, float
    '''
    E = 0
    # for n in range(len(Target)):
        # E = E + np.power(Target[n],Y[n]) * np.power(1-Y[n],Target[n])
    E = np.dot(np.log10(Y.T+1e-10),Target) + np.dot(np.log10(1 - Y.T+1e-10),1 - Target)
    # print()
    return -float(E)/len(Target)


def regularized_gradient_descent(type_of_regularization,Lamada,train_set,train_target,test_set,test_target):
    train_set_weights = np.zeros((train_set.shape[0],1))
    train_set_weights[-1] = 1
    train_set_accuracy = []
    train_set_loss = []
    length_of_weights = []
    test_set_accuracy = []
    eta_0 = 0.001
    T = 100
    # Lamada = 0.01

    for epoch in range(100):
        train_set_accuracy.append(1 - check(train_set_weights, train_set, train_target))
        test_set_accuracy.append(1 - check(train_set_weights, test_set, test_target))
        #
        train_set_loss.append(loss(train_target, sigmoid(train_set_weights, train_set)))

        eta = eta_0 / (1 + epoch / T)
        if type_of_regularization == "l2":
            train_set_weights = train_set_weights + eta * (np.dot(train_set,train_target - sigmoid(train_set_weights, train_set)) - Lamada * 2 * train_set_weights)
            # length_of_weights.append(np.linalg.norm(train_set_weights))
        else:
            train_set_weights = train_set_weights + eta * (np.dot(train_set,train_target - sigmoid(train_set_weights, train_set)) - Lamada * np.sign(train_set_weights))

        length_of_weights.append(np.linalg.norm(train_set_weights))


    return length_of_weights,train_set_weights,train_set_accuracy,test_set_accuracy





def gradient_descent(train_set,train_target,hold_out_set,hold_out_target,test_set,test_target):
    '''

    :param train_set: training set, m * N matrix
    :param train_target: training target, N * 1 vector
    :param hold_out_set:
    :param hold_out_target:
    :param test_set:
    :param test_target:
    :return: train_set_weights,train_set_accuracy,hold_out_accuracy,test_set_accuracy,train_set_loss,hold_out_loss,test_set_loss
    '''
    
    train_set_weights = np.zeros((train_set.shape[0],1))
    train_set_weights[-1] = 1
    train_set_accuracy = []
    hold_out_accuracy = []
    test_set_accuracy = []
    train_set_loss = []
    hold_out_loss = []
    test_set_loss = []
    eta_0 = 0.001
    T = 100
    
    for epoch in range(100):

        train_set_accuracy.append(1 - check(train_set_weights,train_set,train_target))
        hold_out_accuracy.append(1 - check(train_set_weights,hold_out_set,hold_out_target))
        test_set_accuracy.append(1 - check(train_set_weights,test_set,test_target))
        #
        train_set_loss.append(loss(train_target,sigmoid(train_set_weights,train_set)))
        hold_out_loss.append(loss(hold_out_target,sigmoid(train_set_weights,hold_out_set)))
        test_set_loss.append(loss(test_target,sigmoid(train_set_weights,test_set)))

        eta = eta_0 / (1 + epoch / T)
        train_set_weights = train_set_weights + eta * np.dot(train_set,train_target - sigmoid(train_set_weights,train_set))
    
    return train_set_weights,train_set_accuracy,hold_out_accuracy,test_set_accuracy,train_set_loss,hold_out_loss,test_set_loss



def mini_batch_gradient_descent(train_set,train_target):
    train_set_weights = np.zeros((train_set.shape[0], 1))
    train_set_weights[-1] = 1
    train_set_accuracy = []
    hold_out_accuracy = []
    test_set_accuracy = []
    train_set_loss = []
    hold_out_loss = []
    test_set_loss = []
    eta_0 = 0.001
    T = 100
    how_many_mini_batches = 10

    batches_sizes = [train_set.shape[1] // how_many_mini_batches] * how_many_mini_batches
    random_index = np.arange((train_set.shape[1]//how_many_mini_batches) * how_many_mini_batches)
    np.random.shuffle(random_index)
    random_mini_batches_set = np.array([train_set[:,x] for x in np.split(random_index,how_many_mini_batches)])
    random_mini_batches_target = np.array([train_target[x].squeeze() for x in np.split(random_index, how_many_mini_batches)])

    max_epoch = 4

    update_times = 0

    for epoch in range(max_epoch):
        for i in range(how_many_mini_batches):
            update_times +=1
            eta = eta = eta_0 / (1 + update_times / T)
            train_set_weights = train_set_weights + eta * np.dot(random_mini_batches_set[i],random_mini_batches_target - sigmoid(train_set_weights,random_mini_batches_set[i]))
            train_set_accuracy.append(1 - check(train_set_weights, train_set, train_target))
    return train_set_weights,train_set_accuracy


    # for epoch in range(100):
    #     train_set_accuracy.append(1 - check(train_set_weights, train_set, train_target))
    #     # hold_out_accuracy.append(1 - check(train_set_weights, hold_out_set, hold_out_target))
    #     # test_set_accuracy.append(1 - check(train_set_weights, test_set, test_target))
    #     #
    #     train_set_loss.append(loss(train_target, sigmoid(train_set_weights, train_set)))
    #     # hold_out_loss.append(loss(hold_out_target, sigmoid(train_set_weights, hold_out_set)))
    #     # test_set_loss.append(loss(test_target, sigmoid(train_set_weights, test_set)))
    #
    #     eta = eta_0 / (1 + epoch / T)
    #     train_set_weights = train_set_weights + eta * np.dot(train_set,train_target - sigmoid(train_set_weights, train_set))

    return train_set_weights, train_set_accuracy#, hold_out_accuracy, test_set_accuracy, train_set_loss, hold_out_loss, test_set_loss

        
    

def plot_weights(Weights):
    '''

    :param Weights: weights
    :return: picture in 28 * 28
    '''
    plt.imshow(Weights[0:-1].reshape(28,28))

def plot_accuracy(accuracy):
    '''

    :param accuracy: accuracy for all epochs, 1 * N vector
    :return: accuracy plot
    '''
    x = np.arange(len(accuracy))
    y = np.array(accuracy) * 100

    # plt.plot(x,y,marker = '.',linestyle = '-')
    plt.plot(x, y)
def plot_loss(loss,color):
    '''

    :param loss: loss for all epochs, 1 * N vector
    :param color: specifiy color, example 'r','b'
    :return: plot of loss
    '''
    x = np.arange(len(loss))
    y = np.array(loss)

    # plt.plot(x, y, marker='.', linestyle='-',color = color)
    plt.plot(x, y)

def plot_length_of_weights(length_of_weights):
    y = np.array(length_of_weights)
    x= np.arange(len(length_of_weights))
    plt.plot(x,y)

def make_train_data(numberA,numberB):
    '''

    :param numberA: specify which number we choose to make training data, for example 2
    :param numberB: specify which number we choose to make training data, for example 3
    :return:
    train_input : data, (m+1) * N matrix
    train_target : target N * 1 matrix
    hold_out_input
    hold_out_target

    '''

    image_A = load_train_data.fetch_image(numberA)
    image_B = load_train_data.fetch_image(numberB)

    #make_train_set

    train_image_A = image_A[np.fix(image_A.shape[0] * 0.1).astype(int):]
    train_image_B = image_B[np.fix(image_B.shape[0] * 0.1).astype(int):]
    train_input_A = np.concatenate((train_image_A, np.ones((1, train_image_A.shape[0])).T), axis=1).T
    train_input_B = np.concatenate((train_image_B, np.ones((1, train_image_B.shape[0])).T), axis=1).T
    train_target = np.concatenate((np.ones((1, train_input_A.shape[1])), np.zeros((1, train_input_B.shape[1]))), axis=1).T
    train_input = np.concatenate((train_input_A, train_input_B), axis=1)

    #make hold-out set
    hold_out_image_A = image_A[:np.fix(image_A.shape[0] * 0.1).astype(int)]
    hold_out_image_B = image_B[:np.fix(image_B.shape[0] * 0.1).astype(int)]

    hold_out_input_A = np.concatenate((hold_out_image_A, np.ones((1, hold_out_image_A.shape[0])).T), axis=1).T
    hold_out_input_B = np.concatenate((hold_out_image_B, np.ones((1, hold_out_image_B.shape[0])).T), axis=1).T
    hold_out_target = np.concatenate((np.ones((1, hold_out_input_A.shape[1])), np.zeros((1, hold_out_input_B.shape[1]))), axis=1).T
    hold_out_input = np.concatenate((hold_out_input_A, hold_out_input_B), axis=1)


    return train_input,train_target,hold_out_input,hold_out_target

def make_test_data(numberA,numberB):
    '''

    :param numberA: specify which number we choose to make training data, for example 2
    :param numberB: specify which number we choose to make training data, for example 3
    :return:
    test_input : (m + 1) * N matrix
    test_target : N * 1 vector
    '''
    test_image_A = load_test_data.fetch_image(numberA)
    test_image_B = load_test_data.fetch_image(numberB)
    test_input_A = np.concatenate((test_image_A, np.ones((1, test_image_A.shape[0])).T), axis=1).T
    test_input_B = np.concatenate((test_image_B, np.ones((1, test_image_B.shape[0])).T), axis=1).T
    test_target = np.concatenate((np.ones((1, test_input_A.shape[1])), np.zeros((1, test_input_B.shape[1]))), axis=1).T
    test_input = np.concatenate((test_input_A, test_input_B), axis=1)

    return test_input,test_target




if __name__ == "__main__":


    # 2 vs 3

    train_input_2vs3,train_target_2vs3,hold_out_input_2vs3,hold_out_target_2vs3 = make_train_data(2,3)
    test_input_2vs3, test_target_2vs3 = make_test_data(2, 3)

    # train_Weights_2vs3,train_accuracy_2vs3,hold_out_accuracy_2vs3,test_set_accuracy_2vs3,train_set_loss_2vs3,hold_out_loss_2vs3,test_set_loss_2vs3 = gradient_descent(train_input_2vs3, train_target_2vs3,hold_out_input_2vs3,hold_out_target_2vs3,test_input_2vs3,test_target_2vs3)
    # #train_Weights_2vs3,train_accuracy_2vs3 = gradient(train_input_2vs3,train_target_2vs3)
    #

    # train_Weights_2vs3, train_accuracy_2vs3 = mini_batch_gradient_descent(train_input_2vs3, train_target_2vs3)
    # plt.figure(1)
    # ax = plt.gca()
    # ax.set_title("Weights Pattern 2 vs 3")
    # plot_weights(train_Weights_2vs3)
    # plt.show()
    # #
    # plt.figure(2)
    # ax = plt.gca()
    # ax.set_xlim([0,500])
    # ax.set_title("Correction Rate over Training")
    # ax.set_xlabel("Training Epochs")
    # ax.set_ylabel("Correction Rate Percentage ")
    # plot_accuracy(train_accuracy_2vs3)
    # # plot_accuracy(hold_out_accuracy_2vs3)
    # # plot_accuracy(test_set_accuracy_2vs3)
    # plt.show()
    #
    # plt.figure(3)
    # ax = plt.gca()
    # # ax.grid()
    # ax.set_title("Loss (E) over Training")
    # ax.set_xlabel("Training Epochs")
    # plot_loss(train_set_loss_2vs3,'r')
    # plot_loss(hold_out_loss_2vs3,'b')
    # plot_loss(test_set_loss_2vs3,'g')
    # # ax.legend(['Training Set','Hold Out Set','Test Set'])
    # plt.show()


    #regulized logistic regression
    LAMADA = [2,1,0.1,0.001,0.00001,0]
    for Lamada in LAMADA:
        length_of_weights,reg_train_Weights_2vs3,reg_train_accuracy_2vs3,test_accuracy_2vs3=regularized_gradient_descent('l2',Lamada,train_input_2vs3,train_target_2vs3,test_input_2vs3,test_target_2vs3)
        ##plot _accuracy of training set over epochs with different lamada
        # plot_accuracy(reg_train_accuracy_2vs3)
        # ax = plt.gca()
        # ax.set_title("Accuracy over Training with different lamada")
        # ax.set_xlabel("Training Times")
        # ax.set_ylabel("Accuracy")

        ## plot length of weights
        # plot_length_of_weights(length_of_weights)
        # ax = plt.gca()
        # ax.set_title("Lengths of Weights over Training with different lamada")
        # ax.set_xlabel("Training Times")
        # ax.set_ylabel("Lengths of Weights")

        ## plot error with different lamada
        # plot_accuracy(1-np.array(test_accuracy_2vs3))
        # plt.scatter(np.log10(Lamada),1-test_accuracy_2vs3[-1])




    ax = plt.gca()
    ax.legend(["lamada = 2","lamada = 1","lamada = 0.1","lamada = 0.001","lamada = 0.00001","lamada = 0"])
    plt.show()










