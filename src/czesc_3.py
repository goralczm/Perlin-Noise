from tkinter.ttk import Label

from czesc_2 import *

seed = 42
tab_wart = [0, 0.3333, 0.6667, 1.0]
tab_perm = [1, 3, 2, 0, 1, 3, 2, 0]

def funkcja_skrotu_uniw_perm_v3(tab_skl, tab_perm):
    dtw = len(tab_perm) // 2
    wynik = 0
    for skl_c in tab_skl:
        if skl_c < 0:
            czy_ujemne = 1
            skl_c = -skl_c
        else:
            czy_ujemne = 0
        wynik = tab_perm[wynik + (skl_c % dtw)]
        skl_c = math.floor(skl_c / dtw)
        while skl_c > 0:
            wynik = tab_perm[wynik + (skl_c % dtw)]
            skl_c = math.floor(skl_c / dtw)

        if czy_ujemne:
            wynik = tab_perm[wynik]

    return wynik

def interpolacja_2d_rdzen_vlin(w_ld, w_lg, w_pd, w_pg, delta_x, delta_y):
    return w_ld * (1 - delta_x) * (1 - delta_y) + w_lg * (1 - delta_x) * delta_y + w_pd * delta_x * (1 - delta_y) + w_pg * delta_x * delta_y

def interpolacja_2d_rdzen_vnlin(w_ld, w_lg, w_pd, w_pg, delta_x, delta_y):
    delta_x = 6 * math.pow(delta_x, 5) - 15 * math.pow(delta_x, 4) + 10 * math.pow(delta_x, 3)
    delta_y = 6 * math.pow(delta_y, 5) - 15 * math.pow(delta_y, 4) + 10 * math.pow(delta_y, 3)

    return interpolacja_2d_rdzen_vlin(w_ld, w_lg, w_pd, w_pg, delta_x, delta_y)

def interpolacja_2d_cala_vperm_nlin(x, y, tab_wart, tab_perm):
    x_l = math.floor(x)
    x_p = x_l + 1
    x_delta = x - x_l
    y_d = math.floor(y)
    y_g = y_d + 1
    y_delta = y - y_d
    i_ld = funkcja_skrotu_uniw_perm_v3([x_l, y_d], tab_perm)
    i_lg = funkcja_skrotu_uniw_perm_v3([x_l, y_g], tab_perm)
    i_pd = funkcja_skrotu_uniw_perm_v3([x_p, y_d], tab_perm)
    i_pg = funkcja_skrotu_uniw_perm_v3([x_p, y_g], tab_perm)
    w_ld = tab_wart[i_ld]
    w_lg = tab_wart[i_lg]
    w_pd = tab_wart[i_pd]
    w_pg = tab_wart[i_pg]
    return interpolacja_2d_rdzen_vnlin(w_ld, w_lg, w_pd, w_pg, x_delta, y_delta)

def interpolacja_2d_cala_vperm_lin(x, y, tab_wart, tab_perm):
    x_l = math.floor(x)
    x_p = x_l + 1
    x_delta = x - x_l
    y_d = math.floor(y)
    y_g = y_d + 1
    y_delta = y - y_d
    i_ld = funkcja_skrotu_uniw_perm_v3([x_l, y_d], tab_perm)
    i_lg = funkcja_skrotu_uniw_perm_v3([x_l, y_g], tab_perm)
    i_pd = funkcja_skrotu_uniw_perm_v3([x_p, y_d], tab_perm)
    i_pg = funkcja_skrotu_uniw_perm_v3([x_p, y_g], tab_perm)
    w_ld = tab_wart[i_ld]
    w_lg = tab_wart[i_lg]
    w_pd = tab_wart[i_pd]
    w_pg = tab_wart[i_pg]
    return interpolacja_2d_rdzen_vlin(w_ld, w_lg, w_pd, w_pg, x_delta, y_delta)

def szum_2d_pseudoperlina_vperm3_vnlin(x, y, tab_wart, tab_perm):
    return interpolacja_2d_cala_vperm_nlin(x, y, tab_wart, tab_perm)

def szum_2d_pseudoperlina_vperm3_vlin(x, y, tab_wart, tab_perm):
    return interpolacja_2d_cala_vperm_lin(x, y, tab_wart, tab_perm)

def szum_2d_pseudoperlin_oktawy(x, y, tab_wart, tab_perm, oktawa_liczba, oktawa_mnoznik, oktawa_zageszczenie):
    ampl_suma = 0
    wy = 0
    for okt_n in range(0, oktawa_liczba):
        wys_mnoznik = math.pow(oktawa_mnoznik, okt_n)
        zageszczenie_mnoznik = math.pow(oktawa_zageszczenie, okt_n)
        ampl_suma += wys_mnoznik
        wy += wys_mnoznik * szum_2d_pseudoperlina_vperm3_vnlin(x * zageszczenie_mnoznik, y * zageszczenie_mnoznik, tab_wart, tab_perm)

    wy = wy / ampl_suma
    return wy

if __name__ == '__main__':
    def test_funkcja_skrotu_uniw_perm_v3_v1():
        x = np.arange(-5, 5, 1)
        y = [funkcja_skrotu_uniw_perm_v3([delta], [1, 2, 0, 1, 2, 0]) for delta in x]
        print(x)
        print(y)

    #test_funkcja_skrotu_uniw_perm_v3_v1()

    def test_funkcja_skrotu_uniw_perm_v3_v2():
        tab_perm = [1, 3, 2, 0, 1, 3, 2, 0]
        x = np.arange(-1, 10, 1)
        y = np.arange(0, 7, 1)

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = funkcja_skrotu_uniw_perm_v3([X[i, j], Y[i, j]], tab_perm)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        print(Z)
        plt.show()

    #test_funkcja_skrotu_uniw_perm_v3_v2()

    def test_interpolacja_2d_rdzen_vlin():
        x = np.arange(0, 1, .1)
        y = np.arange(0, 1, .1)

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = interpolacja_2d_rdzen_vlin(0, 1, 3, 2, X[i, j], Y[i, j])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        plt.show()

    #test_interpolacja_2d_rdzen_vlin()

    def test_interpolacja_2d_rdzen_vnlin():
        x = np.arange(0, 1, .1)
        y = np.arange(0, 1, .1)

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = interpolacja_2d_rdzen_vnlin(0, 1, 3, 2, X[i, j], Y[i, j])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        plt.show()

    #test_interpolacja_2d_rdzen_vnlin()

    def test_interpolacja_2d_cala_vperm_nlin_lin():
        tab_wart = [0, 0.3333, 0.6667, 1.0]
        tab_perm = [1, 3, 2, 0, 1, 3, 2, 0]

        x = np.arange(-1, 3, .1)
        y = np.arange(2, 4, .1)

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = interpolacja_2d_cala_vperm_nlin(X[i, j], Y[i, j], tab_wart, tab_perm)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        plt.show()

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = interpolacja_2d_cala_vperm_lin(X[i, j], Y[i, j], tab_wart, tab_perm)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        plt.show()

    #test_interpolacja_2d_cala_vperm_nlin_lin()

    def test_szum_2d_pseudoperlin_oktawy():
        tab_wart = [0, 0.3333, 0.6667, 1.0]
        tab_perm = [1, 3, 2, 0, 1, 3, 2, 0]

        x = np.arange(-1, 3, .1)
        y = np.arange(2, 4, .1)

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = szum_2d_pseudoperlin_oktawy(X[i, j], Y[i, j], tab_wart, tab_perm, 3, .5, 2)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        plt.show()

    #test_szum_2d_pseudoperlin_oktawy()

    # <--- Ćwiczenia --->
    def zadanie_1():
        x = np.arange(-5, 5, 1)
        y = [funkcja_skrotu_uniw_perm_v3([delta], [1, 2, 0, 1, 2, 0]) for delta in x]
        print(x)
        print(y)

    zadanie_1()

    def zadanie_2():
        tab_wart = [0, 0.3333, 0.6667, 1.0]
        tab_perm = [1, 3, 2, 0, 1, 3, 2, 0]

        x = np.arange(-1, 3, .1)
        y = np.arange(2, 4, .1)

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = interpolacja_2d_cala_vperm_nlin(X[i, j], Y[i, j], tab_wart, tab_perm)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('interpolacja_2d_cala_vperm_nlin')

        plt.show()

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = interpolacja_2d_cala_vperm_lin(X[i, j], Y[i, j], tab_wart, tab_perm)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('interpolacja_2d_cala_vperm_lin')

        plt.show()

    zadanie_2()

    def zadanie_3():
        tab_wart = [0, 0.3333, 0.6667, 1.0]
        tab_perm = [1, 3, 2, 0, 1, 3, 2, 0]

        x = np.arange(-1, 3, .1)
        y = np.arange(2, 4, .1)

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = szum_2d_pseudoperlin_oktawy(X[i, j], Y[i, j], tab_wart, tab_perm, 2, .5, 2)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('szum_2d_pseudoperlin_oktawy, oktawa_liczba=2, oktawa_mnoznik=0.5, oktawa_zageszczenie=2')

        plt.show()

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = interpolacja_2d_cala_vperm_nlin(X[i, j], Y[i, j], tab_wart, tab_perm)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('interpolacja_2d_cala_vperm_nlin')

        plt.show()

        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = interpolacja_2d_cala_vperm_nlin(X[i, j] * 2, Y[i, j] * 2, tab_wart, tab_perm) * 0.5

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('interpolacja_2d_cala_vperm_nlin * 0.5, 2x, 2y')

        plt.show()

    zadanie_3()