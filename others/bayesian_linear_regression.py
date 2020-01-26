import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def bayesian_linear_regression(filepath):
    if type(filepath) != pd.DataFrame
        df = pd.read_csv(filepath, header=None)
    else:
        df = filepath

    # X = np.array([0.02, 0.12, 0.19, 0.27, 0.42, 0.51, 0.64, 0.84, 0.88, 0.99])
    # y = np.array([0.05, 0.87, 0.94, 0.92, 0.54, -0.11, -0.78, -0.79, -0.89, -0.04])
    X = df.index
    y = df[0]

    #基底関数 ガウス関数
    def phi(x):
        #ガウス関数のバンド幅
        s = 0.1
        return np.append(1,np.exp(-(x - np.arange(0,1+s,s))**2/(2 * s * s)))

    PhiX = np.array([phi(x) for x in X])

    #1/sigma_n^2 = alpha
    alpha = 9.0
    #Sigma_p^-1 = beta * I
    beta = 0.1

    #p
    A = alpha * np.dot(PhiX.T,PhiX) + beta * np.identity(PhiX.shape[1])
    w_bar = alpha * np.dot(np.dot(np.linalg.inv(A),PhiX.T),y)

    xlist = np.arange(0,len(X),1)
    ylist = [np.dot(w_bar,phi(x)) for x in xlist]
    #予測分布の分散
    s_2 = [1.0/alpha + np.dot(np.dot(phi(x),np.linalg.inv(A)),phi(x).T) for x in xlist]

    s = np.sqrt(s_2)
    predict_upper = ylist + s
    predict_lower = ylist - s
    plt.plot(xlist,ylist)
    plt.plot(X,y,'o')
    plt.fill_between(xlist,predict_upper,predict_lower,facecolor='r',alpha=0.2)
    plt.show()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()
    bayesian_linear_regression(args.file)
