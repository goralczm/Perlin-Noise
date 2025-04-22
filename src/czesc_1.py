import random
import matplotlib.pyplot as plt
import math
import numpy as np

def wartosci_losowe_wygeneruj_v0(dtw, seed):
    random.seed(seed)
    return [random.random() for _ in range(dtw)]

def funkcja_skrotu_1d_v0(x_c, dtw):
    return x_c % dtw

def wartosci_losowe_wygeneruj_v1(dtw, seed):
    random.seed(seed)
    return [0, 1] + [random.random() for _ in range(dtw - 2)]

def interpolacja_1d_rdzen_vlin(w_l, w_p, delta_x):
    return w_p * delta_x + w_l * (1 - delta_x)

def interpolacja_1d_cala_vlin(x, tab_wart):
    x_l = math.floor(x)
    x_p = x_l + 1
    i_x_l = funkcja_skrotu_1d_v0(x_l, len(tab_wart))
    i_x_p = funkcja_skrotu_1d_v0(x_p, len(tab_wart))
    w_l = tab_wart[i_x_l]
    w_p = tab_wart[i_x_p]
    delta_x = x - x_l

    return interpolacja_1d_rdzen_vlin(w_l, w_p, delta_x)

def vkos(delta_x):
    return math.cos(math.pi + delta_x * math.pi) / 2 + .5

def vwmian(delta_x):
    return 6 * math.pow(delta_x, 5) - 15 * math.pow(delta_x, 4) + 10 * math.pow(delta_x, 3)

def interpolacja_1d_rdzen_vnlin(w_l, w_p, delta_x, f):
    delta_x = f(delta_x)
    return w_p * delta_x + w_l * (1 - delta_x)

def interpolacja_1d_cala_vnlin(x, tab_wart):
    x_l = math.floor(x)
    x_p = x_l + 1
    i_x_l = funkcja_skrotu_1d_v0(x_l, len(tab_wart))
    i_x_p = funkcja_skrotu_1d_v0(x_p, len(tab_wart))
    w_l = tab_wart[i_x_l]
    w_p = tab_wart[i_x_p]
    delta_x = x - x_l

    return interpolacja_1d_rdzen_vnlin(w_l, w_p, delta_x, vkos)

if __name__ == '__main__':
    seed = 42

    #plt.bar(range(8), wartosci_losowe_wygeneruj_v1(8, seed))
    #plt.show()

    x = [0, .2, .4, .6, .8, 1]
    y = [interpolacja_1d_rdzen_vlin(.3, .7, delta) for delta in x]
    #plt.plot(x, y)
    #plt.title('interpolacja_1d_rdzen_vlin dla w_l=0.3, w_p=0.7')
    #plt.show()

    x = np.arange(-10, 16, .01)
    tab_wart = wartosci_losowe_wygeneruj_v1(8, seed)
    y = [interpolacja_1d_cala_vlin(wart, tab_wart) for wart in x]
    #plt.plot(x, y)
    #plt.title('interpolacja_1d_cala_vlin')
    #plt.show()

    def test_vkos(delta_x):
        return interpolacja_1d_rdzen_vnlin(0, 1, delta_x, vkos)

    def test_vwmian(delta_x):
        return interpolacja_1d_rdzen_vnlin(0, 1, delta_x, vwmian)

    x = np.arange(0, 1, .1)
    y_vkos = np.array(list(map(test_vkos, x)))
    y_vwmian = np.array(list(map(test_vwmian, x)))
    #plt.plot(x, y_vkos)
    #plt.plot(x, y_vwmian)
    #plt.show()

    x = np.arange(-10, 16, .1)
    tab_wart = wartosci_losowe_wygeneruj_v1(8, seed)
    y = [interpolacja_1d_cala_vnlin(wart, tab_wart) for wart in x]
    #plt.plot(x, y)
    #plt.title('interpolacja_1d_cala_vnlin')
    #plt.show()

    #fig, axs = plt.subplots(2)
    #fig.suptitle('przed i po interpolacja_1d_cala_vnlin')
    #axs[1].plot(x, y)

    x = np.arange(-10, 16, .1)
    tab_wart = wartosci_losowe_wygeneruj_v1(8, seed)
    y = [interpolacja_1d_cala_vlin(wart, tab_wart) for wart in x]
    #axs[0].plot(x, y)

    #plt.show()

    # <---- Ćwiczenia ---->
    print(f'1. wartosci_losowe_wygeneruj_v0: {wartosci_losowe_wygeneruj_v0(8, seed)}\n   wartosci_losowe_wygeneruj_v1: {wartosci_losowe_wygeneruj_v1(8, seed)}')

    funkcja_skrotu_1d = {x: funkcja_skrotu_1d_v0(x, 8) for x in range(-10, 16)}
    print(f'2. funkcja_skrotu_1d_v0: {funkcja_skrotu_1d}')

    x = np.arange(0, 1, .1)
    y = [interpolacja_1d_rdzen_vlin(.3, .7, delta) for delta in x]
    plt.plot(x, y)
    plt.title('3. interpolacja_1d_rdzen_vlin dla w_l=0.3, w_p=0.7')
    plt.show()

    x = np.arange(0, 1, .1)
    y = [interpolacja_1d_rdzen_vlin(.9, .2, delta) for delta in x]
    plt.plot(x, y)
    plt.title('3. interpolacja_1d_rdzen_vlin dla w_l=0.9, w_p=0.2')
    plt.show()

    def test_vkos_v1(delta_x):
        return interpolacja_1d_rdzen_vnlin(.3, .7, delta_x, vkos)

    def test_vwmian_v1(delta_x):
        return interpolacja_1d_rdzen_vnlin(.3, .7, delta_x, vwmian)

    x = np.arange(0, 1, .05)
    y_vkos = np.array(list(map(test_vkos_v1, x)))
    y_vwmian = np.array(list(map(test_vwmian_v1, x)))
    plt.plot(x, y_vkos)
    plt.plot(x, y_vwmian)
    plt.title('4. interpolacja_1d_rdzen_vkos i vwmian dla w_l=0.3, w_p=0.7')
    plt.show()

    def test_vkos_v2(delta_x):
        return interpolacja_1d_rdzen_vnlin(.9, .2, delta_x, vkos)

    def test_vwmian_v2(delta_x):
        return interpolacja_1d_rdzen_vnlin(.9, .2, delta_x, vwmian)

    y_vkos = np.array(list(map(test_vkos_v2, x)))
    y_vwmian = np.array(list(map(test_vwmian_v2, x)))
    plt.plot(x, y_vkos)
    plt.plot(x, y_vwmian)
    plt.title('4. interpolacja_1d_rdzen_vkos i vwmian dla w_l=0.9, w_p=0.2')
    plt.show()

    x = np.arange(-4, 9, .05)
    tab_wart = wartosci_losowe_wygeneruj_v1(4, seed)
    y = [interpolacja_1d_cala_vlin(wart, tab_wart) for wart in x]
    plt.plot(x, y)
    plt.title('5. interpolacja_1d_cala_vlin')
    plt.show()

    tab_wart = wartosci_losowe_wygeneruj_v1(4, seed)
    y = [interpolacja_1d_cala_vnlin(wart, tab_wart) for wart in x]
    plt.plot(x, y)
    plt.title('5. interpolacja_1d_cala_vnlin')
    plt.show()